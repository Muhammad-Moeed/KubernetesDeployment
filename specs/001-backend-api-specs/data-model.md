# Data Model: Backend API

**Feature**: Backend API Specifications
**Created**: 2026-01-05
**Status**: Complete
**Source**: Derived from `/specs/database/schema.md`

---

## Overview

This document defines the data entities, relationships, validation rules, and state transitions for the backend API. It serves as the bridge between the database schema and API implementation.

---

## Entity Definitions

### 1. Task Entity

**Purpose**: Represents a single todo item owned by a user

**Fields:**

| Field Name   | Type             | Required | Default Value     | Validation Rules                                         |
|--------------|------------------|----------|-------------------|----------------------------------------------------------|
| id           | Integer          | Yes*     | Auto-generated    | Unique, primary key, auto-increment                      |
| user_id      | String           | Yes      | -                 | Non-empty, references User.id                            |
| title        | String           | Yes      | -                 | Non-empty, max 500 characters                            |
| description  | String           | No       | null              | Max 10,000 characters                                    |
| completed    | Boolean          | Yes      | false             | true or false                                            |
| priority     | Enum<Priority>   | Yes      | "medium"          | One of: "high", "medium", "low"                          |
| tags         | Array<String>    | No       | null              | Each tag max 50 characters, max 20 tags                  |
| due_date     | DateTime         | No       | null              | ISO 8601 format, can be past date                        |
| created_at   | DateTime         | Yes      | Current timestamp | ISO 8601 format, auto-generated                          |
| updated_at   | DateTime         | Yes      | Current timestamp | ISO 8601 format, auto-updated on modification            |

*Auto-generated on creation, not required in request body

**Validation Rules:**

1. **Title Validation:**
   - MUST NOT be empty string
   - MUST NOT be only whitespace
   - MUST be ≤500 characters
   - Trimmed before storage (leading/trailing whitespace removed)

2. **Description Validation:**
   - Optional (can be null or omitted)
   - If provided, MUST be ≤10,000 characters
   - Trimmed before storage

3. **Priority Validation:**
   - MUST be one of: "high", "medium", "low" (case-insensitive)
   - Defaults to "medium" if not provided
   - Invalid values → 400 Bad Request

4. **Tags Validation:**
   - Optional (can be null, empty array, or omitted)
   - If provided as array, each tag:
     - MUST be string
     - MUST NOT be empty
     - MUST be ≤50 characters
     - Trimmed before storage
   - Maximum 20 tags per task
   - Duplicate tags automatically deduplicated
   - Empty tags filtered out

5. **Due Date Validation:**
   - Optional (can be null or omitted)
   - If provided, MUST be valid ISO 8601 datetime string
   - Past dates allowed (for backdated tasks)
   - Timezone: Stored in UTC, converted from user timezone in frontend

6. **User ID Validation:**
   - MUST match authenticated user's ID from JWT token
   - MUST reference existing user in users table (foreign key constraint)
   - Empty or null → 400 Bad Request

---

### 2. User Entity (Reference Only)

**Purpose**: Represents a registered application user

**Note**: Users table is managed by Better Auth. Backend only references user_id as foreign key.

**Referenced Fields:**

| Field Name | Type   | Description                  |
|------------|--------|------------------------------|
| id         | String | Unique user identifier (PK)  |

**Backend Responsibilities:**
- Validate user_id from JWT matches path parameter
- Reference users.id in tasks.user_id foreign key
- Query user's tasks by filtering on user_id

**Not in Backend Scope:**
- User creation (handled by Better Auth)
- User authentication (handled by Better Auth)
- Password hashing (handled by Better Auth)
- User profile management (handled by Better Auth)

---

## Entity Relationships

```
┌─────────────┐
│   User      │
│  (Better    │
│   Auth      │
│  Managed)   │
└──────┬──────┘
       │
       │ 1
       │
       │ owns
       │
       │ 0..*
       │
┌──────▼──────┐
│   Task      │
│             │
│ - id        │
│ - user_id   │ (Foreign Key → User.id)
│ - title     │
│ - ...       │
└─────────────┘
```

**Relationship Rules:**

1. **User → Task (One-to-Many)**
   - One user can have zero or more tasks
   - Each task belongs to exactly one user
   - Foreign key: `tasks.user_id` REFERENCES `users.id`

2. **Referential Integrity:**
   - ON DELETE CASCADE: When user deleted, all their tasks are deleted
   - ON UPDATE CASCADE: If user.id changes (unlikely), tasks.user_id updates automatically

3. **Query Isolation:**
   - ALL task queries MUST filter by user_id
   - Backend NEVER returns tasks from different users in same response
   - Path parameter {user_id} MUST match JWT token user_id

---

## Validation Rules Summary

### Create Task (POST)

**Required Fields:**
- title (string, 1-500 chars)

**Optional Fields:**
- description (string, max 10,000 chars)
- priority (enum: "high"/"medium"/"low", default "medium")
- tags (array of strings, max 20, each max 50 chars)
- due_date (ISO 8601 datetime string)

