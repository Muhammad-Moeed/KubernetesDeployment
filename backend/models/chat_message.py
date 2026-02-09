"""
ChatMessage Model
SQLModel definition for ChatMessage entity (Phase 3 AI Chatbot)
"""
from __future__ import annotations

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any
from enum import Enum


class MessageSender(str, Enum):
    """Enum for message sender type"""
    USER = "user"
    BOT = "bot"


class ChatMessage(SQLModel, table=True):
    """
    ChatMessage entity representing a single message in a conversation

    Foreign Key Constraints:
    - conversation_id references conversations.id with ON DELETE CASCADE
    - user_id references users.id with ON DELETE CASCADE

    Indexes:
    - conversation_id (for message retrieval)
    - user_id (for user isolation)
    - created_at (for chronological ordering)
    - (conversation_id, created_at) composite index (for efficient history queries)
    """
    __tablename__: str = "chat_messages"

    # Primary Key
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Foreign Keys
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True,
        description="Parent conversation ID"
    )

    user_id: str = Field(
        nullable=False,
        index=True,
        description="User who owns this message (references users.id)"
    )

    # Message Content
    sender: MessageSender = Field(
        nullable=False,
        description="Message sender: 'user' or 'bot'"
    )

    message_text: str = Field(
        nullable=False,
        max_length=1000,
        description="Message content (max 1000 characters)"
    )

    # Timestamp
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Message timestamp (auto-generated)"
    )

    # Optional Metadata (JSONB) - renamed to avoid SQLModel reserved attribute
    message_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Optional metadata (intent, tool results, language, etc.)"
    )

    class Config:
        """SQLModel configuration"""
        use_enum_values = True  # Store enum as string values in database
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440001",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "user_abc123",
                "sender": "user",
                "message_text": "Add a task to buy milk",
                "created_at": "2026-02-09T10:30:00Z",
                "message_metadata": {
                    "intent": "add_task",
                    "language": "en"
                }
            }
        }
