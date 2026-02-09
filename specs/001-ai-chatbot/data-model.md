# Data Model: AI Todo Chatbot Integration

**Feature**: AI Todo Chatbot Integration
**Branch**: `001-ai-chatbot`
**Date**: 2026-02-09

## Overview

This document defines the database entities, relationships, and validation rules for the Phase 3 AI chatbot feature. The data model extends the existing Phase 2 schema with new tables for conversation management while maintaining compatibility with existing Task and User entities.

## Entity Relationship Diagram

```
┌─────────────────┐
│     User        │ (Existing from Phase 2)
│─────────────────│
│ id (PK)         │
│ email           │
│ name            │
│ password_hash   │
│ created_at      │
└─────────────────┘
        │
        │ 1:N
        ├──────────────────────────────────┐
        │                                  │
        ▼                                  ▼
┌─────────────────┐              ┌─────────────────┐
│  Conversation   │              │      Task       │ (Existing from Phase 2)
│─────────────────│              │─────────────────│
│ id (PK)         │              │ id (PK)         │
│ user_id (FK)    │              │ user_id (FK)    │
│ created_at      │              │ title           │
│ last_activity_at│              │ description     │
└─────────────────┘              │ status          │
        │                        │ priority        │
        │ 1:N                    │ due_date        │
        │                        │ created_at      │
        ▼                        │ updated_at      │
┌─────────────────┐              └─────────────────┘
│  ChatMessage    │
│─────────────────│
│ id (PK)         │
│ conversation_id │
│ user_id (FK)    │
│ sender          │
│ message_text    │
│ created_at      │
│ metadata        │
└─────────────────┘
```

## Entities

### 1. User (Existing from Phase 2)

**Purpose**: Represents an authenticated user account

**Attributes**:
- `id` (Integer, Primary Key): Unique user identifier
- `email` (String, Unique, Not Null): User's email address
- `name` (String, Not Null): User's display name
- `password_hash` (String, Not Null): Hashed password
- `created_at` (DateTime, Not Null): Account creation timestamp

**Relationships**:
- One-to-Many with Task (one user has many tasks)
- One-to-Many with Conversation (one user has many conversations)
- One-to-Many with ChatMessage (one user has many messages)

**Validation Rules**:
- Email must be valid format and unique
- Name must be 1-100 characters
- Password must be hashed (never stored plain text)

**Indexes**:
- Primary key on `id`
- Unique index on `email`

**Notes**: This entity is not modified in Phase 3. It's referenced here for completeness.

---

### 2. Task (Existing from Phase 2)

**Purpose**: Represents a todo item in the user's task list

**Attributes**:
- `id` (Integer, Primary Key): Unique task identifier
- `user_id` (Integer, Foreign Key → User.id, Not Null): Owner of the task
- `title` (String, Not Null): Task title (max 200 characters)
- `description` (Text, Nullable): Detailed task description (max 1000 characters)
- `status` (Enum, Not Null): Task status - "pending", "in_progress", "completed"
- `priority` (Enum, Not Null): Task priority - "low", "medium", "high"
- `due_date` (Date, Nullable): Optional due date
- `created_at` (DateTime, Not Null): Task creation timestamp
- `updated_at` (DateTime, Not Null): Last update timestamp

**Relationships**:
- Many-to-One with User (many tasks belong to one user)

**Validation Rules**:
- Title must be 1-200 characters
- Description max 1000 characters
- Status must be one of: pending, in_progress, completed
- Priority must be one of: low, medium, high
- Due date must be in the future (if provided)
- User_id must reference existing user

**Indexes**:
- Primary key on `id`
- Index on `user_id` for user-scoped queries
- Index on `status` for filtering
- Index on `created_at` for sorting

**State Transitions**:
- pending → in_progress → completed
- Any status → pending (reset)
- completed → pending (reopen)

**Notes**: This entity is not modified in Phase 3. MCP tools will interact with this table through existing Phase 2 API endpoints.

---

### 3. Conversation (NEW for Phase 3)

**Purpose**: Represents a chat session between a user and the AI chatbot

**Attributes**:
- `id` (UUID, Primary Key): Unique conversation identifier
- `user_id` (Integer, Foreign Key → User.id, Not Null): Owner of the conversation
- `created_at` (DateTime, Not Null): Conversation start timestamp
- `last_activity_at` (DateTime, Not Null): Last message timestamp

**Relationships**:
- Many-to-One with User (many conversations belong to one user)
- One-to-Many with ChatMessage (one conversation has many messages)

**Validation Rules**:
- User_id must reference existing user
- Created_at must be <= last_activity_at
- Last_activity_at updated on every new message

