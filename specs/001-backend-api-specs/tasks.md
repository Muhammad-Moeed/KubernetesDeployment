# Implementation Tasks: Backend API Specifications

**Feature**: Backend API for Multi-User Todo Application
**Branch**: `001-backend-api-specs`
**Created**: 2026-01-05
**Tech Stack**: Python FastAPI, SQLModel, Neon PostgreSQL, python-jose (JWT)
**Total Tasks**: 45

---

## Task Summary

| Phase | User Story | Tasks | Can Run in Parallel |
|-------|------------|-------|---------------------|
| Setup | - | 5 | 0 |
| Foundational | - | 8 | 5 |
| P1: Database Storage | US1 (Database) | 4 | 2 |
| P1: JWT Authentication | US1-US3 (Auth) | 6 | 2 |
| P1: Basic CRUD API | US1-US2 (API) | 9 | 4 |
| P2: Advanced Filtering | US3 (API) | 6 | 3 |
| P3: Sorting | US4 (API) | 3 | 0 |
| Polish | - | 4 | 2 |

**MVP Scope**: Complete through Phase "P1: Basic CRUD API" (32 tasks) for working backend with authentication and basic task management.

---

## Phase 1: Setup

**Goal**: Initialize backend project structure and environment configuration

**Prerequisites**: None

**Completion Criteria**:
- Backend directory exists with proper structure
- Dependencies installed and verified
- Environment variables documented
- Database connection tested

### Tasks

- [ ] T001 Create backend directory structure at /backend with subdirectories: /models, /routes, /middleware, /database, /config
- [ ] T002 Initialize Python project in /backend with pyproject.toml or requirements.txt
- [ ] T003 [P] Install core dependencies: fastapi, uvicorn, sqlmodel, python-jose[cryptography], passlib, python-multipart in /backend
- [ ] T004 Create environment configuration file /backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL, JWT_TOKEN_EXPIRY_HOURS
- [ ] T005 Create main application file /backend/main.py with FastAPI app initialization and CORS middleware configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Establish database connection, models, and JWT utilities that all user stories depend on

**Prerequisites**: Phase 1 complete

**Completion Criteria**:
- Database connection established to Neon PostgreSQL
- Base SQLModel models defined with type safety
- JWT verification utility functions working
- Pydantic request/response models defined

### Tasks

- [ ] T006 Create database connection module /backend/database/connection.py with SQLModel engine setup and session management for Neon PostgreSQL
- [ ] T007 [P] Define PriorityLevel enum in /backend/models/enums.py with values HIGH="high", MEDIUM="medium", LOW="low"
- [ ] T008 [P] Create base Task SQLModel in /backend/models/task.py with all fields per data-model.md (id, user_id, title, description, completed, priority, tags, due_date, created_at, updated_at)
- [ ] T009 [P] Create Pydantic request models in /backend/models/schemas.py: CreateTaskRequest, UpdateTaskRequest with validation rules
- [ ] T010 [P] Create Pydantic response models in /backend/models/schemas.py: TaskResponse, ErrorResponse with orm_mode=True
- [ ] T011 Create JWT utility functions in /backend/middleware/jwt_utils.py: decode_token(), extract_user_id(), with python-jose
- [ ] T012 Create database initialization script /backend/database/init_db.py to run SQLModel.metadata.create_all() for table creation
- [ ] T013 Test database connection and table creation by running init_db.py script and verifying tasks table exists in Neon dashboard

---

## Phase 3: P1 - Database Storage (User Story 1 - Database)

**User Story**: Store User Tasks Securely
**Priority**: P1 (Critical)
**Goal**: Persistently store task data with strict user isolation via foreign keys and indexes

**Independent Test**: Create test database, insert tasks for two users, query by user_id, verify zero cross-user data leakage

**Prerequisites**: Phase 2 complete

**Completion Criteria**:
- Tasks table created with all columns and constraints
- Foreign key constraint on user_id referencing users.id
- Indexes created on user_id, due_date, completed
- User isolation verified through test queries

### Tasks

- [ ] T014 [P] [US1] Add foreign key constraint to Task model: user_id references users.id with ON DELETE CASCADE in /backend/models/task.py
- [ ] T015 [P] [US1] Create database indexes in /backend/database/init_db.py: idx_tasks_user_id, idx_tasks_due_date, idx_tasks_completed, idx_tasks_user_completed
- [ ] T016 [US1] Create database query helper functions in /backend/database/queries.py: get_user_tasks(user_id), get_task_by_id(task_id, user_id) with user isolation filtering
- [ ] T017 [US1] Write manual test script /backend/tests/test_user_isolation.py to verify user A cannot access user B's tasks

