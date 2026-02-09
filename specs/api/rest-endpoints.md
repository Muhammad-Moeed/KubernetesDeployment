# REST API Endpoints Specification: Todo Application

**Created**: 2026-01-05
**Status**: Draft
**Related**: See `/specs/database/schema.md` for data models, `/specs/features/authentication.md` for auth requirements
**Constitutional Reference**: CONSTITUTION.md § IV (User Isolation and Security), § III (Reusable Intelligence)

## Overview

This specification defines the RESTful HTTP API for the multi-user Todo application backend. All endpoints enforce strict user isolation through JWT authentication, ensuring users can only access and modify their own tasks. The API follows the `/api/{user_id}/tasks` pattern with comprehensive filtering, sorting, and search capabilities.

## User Scenarios & Testing

### User Story 1 - Create and Retrieve Tasks via API (Priority: P1)

As an authenticated user, I must be able to create new tasks through an API call and retrieve my task list, so that I can manage my todos programmatically from any client application.

**Why this priority**: Core API functionality - without create and list operations, the application has no basic utility.

**Independent Test**: Authenticate as a user, POST a new task with title "Test Task", then GET the task list and verify the created task appears with correct data and user_id matching the authenticated user.

**Acceptance Scenarios**:

1. **Given** an authenticated user with valid JWT token, **When** they POST to `/api/{user_id}/tasks` with title "Buy groceries", **Then** the API returns 201 Created with the new task object including auto-generated ID, created_at timestamp, and user_id matching the path parameter
2. **Given** a user has created 5 tasks, **When** they GET `/api/{user_id}/tasks`, **Then** the API returns 200 OK with a JSON array containing all 5 tasks sorted by creation date (newest first by default)
3. **Given** User A and User B each have created tasks, **When** User A requests `/api/{user_id_A}/tasks`, **Then** the response contains only User A's tasks with zero visibility into User B's data

---

### User Story 2 - Update and Delete Tasks (Priority: P1)

As an authenticated user, I must be able to update task details and delete tasks I no longer need, so that I can maintain an accurate and current task list.

**Why this priority**: Essential CRUD operations - users must be able to modify and remove tasks to maintain data accuracy.

**Independent Test**: Create a task, update its title via PUT, verify the change persists, mark it complete via PATCH, then DELETE it and verify it no longer appears in the task list.

**Acceptance Scenarios**:

1. **Given** a user owns task with ID 123, **When** they PUT to `/api/{user_id}/tasks/123` with updated title "Updated Task", **Then** the API returns 200 OK with the updated task object and updated_at timestamp is newer than created_at
2. **Given** a user owns an incomplete task with ID 456, **When** they PATCH to `/api/{user_id}/tasks/456/complete`, **Then** the API toggles completed status to true and returns 200 OK with the updated task
3. **Given** a user owns task with ID 789, **When** they DELETE `/api/{user_id}/tasks/789`, **Then** the API returns 204 No Content and subsequent GET requests for that task return 404 Not Found

---

### User Story 3 - Filter and Search Tasks (Priority: P2)

As a user with many tasks, I need to filter by status, priority, tags, and search by keywords, so that I can quickly find relevant tasks without scrolling through my entire list.

**Why this priority**: Power-user feature enabling productivity at scale - critical for users managing 50+ tasks.

**Independent Test**: Create 20 tasks with various priorities, tags, and due dates, then test each query parameter combination (status=pending, priority=high, tag=work, search=urgent, due_before=2026-02-01) to verify correct filtering.

**Acceptance Scenarios**:

1. **Given** a user has 10 completed and 5 pending tasks, **When** they GET `/api/{user_id}/tasks?status=pending`, **Then** the API returns only the 5 pending tasks (completed=false)
2. **Given** a user has tasks with priorities [high: 3, medium: 5, low: 2], **When** they GET `/api/{user_id}/tasks?priority=high`, **Then** the API returns only the 3 high-priority tasks
3. **Given** a user has tasks tagged with ["work", "home", "urgent"], **When** they GET `/api/{user_id}/tasks?tag=work`, **Then** the API returns only tasks where tags array contains "work"
4. **Given** a user has tasks with titles and descriptions containing various keywords, **When** they GET `/api/{user_id}/tasks?search=meeting`, **Then** the API returns tasks where title OR description contains "meeting" (case-insensitive)
5. **Given** a user has tasks with due dates ranging from 2026-01-10 to 2026-03-15, **When** they GET `/api/{user_id}/tasks?due_before=2026-02-01`, **Then** the API returns only tasks with due_date before February 1st, 2026

---

