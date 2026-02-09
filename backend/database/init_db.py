"""
Database Initialization Script
Creates all database tables and indexes based on SQLModel definitions
"""
from sqlmodel import SQLModel
from sqlalchemy import Index
from .connection import engine
from models.task import Task  # Import all models to register with SQLModel metadata
from models.conversation import Conversation  # Phase 3: AI Chatbot
from models.chat_message import ChatMessage  # Phase 3: AI Chatbot


def create_indexes():
    """
    Create database indexes for performance optimization.

    Indexes created:
    - idx_tasks_user_id: Fast user isolation queries
    - idx_tasks_due_date: Filter by due date, sort by due date
    - idx_tasks_completed: Filter by completion status
    - idx_tasks_user_completed: Combined filter for user's pending/completed tasks
    - idx_chat_messages_conversation_created: Efficient conversation history queries (Phase 3)
    """
    # Indexes are automatically created by SQLModel based on Field(index=True)
    # Composite indexes need to be defined explicitly

    # Create composite index on (user_id, completed) for common query pattern
    idx_user_completed = Index(
        'idx_tasks_user_completed',
        Task.user_id,
        Task.completed
    )

    # Phase 3: Create composite index on (conversation_id, created_at) for chat history
    idx_chat_conversation_created = Index(
        'idx_chat_messages_conversation_created',
        ChatMessage.conversation_id,
        ChatMessage.created_at
    )

    try:
        # Create the composite indexes
        idx_user_completed.create(engine, checkfirst=True)
        print("[OK] Composite index 'idx_tasks_user_completed' created successfully")

        idx_chat_conversation_created.create(engine, checkfirst=True)
        print("[OK] Composite index 'idx_chat_messages_conversation_created' created successfully")
    except Exception as e:
        print(f"Warning: Could not create composite indexes: {e}")


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel metadata.

    This function:
    1. Creates all tables based on SQLModel class definitions
    2. Creates all indexes (both single-column and composite)
    3. Establishes foreign key constraints

    Should be called once during application startup.
    """
    try:
        print("Creating database tables...")

        # Create all tables
        SQLModel.metadata.create_all(engine)
        print("[OK] Database tables created successfully")

        # Create additional indexes
        create_indexes()
        print("[OK] Database indexes created successfully")

        print("[OK] Database initialization complete")

    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        raise


def drop_all_tables():
    """
    Drop all database tables.

    WARNING: This will delete all data!
    Use only for development/testing purposes.
    """
    print("WARNING: Dropping all database tables...")
    SQLModel.metadata.drop_all(engine)
    print("[OK] All tables dropped")


if __name__ == "__main__":
    """
    Run this script directly to initialize the database:
    python -m database.init_db
    """
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        confirm = input("Are you sure you want to drop all tables? (yes/no): ")
        if confirm.lower() == "yes":
            drop_all_tables()
        else:
            print("Operation cancelled")
    else:
        create_db_and_tables()
