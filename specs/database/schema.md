# Database Schema Specification: Todo Application

**Created**: 2026-01-05
**Status**: Draft
**Related**: See `/specs/api/rest-endpoints.md` for API implementation, `/specs/features/authentication.md` for auth context
**Constitutional Reference**: CONSTITUTION.md § IV (User Isolation and Security), § III (Reusable Intelligence)

## Overview

This specification defines the database schema for the multi-user Todo application backend. The schema must support user-scoped task management with strict data isolation, ensuring no cross-user data access while enabling rich task organization through priorities, tags, due dates, and completion tracking.

## User Scenarios & Testing

### User Story 1 - Store User Tasks Securely (Priority: P1)

As a registered user, the system must persistently store my task data in a way that only I can access it, so that my tasks remain private and secure across sessions.

**Why this priority**: Core data persistence is foundational - without it, no other features function. User isolation prevents data breaches and ensures privacy compliance.

**Independent Test**: Create a test database, insert tasks for two different users, query tasks by user_id, and verify each user sees only their own tasks with zero cross-user data leakage.

**Acceptance Scenarios**:

1. **Given** a user creates a task, **When** the task is saved to the database, **Then** the task must include the user's ID and be retrievable only by queries filtered by that user_id
2. **Given** multiple users have created tasks, **When** querying tasks by user_id, **Then** results contain only tasks belonging to that specific user with no other users' data visible
3. **Given** a task exists in the database, **When** another user attempts to query it directly by task ID without user_id validation, **Then** the system architecture prevents access (enforced by application layer, not just database)

---

### User Story 2 - Organize Tasks with Metadata (Priority: P2)

As a user managing multiple tasks, I need to assign priorities, tags, and due dates to my tasks so that I can organize, filter, and focus on what matters most.

**Why this priority**: After basic storage, metadata enables meaningful task organization and productivity workflows. Users can prioritize work and set deadlines.

**Independent Test**: Insert tasks with various priority levels, multiple tags, and different due dates, then query by each metadata field to verify filtering works correctly.

**Acceptance Scenarios**:

1. **Given** a user creates a task with priority "high", **When** the task is saved, **Then** the priority field stores the value accurately and can be used for sorting and filtering
2. **Given** a user assigns multiple tags ["work", "urgent"] to a task, **When** the task is stored, **Then** tags are preserved as an array/list and can be queried for any tag match
3. **Given** a user sets a due date for a task, **When** the task is saved, **Then** the due_date field stores the datetime value and supports comparison queries (e.g., tasks due before a specific date)

---

### User Story 3 - Track Task Lifecycle (Priority: P2)

As a user, the system must automatically track when I created a task and when I last modified it, so I can understand task history and recency without manual effort.

**Why this priority**: Audit trails and temporal context help users understand task evolution and support future features like "recently updated" views.

**Independent Test**: Create a task, verify created_at is set automatically, update the task, verify updated_at changes to the new timestamp while created_at remains unchanged.

**Acceptance Scenarios**:

1. **Given** a user creates a new task, **When** the task is inserted into the database, **Then** created_at is automatically set to the current timestamp
2. **Given** a user updates an existing task, **When** the update is saved, **Then** updated_at is automatically set to the current timestamp while created_at remains the original value
3. **Given** multiple tasks exist, **When** querying tasks sorted by creation or update time, **Then** results are ordered correctly based on these timestamp fields

---

### Edge Cases