---

## Phase 4: P1 - JWT Authentication (User Stories 1-3 - Authentication)

**User Stories**:
- US1: Register and Login via Frontend (P1)
- US2: Backend Validates JWT Tokens (P1)
- US3: User Identity Validation (P1)

**Goal**: Implement JWT verification middleware to enforce authentication and user isolation on all protected endpoints

**Independent Test**: Make API requests with no token (401), invalid token (401), valid token with mismatched user_id (403), valid matching token (200)

**Prerequisites**: Phase 2 complete

**Completion Criteria**:
- JWT verification middleware functional
- User_id extracted from JWT payload
- Path parameter user_id validated against JWT user_id
- 401/403 errors returned correctly

### Tasks

- [ ] T018 [US1-3] Create JWT verification middleware in /backend/middleware/auth.py: verify_jwt_middleware() function
- [ ] T019 [US1-3] Implement Authorization header parsing in verify_jwt_middleware(): extract "Bearer {token}" from request headers
- [ ] T020 [P] [US2] Implement JWT signature verification in verify_jwt_middleware() using python-jose and BETTER_AUTH_SECRET from environment
- [ ] T021 [P] [US2] Implement JWT expiration check in verify_jwt_middleware(): validate exp claim and return 401 if expired
- [ ] T022 [US3] Implement user_id extraction from JWT payload in verify_jwt_middleware(): get "user_id" or "sub" claim
- [ ] T023 [US3] Implement path parameter validation in verify_jwt_middleware(): compare JWT user_id with URL path {user_id}, return 403 if mismatch

---

## Phase 5: P1 - Basic CRUD API (User Stories 1-2 - API)

**User Stories**:
- US1: Create and Retrieve Tasks via API (P1)
- US2: Update and Delete Tasks (P1)

**Goal**: Implement core CRUD operations (Create, Read, Update, Delete) with user isolation

**Independent Test**: Authenticate, POST task, GET task list (verify task appears), PUT update (verify change), DELETE (verify removal)

**Prerequisites**: Phase 3 and Phase 4 complete

**Completion Criteria**:
- POST /api/{user_id}/tasks creates tasks
- GET /api/{user_id}/tasks returns user's tasks
- GET /api/{user_id}/tasks/{task_id} returns single task
- PUT /api/{user_id}/tasks/{task_id} updates task
- PATCH /api/{user_id}/tasks/{task_id}/complete toggles completion
- DELETE /api/{user_id}/tasks/{task_id} deletes task
- All endpoints enforce user isolation
- Proper HTTP status codes (200, 201, 204, 400, 401, 403, 404)

### Tasks

- [ ] T024 Create FastAPI router in /backend/routes/tasks.py with dependency on verify_jwt_middleware for all routes
- [ ] T025 [P] [US1] Implement POST /api/{user_id}/tasks endpoint in /backend/routes/tasks.py: create task with validation, return 201 with TaskResponse
- [ ] T026 [P] [US1] Implement GET /api/{user_id}/tasks endpoint (basic version without filters) in /backend/routes/tasks.py: return all user's tasks as TaskResponse array
- [ ] T027 [P] [US1] Implement GET /api/{user_id}/tasks/{task_id} endpoint in /backend/routes/tasks.py: return single task or 404 if not found/wrong user
- [ ] T028 [P] [US2] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in /backend/routes/tasks.py: update task with partial update support, return 200 with TaskResponse
- [ ] T029 [US2] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in /backend/routes/tasks.py: toggle completed status, return 200 with TaskResponse
- [ ] T030 [US2] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in /backend/routes/tasks.py: delete task, return 204 No Content
- [ ] T031 Add input validation error handling in /backend/routes/tasks.py: return 400 Bad Request with ErrorResponse for invalid data (empty title, invalid priority, etc.)
- [ ] T032 Mount tasks router in /backend/main.py with prefix /api and include JWT middleware dependency

---

## Phase 6: P2 - Advanced Filtering (User Story 3 - API)

**User Story**: Filter and Search Tasks (P2)
**Goal**: Implement query parameters for filtering by status, priority, tag, and searching by keywords

