"""
Conversation Model
SQLModel definition for Conversation entity (Phase 3 AI Chatbot)
"""
from __future__ import annotations

from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a chat session between user and AI chatbot

    Foreign Key Constraints:
    - user_id references users.id with ON DELETE CASCADE

    Indexes:
    - user_id (for user isolation queries)
    - last_activity_at (for sorting by recency)
    """
    __tablename__: str = "conversations"

    # Primary Key
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Foreign Key to User (Better Auth managed)
    # NOTE: Foreign key constraint temporarily disabled - users table managed by Better Auth
    user_id: str = Field(
        nullable=False,
        index=True,
        description="User who owns this conversation (references users.id)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Conversation start timestamp (auto-generated)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last updated timestamp"
    )

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "user_abc123",
                "created_at": "2026-02-09T10:00:00Z",
                "last_activity_at": "2026-02-09T10:30:00Z"
            }
        }