- **Empty or null values**: What happens when optional fields (description, due_date, tags) are not provided? (Expected: Stored as NULL/empty, queries handle gracefully)
- **Very long text**: How does the system handle tasks with extremely long titles (>1000 characters) or descriptions (>10,000 characters)? (Expected: Database column limits enforced, application validates before insert)
- **Invalid priority values**: What happens if a task is created with priority "critical" instead of allowed values? (Expected: Application validates before database insert, or database constraint rejects invalid enum)
- **Tags array limits**: How many tags can a task have? (Assumption: Reasonable limit like 20 tags, enforced at application layer)
- **Due dates in the past**: Can a user create a task with a due_date in the past? (Expected: Yes, allowed for backdated tasks or historical tracking)
- **Concurrent updates**: What happens when two clients update the same task simultaneously? (Expected: Last-write-wins with updated_at reflecting final change; future enhancement could add optimistic locking)
- **User deletion**: What happens to tasks when a user account is deleted? (Expected: Cascade delete or soft delete of user's tasks - to be specified in auth spec)

## Requirements

### Functional Requirements

- **FR-001**: Database MUST store tasks with unique identifiers that enable direct lookup and prevent collisions
- **FR-002**: Database MUST associate every task with exactly one user through a foreign key relationship to enforce user ownership
- **FR-003**: Database MUST support task titles as mandatory text fields and descriptions as optional longer text fields
- **FR-004**: Database MUST track task completion status as a boolean flag (completed: true/false)
- **FR-005**: Database MUST store task priority using predefined values: "high", "medium", "low" with "medium" as the default when not specified
- **FR-006**: Database MUST support multiple tags per task stored as an array or JSON structure to enable flexible categorization
- **FR-007**: Database MUST support optional due dates stored as datetime values to enable temporal task management
- **FR-008**: Database MUST automatically capture task creation timestamps (created_at) without manual input
- **FR-009**: Database MUST automatically update modification timestamps (updated_at) whenever task data changes
- **FR-010**: Database MUST create indexes on user_id, due_date, and completed fields to optimize query performance for common access patterns
- **FR-011**: Database schema MUST be compatible with SQLModel ORM for type-safe Python integration
- **FR-012**: Database MUST prevent deletion or modification of a user referenced by existing tasks (referential integrity via foreign key constraint)

### Key Entities

- **Task**: Represents a single todo item owned by a user
  - Unique identifier (id)
  - Owner reference (user_id) linking to User entity
  - Required title (short description of the task)
  - Optional description (detailed notes about the task)
  - Completion status (boolean flag)
  - Priority level (enum: high, medium, low)
  - Tags (array/list of text labels for categorization)
  - Due date (optional datetime for deadline tracking)
  - Creation timestamp (auto-generated)
  - Update timestamp (auto-maintained)

- **User**: Represents a registered application user (managed by Better Auth, referenced but not defined here)
  - User identifier (referenced by Task.user_id)
  - Authentication credentials (managed externally by Better Auth)
  - Note: Full User schema is outside scope of this spec; this spec only references user_id as a foreign key

## Success Criteria

### Measurable Outcomes

- **SC-001**: Database schema supports insertion and retrieval of 10,000+ tasks per user without performance degradation on indexed queries
- **SC-002**: Query filtering by user_id returns results in under 100ms for datasets up to 100,000 total tasks (demonstrates index effectiveness)
- **SC-003**: Zero cross-user data leakage when executing 1,000 concurrent queries from different users (validates isolation at query level)
- **SC-004**: Schema migration from empty database to full schema completes in under 5 seconds (demonstrates deployment readiness)
- **SC-005**: SQLModel code generation produces type-safe models with zero manual schema adjustments required (validates ORM compatibility)

## Database Schema Definition

### Tasks Table

| Column Name  | Data Type         | Constraints                          | Description                                    |
|--------------|-------------------|--------------------------------------|------------------------------------------------|
| id           | UUID / Integer    | PRIMARY KEY, NOT NULL, AUTO          | Unique task identifier                         |
| user_id      | UUID / String     | FOREIGN KEY (users.id), NOT NULL, INDEXED | Owner of the task (references User table)     |
| title        | VARCHAR(500)      | NOT NULL                             | Task title (required, max 500 characters)      |
| description  | TEXT              | NULL                                 | Optional detailed description                  |
| completed    | BOOLEAN           | NOT NULL, DEFAULT FALSE              | Completion status                              |
| priority     | ENUM / VARCHAR(10)| NOT NULL, DEFAULT 'medium'           | Priority level: 'high', 'medium', 'low'        |
| tags         | JSON / TEXT[]     | NULL                                 | Array of tag strings (e.g., ["work", "urgent"])|
| due_date     | TIMESTAMP         | NULL, INDEXED                        | Optional deadline date/time                    |
| created_at   | TIMESTAMP         | NOT NULL, DEFAULT CURRENT_TIMESTAMP  | Automatic creation timestamp                   |
| updated_at   | TIMESTAMP         | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Automatic update timestamp |

### Indexes

- **idx_tasks_user_id**: Index on `user_id` (supports fast filtering by owner)
- **idx_tasks_due_date**: Index on `due_date` (supports queries for upcoming deadlines)
- **idx_tasks_completed**: Index on `completed` (supports filtering by completion status)
- **idx_tasks_user_completed**: Composite index on `(user_id, completed)` (optimizes common query pattern: user's pending/completed tasks)

### Foreign Key Constraints

- **fk_tasks_user_id**: `tasks.user_id` REFERENCES `users.id`
  - ON DELETE: CASCADE (when user is deleted, their tasks are also deleted)
  - ON UPDATE: CASCADE (if user ID changes, task references update automatically)

### Users Table Reference

The `users` table is managed by Better Auth and is not defined in this specification. For the purposes of this schema, we only need to know:

- The `users` table has a primary key field (likely `id` of type UUID or String)
- Better Auth handles all user creation, authentication, and management
- The `tasks.user_id` foreign key references `users.id`

## SQLModel Examples

### Task Model Definition

```python
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid

class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(max_length=500, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False, nullable=False)
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM, nullable=False)
    tags: Optional[List[str]] = Field(default=None, sa_column_kwargs={"type_": JSON})  # PostgreSQL JSON or ARRAY
    due_date: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow})

    class Config:
        use_enum_values = True  # Store enum as string values in database
```

### Create Table Migration Example

```python
from sqlmodel import create_engine, SQLModel

# Neon PostgreSQL connection string from environment
DATABASE_URL = "postgresql://user:password@ep-example.us-east-2.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create all tables defined in SQLModel metadata"""
    SQLModel.metadata.create_all(engine)

# Indexes are created automatically by SQLModel based on Field(index=True)
# Foreign key constraints are created automatically based on Field(foreign_key=...)
```

### Query Examples (Validating User Isolation)

```python
from sqlmodel import Session, select

# Query all tasks for a specific user (user isolation)
def get_user_tasks(session: Session, user_id: str) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    results = session.exec(statement).all()
    return results

# Query pending tasks for a user (using completed index)
def get_pending_tasks(session: Session, user_id: str) -> List[Task]:
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False
    )
    results = session.exec(statement).all()
    return results

# Query tasks due before a specific date (using due_date index)
def get_tasks_due_before(session: Session, user_id: str, date: datetime) -> List[Task]:
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.due_date < date
    )
    results = session.exec(statement).all()
    return results

# Query tasks by tag (requires JSON containment or array overlap)
def get_tasks_by_tag(session: Session, user_id: str, tag: str) -> List[Task]:
    # PostgreSQL specific: JSON contains or ARRAY overlap
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.tags.contains([tag])  # Adjust based on PostgreSQL JSON/ARRAY syntax
    )
    results = session.exec(statement).all()
    return results
```

## Constitutional Compliance

This specification adheres to the project Constitution:

- **§ IV (User Isolation and Security)**: Foreign key on user_id with indexed queries ensures user-scoped data access; all queries must filter by user_id
- **§ III (Reusable Intelligence)**: Schema designed for backend-builder and auth-specialist subagents to implement without ambiguity
- **§ I (Spec-Driven Development)**: No implementation details beyond SQLModel examples; backend-builder will generate FastAPI integration code
- **Security Requirements**: SQLModel parameterized queries prevent SQL injection by design; user_id validation enforced at application layer (see `/specs/api/rest-endpoints.md`)

## Urdu Translations (Error Messages)

| English Message                          | Urdu Translation (اردو)                          |
|------------------------------------------|-------------------------------------------------|
| "Task not found"                         | "ٹاسک نہیں ملا"                                  |
| "Invalid priority value"                 | "غلط ترجیح کی قیمت"                             |
| "Title is required"                      | "عنوان ضروری ہے"                                |
| "Invalid user ID"                        | "غلط صارف کی شناخت"                             |
| "Database connection failed"             | "ڈیٹا بیس کنکشن ناکام"                          |
| "Task created successfully"              | "ٹاسک کامیابی سے بنایا گیا"                     |
| "Task updated successfully"              | "ٹاسک کامیابی سے اپ ڈیٹ کیا گیا"               |
| "Task deleted successfully"              | "ٹاسک کامیابی سے حذف کیا گیا"                   |

## Assumptions

- User ID format (UUID vs integer) will be determined by Better Auth implementation; schema uses flexible String type
- Tag storage will use PostgreSQL JSON type for flexibility (alternative: TEXT[] array)
- Task ID uses auto-incrementing integer for simplicity; UUID alternative available if needed
- Soft delete not implemented initially (tasks are hard-deleted); can be added later with `deleted_at` field
- No task versioning or history tracking in initial schema; can be added later with audit table
- Maximum 20 tags per task enforced at application layer, not database constraint
- Title limited to 500 characters based on typical todo app usage patterns
- Database timezone stored as UTC; application layer handles user timezone conversion

## Next Steps

1. Use `@backend-builder` to implement FastAPI integration:
   - Database connection to Neon PostgreSQL
   - SQLModel setup and migrations
   - CRUD operations with user isolation
2. Use `@auth-specialist` to integrate JWT validation:
   - Verify user_id from JWT matches query parameters
   - Implement middleware for protected routes
3. Reference `/specs/api/rest-endpoints.md` for HTTP API layer built on this schema
