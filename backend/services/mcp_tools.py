"""
MCP Tools for AI Chatbot
Model Context Protocol tools that the chatbot can invoke to perform task operations
"""
from typing import Dict, Any, Optional
from datetime import datetime
from sqlmodel import Session

from database import queries
from models.task import Task
from models.enums import PriorityLevel


def add_task(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Create a new task in the user's account

    This tool wraps the existing Phase 2 task creation functionality
    and provides a structured interface for the AI chatbot.

    Args:
        session: Database session
        user_id: User ID from JWT token (enforces user isolation)
        title: Task title (required, max 200 chars)
        description: Task description (optional, max 1000 chars)
        priority: Priority level - "low", "medium", "high" (default: "medium")
        due_date: Due date in ISO format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ (optional)

    Returns:
        Dictionary with success status, task data, and message

    Example Success Response:
        {
            "success": True,
            "task": {
                "id": 123,
                "title": "Buy groceries",
                "description": "",
                "status": "pending",
                "priority": "medium",
                "due_date": None,
                "created_at": "2026-02-09T10:30:00Z"
            },
            "message": "Task created successfully"
        }

    Example Error Response:
        {
            "success": False,
            "error": {
                "code": "INVALID_TITLE",
                "message": "Task title cannot be empty",
                "details": "Please provide a task title"
            }
        }
    """
    try:
        # Validate title
        if not title or not title.strip():
            return {
                "success": False,
                "error": {
                    "code": "INVALID_TITLE",
                    "message": "Task title cannot be empty",
                    "details": "Please provide a task title"
                }
            }

        if len(title) > 500:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_TITLE",
                    "message": "Task title is too long",
                    "details": "Title must be 500 characters or less"
                }
            }

        # Validate and convert priority
        priority_lower = priority.lower()
        if priority_lower not in ["low", "medium", "high"]:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_PRIORITY",
                    "message": "Invalid priority level",
                    "details": "Priority must be one of: low, medium, high"
                }
            }

        # Convert priority string to enum
        priority_enum = PriorityLevel(priority_lower)

        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                # Try parsing ISO format
                due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                return {
                    "success": False,
                    "error": {
                        "code": "INVALID_DATE",
                        "message": "Invalid due date format",
                        "details": "Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)"
                    }
                }

        # Create Task object
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority_enum,
            due_date=due_date_obj,
            completed=False
        )

        # Save to database using existing Phase 2 query function
        created_task = queries.create_task(session, task)

        # Format response
        return {
            "success": True,
            "task": {
                "id": created_task.id,
                "title": created_task.title,
                "description": created_task.description or "",
                "status": "completed" if created_task.completed else "pending",
                "priority": created_task.priority.value,
                "due_date": created_task.due_date.isoformat() if created_task.due_date else None,
                "created_at": created_task.created_at.isoformat()
            },
            "message": "Task created successfully"
        }

    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"[ERROR] add_task failed: {type(e).__name__}: {e}")

        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to create task",
                "details": "An unexpected error occurred. Please try again."
            }
        }


def list_tasks(
    session: Session,
    user_id: str,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Retrieve all tasks or filtered tasks for the user

    Args:
        session: Database session
        user_id: User ID from JWT token
        status_filter: Filter by status - "pending", "completed", or None for all
        priority_filter: Filter by priority - "low", "medium", "high", or None for all

    Returns:
        Dictionary with success status, tasks array, count, and message
    """
    try:
        # Validate filters
        if status_filter and status_filter not in ["pending", "completed", "all"]:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_FILTER",
                    "message": "Invalid status filter",
                    "details": "Status must be one of: pending, completed, all"
                }
            }

        if priority_filter and priority_filter.lower() not in ["low", "medium", "high"]:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_FILTER",
                    "message": "Invalid priority filter",
                    "details": "Priority must be one of: low, medium, high"
                }
            }

        # Get tasks from database
        tasks = queries.get_user_tasks(
            session=session,
            user_id=user_id,
            status=status_filter,
            priority=priority_filter,
            sort="created_at",
            order="desc"
        )

        # Format tasks for response
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append({
                "id": task.id,
                "title": task.title,
                "description": task.description or "",
                "status": "completed" if task.completed else "pending",
                "priority": task.priority.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat()
            })

        return {
            "success": True,
            "tasks": formatted_tasks,
            "count": len(formatted_tasks),
            "message": f"Retrieved {len(formatted_tasks)} task{'s' if len(formatted_tasks) != 1 else ''}"
        }

    except Exception as e:
        print(f"[ERROR] list_tasks failed: {type(e).__name__}: {e}")

        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to retrieve tasks",
                "details": "An unexpected error occurred. Please try again."
            }
        }