**Auto-Generated Fields:**
- id (integer, auto-increment)
- user_id (from JWT token)
- completed (boolean, default false)
- created_at (datetime, current timestamp)
- updated_at (datetime, current timestamp)

**Validation Errors:**
- Missing title → 400 "Title is required"
- Empty title → 400 "Title cannot be empty"
- Title >500 chars → 400 "Title must be 500 characters or less"
- Invalid priority → 400 "Priority must be: high, medium, or low"
- Invalid due_date format → 400 "Invalid date format, use ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)"
- Too many tags → 400 "Maximum 20 tags allowed"
- Tag too long → 400 "Each tag must be 50 characters or less"

---

### Update Task (PUT)

**All Fields Optional** (partial update supported):
- title (string, 1-500 chars)
- description (string, max 10,000 chars)
- priority (enum: "high"/"medium"/"low")
- tags (array of strings)
- due_date (ISO 8601 datetime string)
- completed (boolean)

**Immutable Fields:**
- id (cannot be changed)
- user_id (cannot be changed)
- created_at (cannot be changed)

**Auto-Updated Fields:**
- updated_at (automatically set to current timestamp)

**Validation Errors:**
- Same as Create Task for provided fields
- Cannot update non-existent task → 404 "Task not found"
- Cannot update another user's task → 404 "Task not found" (don't reveal existence)

---

### Toggle Completion (PATCH /tasks/{task_id}/complete)

**No Request Body Required**

**Behavior:**
- Reads current `completed` value
- Toggles: true → false, false → true
- Updates `updated_at` to current timestamp

**Validation Errors:**
- Task not found → 404 "Task not found"
- Task belongs to different user → 404 "Task not found"

---

### Delete Task (DELETE)

**No Request Body Required**

**Behavior:**
- Permanently deletes task from database
- No soft delete (no `deleted_at` field)

**Validation Errors:**
- Task not found → 404 "Task not found"
- Task belongs to different user → 404 "Task not found"

---

## State Transitions

### Task Completion Lifecycle

```
┌──────────────┐
│  Created     │ (completed = false)
│  (Pending)   │
└───────┬──────┘
        │
        │ PATCH /complete
        ▼
┌──────────────┐
│  Completed   │ (completed = true)
└───────┬──────┘
        │
        │ PATCH /complete
        ▼
┌──────────────┐
│  Pending     │ (completed = false)
└──────────────┘
```

**States:**
- **Pending** (completed = false): Default state on creation, task not yet done
- **Completed** (completed = true): Task marked as done

**Transitions:**
- **Complete**: PATCH /tasks/{id}/complete when pending → completed = true
- **Uncomplete**: PATCH /tasks/{id}/complete when completed → completed = false

**No Terminal State:** Tasks can be toggled indefinitely between pending and completed.

---

## Database Indexes

Indexes optimize query performance for common access patterns:

| Index Name                | Columns             | Purpose                                          |
|---------------------------|---------------------|--------------------------------------------------|
| pk_tasks_id               | id                  | Primary key, unique lookup                       |
| idx_tasks_user_id         | user_id             | Fast user isolation queries                      |
| idx_tasks_due_date        | due_date            | Filter by due date, sort by due date             |
| idx_tasks_completed       | completed           | Filter by completion status                      |
| idx_tasks_user_completed  | (user_id, completed)| Combined filter: user's pending/completed tasks  |

**Query Optimization:**
- `GET /api/{user_id}/tasks` → Uses idx_tasks_user_id
- `GET /api/{user_id}/tasks?status=pending` → Uses idx_tasks_user_completed
- `GET /api/{user_id}/tasks?due_before=2026-02-01` → Uses idx_tasks_due_date
- `GET /api/{user_id}/tasks?status=pending&priority=high` → Composite index on (user_id, completed) + filter priority in application

---

## API Request/Response Models

### CreateTaskRequest (POST /tasks)

```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs, cheese",
  "priority": "high",
  "tags": ["home", "shopping", "urgent"],
  "due_date": "2026-01-10T18:00:00Z"
}
```

**Pydantic Model:**
```python
class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=10000)
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    tags: Optional[List[str]] = Field(None, max_items=20)
    due_date: Optional[datetime] = None
```

---

### UpdateTaskRequest (PUT /tasks/{id})

```json
{
  "title": "Buy groceries (updated)",
  "completed": true
}
```

**Pydantic Model:**
```python
class UpdateTaskRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=10000)
    priority: Optional[PriorityLevel] = None
    tags: Optional[List[str]] = Field(None, max_items=20)
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
```

---

### TaskResponse (All endpoints)

```json
{
  "id": 123,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs, cheese",
  "completed": false,
  "priority": "high",
  "tags": ["home", "shopping", "urgent"],
  "due_date": "2026-01-10T18:00:00Z",
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T10:30:00Z"
}
```

**Pydantic Model:**
```python
class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str  # "high", "medium", or "low"
    tags: Optional[List[str]]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allow creation from SQLModel objects
```