**Independent Test**: Create 20 tasks with varied metadata, test each filter combination (status=pending, priority=high, tag=work, search=meeting) and verify correct results

**Prerequisites**: Phase 5 complete

**Completion Criteria**:
- Filter by status (all/pending/completed) works
- Filter by priority (high/medium/low) works
- Filter by tag (matches tasks containing specified tag) works
- Search by keyword (title or description) works
- Filter by due_before date works
- Multiple filters combine with AND logic

### Tasks

- [ ] T033 [US3] Add query parameters to GET /api/{user_id}/tasks in /backend/routes/tasks.py: status, priority, tag, search, due_before with FastAPI Query() validation
- [ ] T034 [P] [US3] Implement status filtering logic in /backend/database/queries.py: filter by completed=true/false based on status parameter
- [ ] T035 [P] [US3] Implement priority filtering logic in /backend/database/queries.py: filter by priority enum value
- [ ] T036 [P] [US3] Implement tag filtering logic in /backend/database/queries.py: use PostgreSQL JSON containment operator for tags array
- [ ] T037 [US3] Implement search logic in /backend/database/queries.py: case-insensitive ILIKE on title and description fields
- [ ] T038 [US3] Implement due_before filtering logic in /backend/database/queries.py: filter tasks where due_date < specified date

---

## Phase 7: P3 - Sorting (User Story 4 - API)

**User Story**: Sort Task Results (P3)
**Goal**: Implement query parameters for sorting results by due_date, priority, or created_at in asc/desc order

**Independent Test**: Create tasks with different due dates and priorities, request sorted results (sort=due_date&order=asc) and verify correct ordering

**Prerequisites**: Phase 6 complete

**Completion Criteria**:
- Sort by due_date works (ascending and descending)
- Sort by priority works (high > medium > low)
- Sort by created_at works (ascending and descending)
- Default sort is created_at descending

### Tasks

- [ ] T039 [US4] Add query parameters to GET /api/{user_id}/tasks in /backend/routes/tasks.py: sort (default="created_at"), order (default="desc")
- [ ] T040 [US4] Implement sorting logic in /backend/database/queries.py: apply ORDER BY clause based on sort and order parameters
- [ ] T041 [US4] Implement priority sorting in /backend/database/queries.py: use CASE statement to map "high"→3, "medium"→2, "low"→1 for numeric sorting

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Finalize error handling, logging, CORS configuration, and documentation

**Prerequisites**: All user story phases complete

**Completion Criteria**:
- CORS configured for frontend origin
- Error handling consistent across all endpoints
- Environment variables documented
- API testable with HTTP client

### Tasks

- [ ] T042 [P] Configure CORS middleware in /backend/main.py: allow_origins=[FRONTEND_URL], allow_methods=[GET,POST,PUT,PATCH,DELETE], allow_headers=[Authorization,Content-Type]
- [ ] T043 [P] Create global exception handlers in /backend/main.py: handle HTTPException, RequestValidationError, and generic exceptions with ErrorResponse format
- [ ] T044 Create HTTP client examples in /backend/tests/api_examples.http: demonstrate all CRUD operations with sample JWT token for manual testing
- [ ] T045 Update /backend/.env.example with production-ready values and security notes: document BETTER_AUTH_SECRET must match frontend, DATABASE_URL SSL requirement

---

## Dependencies Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← Must complete before any user stories
    ├─→ Phase 3 (P1: Database Storage)
    ├─→ Phase 4 (P1: JWT Authentication)
    └─→ Phase 5 (P1: Basic CRUD API) ← Depends on Phases 3 & 4
            ↓
        Phase 6 (P2: Advanced Filtering)
            ↓
        Phase 7 (P3: Sorting)
            ↓
        Phase 8 (Polish)