def complete_task(
    session: Session,
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    MCP Tool: Mark a task as completed

    Args:
        session: Database session
        user_id: User ID from JWT token (enforces user isolation)
        task_id: ID of the task to complete

    Returns:
        Dictionary with success status, updated task data, and message
    """
    try:
        # Get task and verify ownership
        task = queries.get_task_by_id(session, task_id, user_id)

        if not task:
            return {
                "success": False,
                "error": {
                    "code": "TASK_NOT_FOUND",
                    "message": "Task not found",
                    "details": f"No task found with ID {task_id} for this user"
                }
            }

        # Check if already completed
        if task.completed:
            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "status": "completed"
                },
                "message": "Task was already completed"
            }

        # Update task to completed
        task.completed = True
        updated_task = queries.update_task(session, task)

        return {
            "success": True,
            "task": {
                "id": updated_task.id,
                "title": updated_task.title,
                "description": updated_task.description or "",
                "status": "completed",
                "priority": updated_task.priority.value,
                "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                "updated_at": updated_task.updated_at.isoformat()
            },
            "message": f"Task '{updated_task.title}' marked as completed"
        }

    except Exception as e:
        print(f"[ERROR] complete_task failed: {type(e).__name__}: {e}")

        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to complete task",
                "details": "An unexpected error occurred. Please try again."
            }
        }


def delete_task(
    session: Session,
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    MCP Tool: Delete a task from the user's account

    Args:
        session: Database session
        user_id: User ID from JWT token (enforces user isolation)
        task_id: ID of the task to delete

    Returns:
        Dictionary with success status and message
    """
    try:
        # Get task and verify ownership
        task = queries.get_task_by_id(session, task_id, user_id)

        if not task:
            return {
                "success": False,
                "error": {
                    "code": "TASK_NOT_FOUND",
                    "message": "Task not found",
                    "details": f"No task found with ID {task_id} for this user"
                }
            }

        # Store task title before deletion
        task_title = task.title

        # Delete task
        queries.delete_task(session, task_id, user_id)

        return {
            "success": True,
            "task_id": task_id,
            "message": f"Task '{task_title}' deleted successfully"
        }

    except Exception as e:
        print(f"[ERROR] delete_task failed: {type(e).__name__}: {e}")

        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to delete task",
                "details": "An unexpected error occurred. Please try again."
            }
        }


