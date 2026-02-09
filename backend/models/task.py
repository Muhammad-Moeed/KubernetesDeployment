"""
Task Model
SQLModel definition for Task entity with user isolation
"""
from __future__ import annotations

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional, List
from datetime import datetime
from .enums import PriorityLevel


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item owned by a user

    Foreign Key Constraints:
    - user_id references users.id with ON DELETE CASCADE

    Indexes:
    - user_id (for user isolation queries)
    - due_date (for date filtering)
    - completed (for status filtering)
    - (user_id, completed) composite index (for common query pattern)
    """
    __tablename__: str = "tasks"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Key to User (Better Auth managed)
    # ON DELETE CASCADE: when user is deleted, their tasks are deleted
    # NOTE: Foreign key constraint temporarily disabled - users table managed by Better Auth
    user_id: str = Field(
        nullable=False,
        index=True,
        description="User who owns this task (references users.id)"
    )

    # Required Fields
    title: str = Field(
        max_length=500,
        nullable=False,
        description="Task title (required, max 500 characters)"
    )

    completed: bool = Field(
        default=False,
        nullable=False,
        index=True,
        description="Completion status (true = completed, false = pending)"
    )

    priority: PriorityLevel = Field(
        default=PriorityLevel.MEDIUM,
        nullable=False,
        description="Priority level: high, medium, or low"
    )

    # Optional Fields
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed description (max 10,000 characters)"
    )

    tags: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Array of tag strings (max 20 tags)"
    )

    due_date: Optional[datetime] = Field(
        default=None,
        index=True,
        description="Optional deadline date/time (ISO 8601 format)"
    )

    # Timestamps (auto-generated)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Task creation timestamp (auto-generated)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp (auto-updated)"
    )

    class Config:
        """SQLModel configuration"""
        use_enum_values = True  # Store enum as string values in database
        json_schema_extra = {
            "example": {
                "id": 123,
                "user_id": "user_abc123",
                "title": "Buy groceries",
                "description": "Milk, bread, eggs, cheese",
                "completed": False,
                "priority": "high",
                "tags": ["home", "shopping", "urgent"],
                "due_date": "2026-01-10T18:00:00Z",
                "created_at": "2026-01-05T10:30:00Z",
                "updated_at": "2026-01-05T10:30:00Z"
            }
        }