### User Story 4 - Sort Task Results (Priority: P3)

As a user viewing my task list, I need to sort by due date, priority, or creation date in ascending or descending order, so that I can organize my view based on what matters most to me at any given time.

**Why this priority**: Nice-to-have UI enhancement - improves user experience but not critical for MVP functionality.

**Independent Test**: Create tasks with different due dates, priorities, and creation timestamps, then request sorted results (sort=due_date&order=asc, sort=priority&order=desc) and verify correct ordering.

**Acceptance Scenarios**:

1. **Given** a user has tasks with due dates [2026-01-15, 2026-01-10, 2026-01-20], **When** they GET `/api/{user_id}/tasks?sort=due_date&order=asc`, **Then** tasks are returned in order [Jan 10, Jan 15, Jan 20]
2. **Given** a user has tasks with priorities [low, high, medium, high], **When** they GET `/api/{user_id}/tasks?sort=priority&order=desc`, **Then** tasks are returned grouped [high, high, medium, low]
3. **Given** a user has tasks created at timestamps [T1, T2, T3] where T1 < T2 < T3, **When** they GET `/api/{user_id}/tasks?sort=created_at&order=desc`, **Then** tasks are returned in reverse chronological order [T3, T2, T1]

---

### Edge Cases

- **Invalid user_id in path**: What happens when user_id in URL doesn't match JWT user_id? (Expected: 403 Forbidden - see `/specs/features/authentication.md`)
- **Missing required fields**: What if POST /tasks omits the required "title" field? (Expected: 400 Bad Request with error message "Title is required")
- **Very long title**: What if title exceeds 500 characters? (Expected: 400 Bad Request with error message "Title must be 500 characters or less")
- **Invalid priority value**: What if POST /tasks includes priority="critical"? (Expected: 400 Bad Request with error message "Priority must be: high, medium, or low")
- **Invalid date format**: What if due_before query parameter is "tomorrow" instead of ISO date? (Expected: 400 Bad Request with error message "Invalid date format, use YYYY-MM-DD")
- **Task not found**: What if GET /tasks/999999 requests a non-existent task? (Expected: 404 Not Found)
- **Task belongs to different user**: What if user A tries to update user B's task? (Expected: 404 Not Found - don't reveal task exists for other user)
- **Empty search query**: What if search parameter is empty string? (Expected: Ignore search filter, return all tasks)
- **Multiple query parameters**: Can user combine filters like `?status=pending&priority=high&tag=work`? (Expected: Yes, AND logic - tasks must match ALL criteria)
- **Pagination**: How many tasks returned in one request? (Assumption: Return all tasks initially; pagination can be added later with ?limit=50&offset=100)
- **Concurrent modifications**: What if two clients update the same task simultaneously? (Expected: Last-write-wins with updated_at reflecting final state)

## Requirements

### Functional Requirements

- **FR-001**: API MUST expose endpoints at base path `/api/{user_id}/tasks` where {user_id} is a path parameter
- **FR-002**: All endpoints MUST require JWT authentication via Authorization: Bearer {token} header
- **FR-003**: API MUST validate that user_id in URL path matches the authenticated user ID extracted from JWT token
- **FR-004**: API MUST return 401 Unauthorized when JWT token is missing, invalid, or expired
- **FR-005**: API MUST return 403 Forbidden when authenticated user_id does not match path user_id
- **FR-006**: POST /tasks endpoint MUST accept JSON body with title (required) and optional fields: description, priority, tags, due_date
- **FR-007**: POST /tasks endpoint MUST return 201 Created with complete task object including auto-generated id, user_id, created_at, updated_at
- **FR-008**: GET /tasks endpoint MUST return 200 OK with JSON array of all user's tasks by default
- **FR-009**: GET /tasks endpoint MUST support query parameters: status, priority, tag, search, sort, due_before
- **FR-010**: GET /tasks/{task_id} endpoint MUST return 200 OK with single task object when task exists and belongs to authenticated user
- **FR-011**: GET /tasks/{task_id} endpoint MUST return 404 Not Found when task doesn't exist or belongs to different user
- **FR-012**: PUT /tasks/{task_id} endpoint MUST accept JSON body with updated fields and return 200 OK with updated task object
- **FR-013**: PUT /tasks/{task_id} endpoint MUST update the updated_at timestamp automatically
- **FR-014**: PATCH /tasks/{task_id}/complete endpoint MUST toggle the completed boolean field and return 200 OK
- **FR-015**: DELETE /tasks/{task_id} endpoint MUST permanently delete the task and return 204 No Content
- **FR-016**: API MUST validate input data and return 400 Bad Request with descriptive error messages for invalid requests
- **FR-017**: API MUST return proper HTTP status codes: 200 (success), 201 (created), 204 (no content), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 500 (server error)
- **FR-018**: API MUST return all responses in JSON format with consistent structure
- **FR-019**: API MUST support CORS headers to allow requests from the frontend origin (configured via environment variable)
- **FR-020**: API MUST log all requests and errors for debugging and audit purposes