def update_task(
    session: Session,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Update task properties

    Args:
        session: Database session
        user_id: User ID from JWT token (enforces user isolation)
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority - "low", "medium", "high" (optional)
        due_date: New due date in ISO format (optional)
        completed: New completion status (optional)

    Returns:
        Dictionary with success status, updated task data, and message
    """
    try:
        # Get task and verify ownership
        task = queries.get_task_by_id(session, task_id, user_id)

        if not task:
            return {
                "success": False,
                "error": {
                    "code": "TASK_NOT_FOUND",
                    "message": "Task not found",
                    "details": f"No task found with ID {task_id} for this user"
                }
            }

        # Build update data dict
        update_data = {}
        updates = []

        # Update title if provided
        if title is not None:
            if not title.strip():
                return {
                    "success": False,
                    "error": {
                        "code": "INVALID_TITLE",
                        "message": "Task title cannot be empty",
                        "details": "Please provide a valid task title"
                    }
                }
            if len(title) > 500:
                return {
                    "success": False,
                    "error": {
                        "code": "INVALID_TITLE",
                        "message": "Task title is too long",
                        "details": "Title must be 500 characters or less"
                    }
                }
            update_data["title"] = title.strip()
            updates.append("title")

        # Update description if provided
        if description is not None:
            update_data["description"] = description.strip() if description else None
            updates.append("description")

        # Update priority if provided
        if priority is not None:
            priority_lower = priority.lower()
            if priority_lower not in ["low", "medium", "high"]:
                return {
                    "success": False,
                    "error": {
                        "code": "INVALID_PRIORITY",
                        "message": "Invalid priority level",
                        "details": "Priority must be one of: low, medium, high"
                    }
                }
            update_data["priority"] = PriorityLevel(priority_lower)
            updates.append("priority")

        # Update due_date if provided
        if due_date is not None:
            try:
                update_data["due_date"] = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                updates.append("due_date")
            except ValueError:
                return {
                    "success": False,
                    "error": {
                        "code": "INVALID_DATE",
                        "message": "Invalid due date format",
                        "details": "Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)"
                    }
                }

        # Update completed status if provided
        if completed is not None:
            update_data["completed"] = completed
            updates.append("status")

        # Check if any updates were made
        if not updates:
            return {
                "success": False,
                "error": {
                    "code": "NO_UPDATES",
                    "message": "No updates provided",
                    "details": "Please specify at least one field to update"
                }
            }

        # Save updates using the queries function with correct parameters
        updated_task = queries.update_task(session, task_id, user_id, update_data)

        if not updated_task:
            return {
                "success": False,
                "error": {
                    "code": "TASK_NOT_FOUND",
                    "message": "Task not found or update failed",
                    "details": f"Could not update task with ID {task_id}"
                }
            }

        return {
            "success": True,
            "task": {
                "id": updated_task.id,
                "title": updated_task.title,
                "description": updated_task.description or "",
                "status": "completed" if updated_task.completed else "pending",
                "priority": updated_task.priority.value,
                "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                "updated_at": updated_task.updated_at.isoformat()
            },
            "message": f"Task updated successfully ({', '.join(updates)} changed)"
        }

    except Exception as e:
        print(f"[ERROR] update_task failed: {type(e).__name__}: {e}")

        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to update task",
                "details": "An unexpected error occurred. Please try again."
            }
        }


def get_user_info(
    user_id: str,
    email: Optional[str] = None,
    name: Optional[str] = None,
    query_type: str = "all"
) -> Dict[str, Any]:
    """
    MCP Tool: Retrieve user information from JWT token

    Note: This tool does NOT query the database. It returns information
    that was already extracted from the JWT token by the authentication middleware.

    Args:
        user_id: User ID from JWT token
        email: User email from JWT token
        name: User name from JWT token
        query_type: Type of info requested - "email", "name", "user_id", "all"

    Returns:
        Dictionary with success status and user information
    """
    try:
        # Validate query type
        if query_type not in ["email", "name", "user_id", "all"]:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_QUERY_TYPE",
                    "message": "Invalid query type",
                    "details": "Query type must be one of: email, name, user_id, all"
                }
            }

        # Build user info response based on query type
        user_info = {}

        if query_type in ["user_id", "all"]:
            user_info["user_id"] = user_id

        if query_type in ["email", "all"]:
            user_info["email"] = email or "Not available"

        if query_type in ["name", "all"]:
            user_info["name"] = name or "Not available"

        return {
            "success": True,
            "user_info": user_info,
            "message": "User information retrieved"
        }

    except Exception as e:
        print(f"[ERROR] get_user_info failed: {type(e).__name__}: {e}")

        return {
            "success": False,
            "error": {
                "code": "UNKNOWN_ERROR",
                "message": "Failed to retrieve user information",
                "details": "An unexpected error occurred. Please try again."
            }
        }