**Indexes**:
- Primary key on `id`
- Index on `user_id` for user-scoped queries
- Index on `last_activity_at` for sorting by recency

**Business Logic**:
- New conversation created on first chat message from user
- Conversation ID persisted in frontend local storage
- Conversation remains active indefinitely (no auto-expiration)
- Future enhancement: Add conversation title, archived flag

**Default Values**:
- `id`: Generated UUID v4
- `created_at`: Current timestamp
- `last_activity_at`: Current timestamp

---

### 4. ChatMessage (NEW for Phase 3)

**Purpose**: Represents a single message in a conversation (user or bot)

**Attributes**:
- `id` (UUID, Primary Key): Unique message identifier
- `conversation_id` (UUID, Foreign Key → Conversation.id, Not Null): Parent conversation
- `user_id` (Integer, Foreign Key → User.id, Not Null): Owner of the conversation
- `sender` (Enum, Not Null): Message sender - "user" or "bot"
- `message_text` (Text, Not Null): Message content (max 1000 characters)
- `created_at` (DateTime, Not Null): Message timestamp
- `metadata` (JSONB, Nullable): Optional metadata (intent, tool results, etc.)

**Relationships**:
- Many-to-One with Conversation (many messages belong to one conversation)
- Many-to-One with User (many messages belong to one user)

**Validation Rules**:
- Conversation_id must reference existing conversation
- User_id must reference existing user
- User_id must match conversation's user_id (enforce ownership)
- Sender must be "user" or "bot"
- Message_text must be 1-1000 characters
- Created_at must be >= conversation.created_at

**Indexes**:
- Primary key on `id`
- Index on `conversation_id` for message retrieval
- Index on `user_id` for user isolation enforcement
- Index on `created_at` for chronological ordering
- Composite index on `(conversation_id, created_at)` for efficient history queries

**Metadata Structure** (Optional JSONB):
```json
{
  "intent": "add_task",
  "tool_name": "add_task",
  "tool_parameters": {"title": "buy milk", "priority": "medium"},
  "tool_result": {"success": true, "task_id": 123},
  "language": "en",
  "is_rtl": false
}
```

**Business Logic**:
- User messages created when user sends chat input
- Bot messages created after LLM generates response
- Messages are immutable (no editing or deletion)
- Conversation history limited to 100 most recent messages in queries
- Metadata used for debugging and analytics (not displayed to user)

**Default Values**:
- `id`: Generated UUID v4
- `created_at`: Current timestamp
- `metadata`: null (optional)

---

## Database Constraints

### Foreign Key Constraints

```sql
-- Conversation references User
ALTER TABLE conversations
ADD CONSTRAINT fk_conversation_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;

-- ChatMessage references Conversation
ALTER TABLE chat_messages
ADD CONSTRAINT fk_message_conversation
FOREIGN KEY (conversation_id) REFERENCES conversations(id)
ON DELETE CASCADE;

-- ChatMessage references User
ALTER TABLE chat_messages
ADD CONSTRAINT fk_message_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

### Check Constraints

```sql
-- ChatMessage sender must be 'user' or 'bot'
ALTER TABLE chat_messages
ADD CONSTRAINT chk_sender
CHECK (sender IN ('user', 'bot'));

-- ChatMessage text length
ALTER TABLE chat_messages
ADD CONSTRAINT chk_message_length
CHECK (LENGTH(message_text) >= 1 AND LENGTH(message_text) <= 1000);

-- Conversation timestamps
ALTER TABLE conversations
ADD CONSTRAINT chk_conversation_timestamps
CHECK (last_activity_at >= created_at);
```

### Unique Constraints

No additional unique constraints beyond primary keys.

---

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_activity_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["ChatMessage"] = Relationship(back_populates="conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": 123,
                "created_at": "2026-02-09T10:00:00Z",
                "last_activity_at": "2026-02-09T10:30:00Z"
            }
        }
```

### ChatMessage Model

```python
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any
from enum import Enum

class MessageSender(str, Enum):
    USER = "user"
    BOT = "bot"

class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    sender: MessageSender = Field(nullable=False)
    message_text: str = Field(nullable=False, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship(back_populates="chat_messages")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440001",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": 123,
                "sender": "user",
                "message_text": "Add a task to buy milk",
                "created_at": "2026-02-09T10:30:00Z",
                "metadata": {
                    "intent": "add_task",
                    "language": "en"
                }
            }
        }
```

---

## Query Patterns

### Get Recent Conversation History