### Key Entities

- **TaskCreateRequest**: Request body for POST /tasks
  - title (string, required, max 500 chars)
  - description (string, optional)
  - priority (enum: "high" | "medium" | "low", optional, default "medium")
  - tags (array of strings, optional)
  - due_date (ISO 8601 datetime string, optional)

- **TaskUpdateRequest**: Request body for PUT /tasks/{task_id}
  - title (string, optional, max 500 chars)
  - description (string, optional)
  - priority (enum: "high" | "medium" | "low", optional)
  - tags (array of strings, optional)
  - due_date (ISO 8601 datetime string, optional)
  - completed (boolean, optional)

- **TaskResponse**: Response object for all task operations
  - id (integer)
  - user_id (string)
  - title (string)
  - description (string | null)
  - completed (boolean)
  - priority (string: "high" | "medium" | "low")
  - tags (array of strings | null)
  - due_date (ISO 8601 datetime string | null)
  - created_at (ISO 8601 datetime string)
  - updated_at (ISO 8601 datetime string)

- **ErrorResponse**: Response object for error cases
  - error (string: error message)
  - detail (string: optional detailed explanation)

## Success Criteria

### Measurable Outcomes

- **SC-001**: API handles 100 concurrent authenticated requests without errors or timeout
- **SC-002**: All endpoints respond in under 200ms for datasets up to 1,000 tasks per user (95th percentile)
- **SC-003**: Zero cross-user data leakage when testing with 1,000 malicious requests attempting to access other users' tasks
- **SC-004**: 100% of invalid requests (missing required fields, invalid data types, malformed JSON) return appropriate 400 Bad Request responses with actionable error messages
- **SC-005**: API documentation (generated from OpenAPI spec) allows frontend developers to integrate without backend team assistance

## API Endpoint Definitions

### Base URL

```
/api/{user_id}/tasks
```

**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID, must match JWT token user_id

**Authentication:**
- All endpoints require: `Authorization: Bearer {jwt_token}`

### Endpoint 1: Create Task

**POST** `/api/{user_id}/tasks`

Creates a new task for the authenticated user.