```

**Critical Path**: Setup → Foundational → JWT Auth → Basic CRUD → Filtering → Sorting → Polish

**Parallel Opportunities**:
- Phase 2: Tasks T007-T010 can run in parallel (different files)
- Phase 3: Tasks T014-T015 can run in parallel (different concerns)
- Phase 4: Tasks T020-T021 can run in parallel (different validation steps)
- Phase 5: Tasks T025-T028 can run in parallel (different endpoints, different files)
- Phase 6: Tasks T034-T036 can run in parallel (different filter implementations)
- Phase 8: Tasks T042-T043 can run in parallel (different concerns)

---

## Parallel Execution Examples

### Phase 2 (Foundational)
**Run in parallel**:
- Developer A: T007 (enums), T008 (Task model)
- Developer B: T009 (request schemas), T010 (response schemas)
- Developer C: T011 (JWT utils)

**Then sequentially**:
- T006 (database connection) - shared by all
- T012, T013 (database initialization and testing)

### Phase 5 (Basic CRUD)
**Run in parallel** (after T024 router setup):
- Developer A: T025 (POST endpoint), T028 (PUT endpoint)
- Developer B: T026 (GET list), T027 (GET single)
- Developer C: T029 (PATCH complete), T030 (DELETE)

**Then**:
- T031 (error handling) - touches all endpoints
- T032 (mount router) - final integration

---

## Implementation Strategy

### MVP First (Phases 1-5)
Complete through "Phase 5: P1 - Basic CRUD API" to have a working backend:
- ✅ User authentication with JWT
- ✅ Create, read, update, delete tasks
- ✅ User isolation enforced
- ✅ Basic task list retrieval

**MVP Task Count**: 32 tasks
**Estimated Parallel Opportunities**: 11 tasks

### Incremental Delivery
After MVP, add features incrementally:
1. **Phase 6**: Advanced filtering for power users (6 tasks)
2. **Phase 7**: Sorting for better UX (3 tasks)
3. **Phase 8**: Polish for production readiness (4 tasks)

### Testing Strategy
Each phase includes independent test criteria:
- **Phase 3**: Manual test script for user isolation
- **Phase 4**: Test JWT scenarios (no token, invalid, mismatched, valid)
- **Phase 5**: Test CRUD operations end-to-end
- **Phase 6**: Test filter combinations
- **Phase 7**: Test sorting variations

---

## Task Execution Guidelines

### Before Starting
1. Read the relevant specifications:
   - Phase 3-4: `/specs/database/schema.md`, `/specs/features/authentication.md`
   - Phase 5-7: `/specs/api/rest-endpoints.md`
2. Review `data-model.md` for validation rules
3. Review `research.md` for technical decisions

### During Implementation
1. Follow task order within each phase (except tasks marked [P])
2. Run parallel tasks ([P]) simultaneously if multiple developers available
3. Mark tasks complete only when tested locally
4. Document any deviations from specs in task notes

### After Each Phase
1. Test phase completion criteria
2. Verify constitutional compliance (user isolation, JWT validation)
3. Update environment variables in `.env.example` if new vars added
4. Move to next phase only when current phase fully working

---

## Constitutional Compliance Checklist

Every task must adhere to CONSTITUTION.md principles:

- **§ I (Spec-Driven)**: ✅ All tasks derived from specifications (database, API, auth specs)
- **§ II (Zero Manual Coding)**: ✅ Tasks executed by @backend-builder and @auth-specialist subagents
- **§ III (Reusable Intelligence)**: ✅ Task structure enables subagent execution with clear file paths
- **§ IV (User Isolation)**: ✅ User_id validation enforced in Phase 4 (T023) and all CRUD operations
- **§ VI (Monorepo Integrity)**: ✅ Shared BETTER_AUTH_SECRET documented in T004

---

## Success Criteria

### Phase Completion
- **Phase 1**: Backend directory exists, dependencies installed, main.py runs without errors
- **Phase 2**: Database connection successful, tables created, models importable
- **Phase 3**: User isolation test passes (user A cannot see user B's tasks)
- **Phase 4**: JWT validation test passes (401 for invalid, 403 for mismatched, 200 for valid)
- **Phase 5**: Full CRUD test passes (create → read → update → delete task)
- **Phase 6**: Filter combinations return correct results
- **Phase 7**: Sorting returns tasks in expected order
- **Phase 8**: CORS works with frontend, error handling consistent

### Overall Success
- ✅ All 45 tasks completed
- ✅ Backend runs locally: `uvicorn main:app --reload`
- ✅ API accessible at `http://localhost:8000/api/{user_id}/tasks`
- ✅ JWT authentication enforced on all protected routes
- ✅ User isolation verified (zero cross-user data leakage)
- ✅ HTTP client examples work for manual testing
- ✅ Ready for frontend integration

---

**Next Steps After Task Completion**:
1. Deploy backend to Render/Railway/Fly.io
2. Update `FRONTEND_URL` environment variable to production Vercel URL
3. Test deployed backend with production Neon PostgreSQL
4. Proceed to frontend implementation (Next.js + Better Auth)
