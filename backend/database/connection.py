"""
Database Connection Module
SQLModel engine setup and session management for Neon PostgreSQL
"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLModel engine
# Neon PostgreSQL requires SSL mode
# echo=True enables SQL query logging (set to False in production)
engine = create_engine(
    DATABASE_URL,
    echo=True if os.getenv("ENVIRONMENT") == "development" else False,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Connection pool size
    max_overflow=10  # Max additional connections beyond pool_size
)


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel metadata.
    Should be called once during application startup or in initialization script.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function to get database session for FastAPI routes.

    Usage in FastAPI routes:
        @router.get("/tasks")
        def get_tasks(session: Session = Depends(get_session)):
            # Use session here
            pass

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session


def get_db_session() -> Session:
    """
    Get a database session for manual use (non-FastAPI contexts).
    Caller is responsible for closing the session.

    Returns:
        Session: SQLModel database session
    """
    return Session(engine)