**Request Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "priority": "high",
  "tags": ["home", "shopping"],
  "due_date": "2026-01-10T18:00:00Z"
}
```

**Request Body Schema:**
| Field       | Type     | Required | Description                                    |
|-------------|----------|----------|------------------------------------------------|
| title       | string   | Yes      | Task title (max 500 characters)                |
| description | string   | No       | Detailed description                           |
| priority    | string   | No       | One of: "high", "medium", "low" (default: "medium") |
| tags        | string[] | No       | Array of tag strings                           |
| due_date    | string   | No       | ISO 8601 datetime (e.g., "2026-01-10T18:00:00Z") |

**Success Response (201 Created):**
```json
{
  "id": 123,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false,
  "priority": "high",
  "tags": ["home", "shopping"],
  "due_date": "2026-01-10T18:00:00Z",
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T10:30:00Z"
}
```

**Error Responses:**
- **400 Bad Request**: Missing title, invalid priority, invalid date format
  ```json
  {"error": "Title is required"}
  ```
- **401 Unauthorized**: Missing or invalid JWT token
  ```json
  {"error": "Authentication required"}
  ```
- **403 Forbidden**: JWT user_id doesn't match path user_id
  ```json
  {"error": "Access denied"}
  ```

---

### Endpoint 2: List Tasks (with filtering)

**GET** `/api/{user_id}/tasks`

Retrieves all tasks for the authenticated user with optional filtering, searching, and sorting.

**Request Headers:**
```
Authorization: Bearer {jwt_token}
```

**Query Parameters:**

| Parameter   | Type   | Required | Description                                                      |
|-------------|--------|----------|------------------------------------------------------------------|
| status      | string | No       | Filter by completion: "all" (default), "pending", "completed"    |
| priority    | string | No       | Filter by priority: "high", "medium", "low"                      |
| tag         | string | No       | Filter by tag (tasks containing this tag)                        |
| search      | string | No       | Search keyword in title or description (case-insensitive)        |
| sort        | string | No       | Sort field: "due_date", "priority", "created_at" (default)       |
| order       | string | No       | Sort order: "asc", "desc" (default)                              |
| due_before  | string | No       | Filter tasks due before this date (YYYY-MM-DD format)            |

**Example Requests:**
```
GET /api/user123/tasks
GET /api/user123/tasks?status=pending
GET /api/user123/tasks?priority=high&status=pending
GET /api/user123/tasks?tag=work
GET /api/user123/tasks?search=meeting
GET /api/user123/tasks?sort=due_date&order=asc
GET /api/user123/tasks?due_before=2026-02-01
GET /api/user123/tasks?status=pending&priority=high&tag=work&sort=due_date&order=asc
```

**Success Response (200 OK):**
```json
[
  {
    "id": 123,
    "user_id": "user123",
    "title": "Prepare presentation",
    "description": "Q4 results review",
    "completed": false,
    "priority": "high",
    "tags": ["work", "urgent"],
    "due_date": "2026-01-08T14:00:00Z",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z"
  },
  {
    "id": 124,
    "user_id": "user123",
    "title": "Buy groceries",
    "description": null,
    "completed": false,
    "priority": "medium",
    "tags": ["home"],
    "due_date": null,
    "created_at": "2026-01-05T10:30:00Z",
    "updated_at": "2026-01-05T10:30:00Z"
  }
]
```

**Error Responses:**
- **400 Bad Request**: Invalid query parameter value
  ```json
  {"error": "Invalid priority value. Must be: high, medium, or low"}
  ```
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: JWT user_id doesn't match path user_id

---

### Endpoint 3: Get Single Task

**GET** `/api/{user_id}/tasks/{task_id}`

Retrieves a specific task by ID (only if it belongs to the authenticated user).

**Request Headers:**
```
Authorization: Bearer {jwt_token}
```

**Path Parameters:**
- `task_id` (integer, required): The task ID

**Success Response (200 OK):**
```json
{
  "id": 123,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false,
  "priority": "high",
  "tags": ["home", "shopping"],
  "due_date": "2026-01-10T18:00:00Z",
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T10:30:00Z"
}
```

**Error Responses:**
- **404 Not Found**: Task doesn't exist or belongs to different user
  ```json
  {"error": "Task not found"}
  ```
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: JWT user_id doesn't match path user_id

---

### Endpoint 4: Update Task

**PUT** `/api/{user_id}/tasks/{task_id}`

Updates an existing task (full or partial update).

**Request Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Path Parameters:**
- `task_id` (integer, required): The task ID

**Request Body:**
```json
{
  "title": "Buy groceries (updated)",
  "description": "Milk, bread, eggs, cheese",
  "priority": "medium",
  "tags": ["home", "shopping", "urgent"],
  "due_date": "2026-01-11T18:00:00Z",
  "completed": false
}
```

**Request Body Schema** (all fields optional for partial update):
| Field       | Type     | Required | Description                                    |
|-------------|----------|----------|------------------------------------------------|
| title       | string   | No       | Updated task title (max 500 characters)        |
| description | string   | No       | Updated description                            |
| priority    | string   | No       | One of: "high", "medium", "low"                |
| tags        | string[] | No       | Updated array of tag strings                   |
| due_date    | string   | No       | ISO 8601 datetime                              |
| completed   | boolean  | No       | Updated completion status                      |

**Success Response (200 OK):**
```json
{
  "id": 123,
  "user_id": "user_abc123",
  "title": "Buy groceries (updated)",
  "description": "Milk, bread, eggs, cheese",
  "completed": false,
  "priority": "medium",
  "tags": ["home", "shopping", "urgent"],
  "due_date": "2026-01-11T18:00:00Z",
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T15:45:00Z"
}
```

**Error Responses:**
- **400 Bad Request**: Invalid data (empty title, invalid priority, malformed date)
- **404 Not Found**: Task doesn't exist or belongs to different user
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: JWT user_id doesn't match path user_id

---

### Endpoint 5: Toggle Task Completion

**PATCH** `/api/{user_id}/tasks/{task_id}/complete`

Toggles the completed status of a task (true ↔ false).

**Request Headers:**
```
Authorization: Bearer {jwt_token}
```

**Path Parameters:**
- `task_id` (integer, required): The task ID

**Success Response (200 OK):**
```json
{
  "id": 123,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": true,
  "priority": "high",
  "tags": ["home", "shopping"],
  "due_date": "2026-01-10T18:00:00Z",
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T16:00:00Z"
}
```

**Error Responses:**
- **404 Not Found**: Task doesn't exist or belongs to different user
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: JWT user_id doesn't match path user_id

---

### Endpoint 6: Delete Task

**DELETE** `/api/{user_id}/tasks/{task_id}`

Permanently deletes a task.

**Request Headers:**
```
Authorization: Bearer {jwt_token}
```

**Path Parameters:**
- `task_id` (integer, required): The task ID

**Success Response (204 No Content):**
```
(empty response body)
```

**Error Responses:**
- **404 Not Found**: Task doesn't exist or belongs to different user
  ```json
  {"error": "Task not found"}
  ```
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: JWT user_id doesn't match path user_id

---

## HTTP Status Codes Summary

| Status Code        | Usage                                                            |
|--------------------|------------------------------------------------------------------|
| 200 OK             | Successful GET, PUT, PATCH operations                            |
| 201 Created        | Successful POST operation (task created)                         |
| 204 No Content     | Successful DELETE operation                                      |
| 400 Bad Request    | Invalid input data, missing required fields, malformed JSON      |
| 401 Unauthorized   | Missing, invalid, or expired JWT token                           |
| 403 Forbidden      | Valid JWT but user_id mismatch (accessing another user's resource) |
| 404 Not Found      | Task doesn't exist or doesn't belong to authenticated user       |
| 500 Server Error   | Unexpected server error (database connection failure, etc.)      |

## CORS Configuration

The API must support Cross-Origin Resource Sharing (CORS) to allow the Next.js frontend to make requests from a different origin.

**Required CORS Headers:**
```
Access-Control-Allow-Origin: {FRONTEND_URL}
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 86400
```

**Configuration:**
- `FRONTEND_URL` environment variable specifies allowed origin (e.g., `http://localhost:3000` for development, `https://todo.vercel.app` for production)
- Preflight OPTIONS requests must return 204 No Content with appropriate CORS headers

