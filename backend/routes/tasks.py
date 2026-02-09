"""
Task Routes
FastAPI routes for task CRUD operations with user isolation
All routes require JWT authentication and enforce user-scoped access
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime

from database.connection import get_session
from database import queries
from models.task import Task
from models.schemas import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    ErrorResponse,
    URDU_TRANSLATIONS
)
from middleware.auth import verify_jwt_token, AuthenticatedUser

# Create router
router = APIRouter()


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user"
)
async def create_task(
    user_id: str,
    task_data: TaskCreateRequest,
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task.

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only create tasks for themselves (user_id must match JWT)

    **Request Body**:
    - title: Required, 1-500 characters
    - description: Optional, max 10,000 characters
    - priority: Optional, one of "high", "medium", "low" (default: "medium")
    - tags: Optional, array of strings, max 20 tags
    - due_date: Optional, ISO 8601 datetime

    **Response**: 201 Created with task object
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only create tasks for yourself"
            }
        )

    # Create Task object
    task = Task(
        user_id=user.user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        tags=task_data.tags,
        due_date=task_data.due_date,
        completed=False  # New tasks are always pending
    )

    # Save to database
    created_task = queries.create_task(session, task)

    return TaskResponse.model_validate(created_task)


@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskResponse],
    summary="List all tasks",
    description="Get all tasks for the authenticated user with optional filtering and sorting"
)
async def list_tasks(
    user_id: str,
    status_filter: Optional[str] = Query(
        None,
        alias="status",
        description="Filter by status: all, pending, completed"
    ),
    priority: Optional[str] = Query(
        None,
        description="Filter by priority: high, medium, low"
    ),
    tag: Optional[str] = Query(
        None,
        description="Filter by tag (tasks containing this tag)"
    ),
    search: Optional[str] = Query(
        None,
        description="Search keyword in title or description"
    ),
    due_before: Optional[str] = Query(
        None,
        description="Filter tasks due before this date (YYYY-MM-DD or ISO 8601)"
    ),
    sort: str = Query(
        "created_at",
        description="Sort field: due_date, priority, created_at"
    ),
    order: str = Query(
        "desc",
        description="Sort order: asc, desc"
    ),
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only access their own tasks

    **Query Parameters**:
    - status: Filter by completion status (all, pending, completed)
    - priority: Filter by priority level (high, medium, low)
    - tag: Filter by tag (returns tasks containing this tag)
    - search: Search keyword in title or description (case-insensitive)
    - due_before: Filter tasks due before this date
    - sort: Sort field (due_date, priority, created_at)
    - order: Sort order (asc, desc)

    **Response**: 200 OK with array of task objects
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only access your own tasks"
            }
        )

    # Parse due_before date if provided
    due_before_date = None
    if due_before:
        try:
            # Try parsing as YYYY-MM-DD first
            due_before_date = datetime.fromisoformat(due_before)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid date format",
                    "error_urdu": URDU_TRANSLATIONS.get("Invalid date format"),
                    "detail": "Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) or YYYY-MM-DD"
                }
            )

    # Get tasks from database with filters
    tasks = queries.get_user_tasks(
        session=session,
        user_id=user.user_id,
        status=status_filter,
        priority=priority,
        tag=tag,
        search=search,
        due_before=due_before_date,
        sort=sort,
        order=order
    )

    return [TaskResponse.model_validate(task) for task in tasks]


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a single task",
    description="Get a specific task by ID"
)
async def get_task(
    user_id: str,
    task_id: int,
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Get a single task by ID.

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only access their own tasks

    **Response**: 200 OK with task object, or 404 Not Found
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only access your own tasks"
            }
        )

    # Get task from database (with user isolation)
    task = queries.get_task_by_id(session, task_id, user.user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Task not found",
                "error_urdu": URDU_TRANSLATIONS.get("Task not found"),
                "detail": f"No task with ID {task_id} exists for this user"
            }
        )

    return TaskResponse.model_validate(task)


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task (full or partial update)"
)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdateRequest,
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only update their own tasks

    **Request Body**: All fields optional (partial update supported)
    - title: 1-500 characters
    - description: Max 10,000 characters
    - priority: One of "high", "medium", "low"
    - tags: Array of strings, max 20 tags
    - due_date: ISO 8601 datetime
    - completed: Boolean

    **Response**: 200 OK with updated task object, or 404 Not Found
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only update your own tasks"
            }
        )

    # Prepare update data (exclude None values for partial update)
    update_data = task_data.model_dump(exclude_unset=True)

    # Update task in database (with user isolation)
    updated_task = queries.update_task(session, task_id, user.user_id, update_data)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Task not found",
                "error_urdu": URDU_TRANSLATIONS.get("Task not found"),
                "detail": f"No task with ID {task_id} exists for this user"
            }
        )

    return TaskResponse.model_validate(updated_task)


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    summary="Toggle task completion",
    description="Toggle the completed status of a task (true ↔ false)"
)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only toggle their own tasks

    **Behavior**: Toggles completed field (true → false, false → true)

    **Response**: 200 OK with updated task object, or 404 Not Found
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only modify your own tasks"
            }
        )

    # Toggle completion status (with user isolation)
    updated_task = queries.toggle_task_completion(session, task_id, user.user_id)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Task not found",
                "error_urdu": URDU_TRANSLATIONS.get("Task not found"),
                "detail": f"No task with ID {task_id} exists for this user"
            }
        )

    return TaskResponse.model_validate(updated_task)


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently delete a task"
)
async def delete_task(
    user_id: str,
    task_id: int,
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only delete their own tasks

    **Behavior**: Permanently removes task from database (hard delete)

    **Response**: 204 No Content on success, or 404 Not Found
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only delete your own tasks"
            }
        )

    # Delete task from database (with user isolation)
    deleted = queries.delete_task(session, task_id, user.user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Task not found",
                "error_urdu": URDU_TRANSLATIONS.get("Task not found"),
                "detail": f"No task with ID {task_id} exists for this user"
            }
        )

    # Return 204 No Content (no response body)
    return None