```python
def get_conversation_history(
    db: Session,
    conversation_id: UUID,
    user_id: int,
    limit: int = 100
) -> List[ChatMessage]:
    """Retrieve recent messages for a conversation"""
    return db.query(ChatMessage)\
        .filter(ChatMessage.conversation_id == conversation_id)\
        .filter(ChatMessage.user_id == user_id)\
        .order_by(ChatMessage.created_at.desc())\
        .limit(limit)\
        .all()
```

### Create New Message

```python
def create_message(
    db: Session,
    conversation_id: UUID,
    user_id: int,
    sender: MessageSender,
    message_text: str,
    metadata: Optional[Dict] = None
) -> ChatMessage:
    """Create a new chat message"""
    message = ChatMessage(
        conversation_id=conversation_id,
        user_id=user_id,
        sender=sender,
        message_text=message_text,
        metadata=metadata
    )
    db.add(message)

    # Update conversation last_activity_at
    conversation = db.query(Conversation)\
        .filter(Conversation.id == conversation_id)\
        .first()
    if conversation:
        conversation.last_activity_at = datetime.utcnow()

    db.commit()
    db.refresh(message)
    return message
```

### Get or Create Conversation

```python
def get_or_create_conversation(
    db: Session,
    conversation_id: Optional[UUID],
    user_id: int
) -> Conversation:
    """Get existing conversation or create new one"""
    if conversation_id:
        conversation = db.query(Conversation)\
            .filter(Conversation.id == conversation_id)\
            .filter(Conversation.user_id == user_id)\
            .first()
        if conversation:
            return conversation

    # Create new conversation
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation
```

---

## Migration Strategy

### Alembic Migration Script

```python
"""Add chat tables for Phase 3

Revision ID: add_chat_tables
Revises: previous_migration
Create Date: 2026-02-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_activity_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint('last_activity_at >= created_at', name='chk_conversation_timestamps')
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('ix_conversations_last_activity', 'conversations', ['last_activity_at'])

    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('sender', sa.String(10), nullable=False),
        sa.Column('message_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('metadata', JSONB, nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("sender IN ('user', 'bot')", name='chk_sender'),
        sa.CheckConstraint("LENGTH(message_text) >= 1 AND LENGTH(message_text) <= 1000", name='chk_message_length')
    )
    op.create_index('ix_chat_messages_conversation_id', 'chat_messages', ['conversation_id'])
    op.create_index('ix_chat_messages_user_id', 'chat_messages', ['user_id'])
    op.create_index('ix_chat_messages_created_at', 'chat_messages', ['created_at'])
    op.create_index('ix_chat_messages_conversation_created', 'chat_messages', ['conversation_id', 'created_at'])

def downgrade():
    op.drop_table('chat_messages')
    op.drop_table('conversations')
```

---

## Data Integrity Rules

### User Isolation

- All queries MUST filter by user_id from JWT token
- ChatMessage.user_id MUST match Conversation.user_id
- No cross-user data access permitted

### Cascade Deletes

- Deleting a User cascades to Conversations and ChatMessages
- Deleting a Conversation cascades to ChatMessages
- Tasks are independent (not affected by chat deletion)

### Immutability

- Messages cannot be edited after creation
- Messages cannot be deleted individually (only via conversation deletion)
- Conversation metadata can be updated (last_activity_at)

---

## Performance Considerations

### Indexing Strategy

- Index on user_id for all user-scoped queries
- Index on conversation_id for message retrieval
- Composite index on (conversation_id, created_at) for history queries
- Index on last_activity_at for sorting conversations by recency

### Query Optimization

- Limit conversation history to 100 messages
- Use pagination for large result sets (future enhancement)
- Avoid N+1 queries with eager loading (Relationship)

### Storage Estimates

- Average message: ~200 bytes (text) + ~100 bytes (metadata) = 300 bytes
- 100 messages per conversation: 30 KB
- 1000 users × 10 conversations × 100 messages = 300 MB
- Negligible storage impact for expected scale

---

## Future Enhancements

### Conversation Metadata

- Add `title` field (auto-generated from first message)
- Add `archived` flag for hiding old conversations
- Add `tags` array for categorization

### Message Features

- Add `edited_at` timestamp for message editing
- Add `deleted_at` for soft deletion
- Add `reactions` JSONB for emoji reactions

### Analytics

- Add `message_count` to Conversation for quick stats
- Add `avg_response_time` for bot performance tracking
- Add `intent_distribution` for usage analytics

---

## Summary

The Phase 3 data model adds two new tables (Conversation, ChatMessage) while maintaining full compatibility with existing Phase 2 entities (User, Task). The design enforces user isolation at the database level, supports efficient querying with proper indexes, and provides flexibility for future enhancements through JSONB metadata fields.