## Constitutional Compliance

This specification adheres to the project Constitution:

- **§ IV (User Isolation and Security)**: All endpoints enforce user_id validation against JWT token; 403 Forbidden prevents cross-user access
- **§ III (Reusable Intelligence)**: Designed for backend-builder subagent to implement FastAPI routes with Pydantic models
- **§ I (Spec-Driven Development)**: Technology-agnostic specification focusing on HTTP semantics, not FastAPI implementation details
- **Security Requirements**: JWT validation on every request; SQL injection prevention via SQLModel (see `/specs/database/schema.md`); CORS restricts to authorized frontend origin

## Urdu Translations (Error Messages & Responses)

| English Message                          | Urdu Translation (اردو)                          |
|------------------------------------------|-------------------------------------------------|
| "Title is required"                      | "عنوان ضروری ہے"                                |
| "Invalid priority value"                 | "غلط ترجیح کی قیمت"                             |
| "Invalid date format"                    | "غلط تاریخ کی شکل"                              |
| "Task not found"                         | "ٹاسک نہیں ملا"                                  |
| "Authentication required"                | "تصدیق ضروری ہے"                                |
| "Access denied"                          | "رسائی مسترد"                                    |
| "Task created successfully"              | "ٹاسک کامیابی سے بنایا گیا"                     |
| "Task updated successfully"              | "ٹاسک کامیابی سے اپ ڈیٹ کیا گیا"               |
| "Task deleted successfully"              | "ٹاسک کامیابی سے حذف کیا گیا"                   |
| "Server error"                           | "سرور کی خرابی"                                 |
| "Invalid request"                        | "غلط درخواست"                                   |

## Assumptions

- Pagination not implemented initially (all user tasks returned); can be added later with `?limit` and `?offset` parameters
- Default sort order is `created_at` descending (newest first)
- Search performs case-insensitive substring match on both title and description fields (OR logic)
- Multiple query parameters use AND logic (e.g., `?status=pending&priority=high` returns tasks that are both pending AND high priority)
- Task updates are full-object replacements (PUT), not field-level patches; omitted fields set to null/default
- Concurrent updates use last-write-wins strategy (no optimistic locking initially)
- Rate limiting not specified (can be added later with middleware)
- API versioning not included (can be added later with `/api/v1/` prefix)
- Response pagination metadata (total count, page info) not included initially

## Next Steps

1. Use `@backend-builder` to implement FastAPI routes:
   - Define Pydantic request/response models
   - Implement route handlers with SQLModel database queries
   - Add input validation and error handling
   - Configure CORS middleware
2. Use `@auth-specialist` to implement JWT middleware:
   - Extract user_id from JWT token
   - Validate user_id matches path parameter
   - Return 401/403 errors appropriately
3. Reference `/specs/features/authentication.md` for JWT validation details
4. Reference `/specs/database/schema.md` for SQLModel integration