---

## Error Response Model

```json
{
  "error": "Task not found",
  "detail": "No task with ID 999 exists for this user"
}
```

**Pydantic Model:**
```python
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
```

---

## Business Rules

1. **User Isolation (Security)**
   - Every task MUST have a user_id
   - All queries MUST filter by authenticated user's ID
   - Users CANNOT access other users' tasks under any circumstances
   - 404 returned for tasks that exist but belong to different user (don't reveal existence)

2. **Task Ownership (Immutability)**
   - Task ownership (user_id) CANNOT be changed after creation
   - Tasks CANNOT be transferred between users
   - If task transfer needed in future, implement via copy-and-delete

3. **Priority Defaults**
   - If priority not specified on creation → default to "medium"
   - Priority is always one of three values (enum enforced)

4. **Tag Management**
   - Tags are case-sensitive ("Work" ≠ "work")
   - Duplicate tags within same task automatically removed
   - Empty strings filtered out from tags array
   - No tag taxonomy or validation (users can create any tags)

5. **Date Handling**
   - All dates stored in UTC in database
   - Frontend responsible for timezone conversion
   - Past due dates allowed (for backdated tasks or completed overdue tasks)
   - No automatic "overdue" status (frontend calculates based on due_date < now)

6. **Completion Semantics**
   - Completed tasks remain in database (no auto-deletion)
   - Completed tasks still editable (user can modify completed tasks)
   - Completing a task does NOT change due_date or priority

7. **Deletion Policy**
   - Hard delete (permanent removal from database)
   - No soft delete or recycle bin in MVP
   - Deleted tasks cannot be recovered
   - Future: Add `deleted_at` field for soft delete if needed

---

## Data Integrity Constraints

1. **Foreign Key Constraint**
   - `tasks.user_id` REFERENCES `users.id`
   - ON DELETE CASCADE (delete tasks when user deleted)
   - ON UPDATE CASCADE (update tasks.user_id if users.id changes)

2. **Primary Key Constraint**
   - `tasks.id` is unique and non-null
   - Auto-incrementing integer

3. **Not Null Constraints**
   - user_id MUST NOT be null
   - title MUST NOT be null
   - completed MUST NOT be null
   - priority MUST NOT be null
   - created_at MUST NOT be null
   - updated_at MUST NOT be null

4. **Check Constraints** (Optional, can be added)
   - `LENGTH(title) BETWEEN 1 AND 500`
   - `LENGTH(description) <= 10000`
   - `priority IN ('high', 'medium', 'low')`
   - `array_length(tags, 1) <= 20`

---

## Query Patterns

### 1. Get User's Tasks (Basic)
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
ORDER BY created_at DESC;
```

### 2. Filter by Status (Pending)
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND completed = false
ORDER BY created_at DESC;
```

### 3. Filter by Priority
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND priority = 'high'
ORDER BY created_at DESC;
```

### 4. Search in Title/Description
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND (
    title ILIKE '%meeting%'
    OR description ILIKE '%meeting%'
  )
ORDER BY created_at DESC;
```

### 5. Filter by Tag (JSON containment)
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND tags @> '["work"]'::jsonb
ORDER BY created_at DESC;
```

### 6. Filter by Due Before Date
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND due_date < :target_date
ORDER BY due_date ASC;
```

### 7. Combined Filters (Pending, High Priority, Work Tag)
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND completed = false
  AND priority = 'high'
  AND tags @> '["work"]'::jsonb
ORDER BY due_date ASC;
```

---

## Performance Considerations

1. **Index Usage**
   - Always filter by user_id first (uses index)
   - Additional filters (completed, priority) applied after user_id filter
   - Due date filtering uses idx_tasks_due_date for range queries

2. **Query Complexity**
   - Multiple filters → O(log n) lookup via indexes + O(k) filter, where k = user's task count
   - Search (ILIKE) → Full text scan within user's tasks (acceptable for <1,000 tasks)
   - Tag filtering → JSON containment operator (GIN index recommended for large datasets)

3. **Scaling Strategy**
   - Indexes sufficient for MVP (<10,000 tasks per user)
   - Future: Full-text search index for better search performance
   - Future: Separate tags table with GIN index for advanced tag queries

---

## Constitutional Compliance

This data model adheres to CONSTITUTION.md principles:

- **§ IV (User Isolation)**: User_id foreign key enforces ownership, all queries filter by user_id
- **§ III (Reusable Intelligence)**: Designed for backend-builder subagent implementation
- **§ I (Spec-Driven)**: Derived directly from database schema spec
- **Security Requirements**: SQL injection prevention via SQLModel, user_id validation enforced

---

## Next Steps

1. Use @backend-builder to implement SQLModel models based on this data model
2. Create Pydantic request/response models for API validation
3. Implement database migrations (create tables, indexes, foreign keys)
4. Write query functions for all filter combinations
5. Add unit tests for validation rules

---

**Data model complete. Ready for API contract generation (OpenAPI schema).**
