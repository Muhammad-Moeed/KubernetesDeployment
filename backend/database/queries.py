"""
Database Query Helper Functions
CRUD operations and filtering logic for Task model with user isolation
"""
from sqlmodel import Session, select, or_, and_, func
from typing import List, Optional
from datetime import datetime
from models.task import Task
from models.enums import PriorityLevel


def get_user_tasks(
    session: Session,
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    due_before: Optional[datetime] = None,
    sort: str = "created_at",
    order: str = "desc"
) -> List[Task]:
    """
    Get all tasks for a user with optional filtering and sorting.

    User Isolation: ALWAYS filters by user_id to prevent cross-user data access.

    Args:
        session: Database session
        user_id: User ID (from JWT token)
        status: Filter by status: "all", "pending", "completed" (optional)
        priority: Filter by priority: "high", "medium", "low" (optional)
        tag: Filter by tag (tasks containing this tag) (optional)
        search: Search keyword in title or description (case-insensitive) (optional)
        due_before: Filter tasks due before this date (optional)
        sort: Sort field: "due_date", "priority", "created_at" (default: "created_at")
        order: Sort order: "asc", "desc" (default: "desc")

    Returns:
        List of Task objects matching the filters
    """
    # Base query: ALWAYS filter by user_id (USER ISOLATION)
    statement = select(Task).where(Task.user_id == user_id)

    # Filter by completion status
    if status and status != "all":
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)

    # Filter by priority
    if priority:
        try:
            priority_enum = PriorityLevel(priority.lower())
            statement = statement.where(Task.priority == priority_enum)
        except ValueError:
            # Invalid priority value, ignore filter
            pass

    # Filter by tag (JSON containment)
    if tag:
        # PostgreSQL JSON containment: check if tags array contains the specified tag
        statement = statement.where(Task.tags.contains([tag]))

    # Search in title or description (case-insensitive)
    if search and search.strip():
        search_pattern = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )

    # Filter by due_before date
    if due_before:
        statement = statement.where(Task.due_date < due_before)

    # Sorting
    sort_column = Task.created_at  # Default sort column

    if sort == "due_date":
        sort_column = Task.due_date
    elif sort == "priority":
        # Priority sorting: high > medium > low
        # Use CASE statement to map enum to numeric values
        priority_order = func.case(
            (Task.priority == PriorityLevel.HIGH, 3),
            (Task.priority == PriorityLevel.MEDIUM, 2),
            (Task.priority == PriorityLevel.LOW, 1),
            else_=0
        )
        if order == "asc":
            statement = statement.order_by(priority_order.asc())
        else:
            statement = statement.order_by(priority_order.desc())
        # Execute and return early since we already applied sorting
        results = session.exec(statement).all()
        return list(results)
    elif sort == "created_at":
        sort_column = Task.created_at

    # Apply order (ascending or descending)
    if order == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    # Execute query
    results = session.exec(statement).all()
    return list(results)


def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a single task by ID with user isolation.

    User Isolation: Returns task ONLY if it belongs to the specified user.
    Returns None if task doesn't exist or belongs to different user.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (from JWT token)

    Returns:
        Task object if found and belongs to user, None otherwise
    """
    statement = select(Task).where(
        and_(
            Task.id == task_id,
            Task.user_id == user_id  # USER ISOLATION
        )
    )
    result = session.exec(statement).first()
    return result


def create_task(session: Session, task: Task) -> Task:
    """
    Create a new task in the database.

    Args:
        session: Database session
        task: Task object with all fields populated (except id)

    Returns:
        Created Task object with auto-generated id and timestamps
    """
    # Set updated_at to match created_at on creation
    task.updated_at = task.created_at

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(
    session: Session,
    task_id: int,
    user_id: str,
    update_data: dict
) -> Optional[Task]:
    """
    Update an existing task with user isolation.

    User Isolation: Updates task ONLY if it belongs to the specified user.
    Returns None if task doesn't exist or belongs to different user.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (from JWT token)
        update_data: Dictionary of fields to update

    Returns:
        Updated Task object if found and updated, None otherwise
    """
    # Get task with user isolation
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Update fields
    for key, value in update_data.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def toggle_task_completion(
    session: Session,
    task_id: int,
    user_id: str
) -> Optional[Task]:
    """
    Toggle task completion status (true ↔ false) with user isolation.

    User Isolation: Toggles task ONLY if it belongs to the specified user.
    Returns None if task doesn't exist or belongs to different user.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (from JWT token)

    Returns:
        Updated Task object with toggled completed status, None if not found
    """
    # Get task with user isolation
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task with user isolation.

    User Isolation: Deletes task ONLY if it belongs to the specified user.
    Returns False if task doesn't exist or belongs to different user.

    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID (from JWT token)

    Returns:
        True if task was deleted, False if not found or unauthorized
    """
    # Get task with user isolation
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def count_user_tasks(session: Session, user_id: str) -> int:
    """
    Count total tasks for a user.

    Args:
        session: Database session
        user_id: User ID (from JWT token)

    Returns:
        Total number of tasks for the user
    """
    statement = select(func.count(Task.id)).where(Task.user_id == user_id)
    result = session.exec(statement).one()
    return result


def count_pending_tasks(session: Session, user_id: str) -> int:
    """
    Count pending (not completed) tasks for a user.

    Args:
        session: Database session
        user_id: User ID (from JWT token)

    Returns:
        Number of pending tasks for the user
    """
    statement = select(func.count(Task.id)).where(
        and_(
            Task.user_id == user_id,
            Task.completed == False
        )
    )
    result = session.exec(statement).one()
    return result


def count_completed_tasks(session: Session, user_id: str) -> int:
    """
    Count completed tasks for a user.

    Args:
        session: Database session
        user_id: User ID (from JWT token)

    Returns:
        Number of completed tasks for the user
    """
    statement = select(func.count(Task.id)).where(
        and_(
            Task.user_id == user_id,
            Task.completed == True
        )
    )
    result = session.exec(statement).one()
    return result
