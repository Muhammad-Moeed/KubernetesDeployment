# Research & Technical Decisions: Backend API

**Feature**: Backend API Specifications
**Created**: 2026-01-05
**Status**: Complete

---

## Overview

This document consolidates all technical research, decisions, and rationale for the backend API implementation. All [NEEDS CLARIFICATION] items from the planning phase have been resolved through research and informed decision-making.

---

## 1. Database Technology: Neon PostgreSQL vs Alternatives

### Decision
**Neon Serverless PostgreSQL** selected as the database

### Rationale
- **Serverless architecture**: Auto-scaling, no connection pooling management required
- **PostgreSQL compatibility**: Full support for advanced features (JSON columns, arrays, indexes)
- **Developer experience**: Easy integration with SQLModel ORM
- **Cost-effective**: Generous free tier, pay-per-use pricing
- **Performance**: Low-latency serverless Postgres suitable for hackathon requirements (<100ms query times)
- **Constitutional compliance**: Specified in CONSTITUTION.md § Technology Constraints

### Alternatives Considered
- **Supabase**: Similar PostgreSQL offering, but Neon chosen for simplicity
- **PlanetScale (MySQL)**: Rejected due to lack of native JSON/array support and PostgreSQL preference
- **MongoDB**: Rejected due to need for relational integrity (foreign keys for user isolation)

### Implementation Notes
- Connection string format: `postgresql://user:password@ep-xxx.region.neon.tech/dbname?sslmode=require`
- SSL mode required for production security
- DATABASE_URL environment variable for configuration

---

## 2. ORM: SQLModel vs SQLAlchemy vs Raw SQL

### Decision
**SQLModel** selected as the ORM

### Rationale
- **Type safety**: Pydantic integration provides runtime validation and IDE autocomplete
- **Simplicity**: Combines SQLAlchemy power with Pydantic ease-of-use
- **FastAPI integration**: Native Pydantic model support for request/response validation
- **Developer experience**: Single model definition for database and API schemas
- **Constitutional compliance**: Mentioned in database spec for SQLModel examples

### Alternatives Considered
- **SQLAlchemy Core**: More control but more boilerplate, less type safety
- **Raw SQL**: Maximum control but high risk of SQL injection, no type safety
- **Tortoise ORM**: Async-first but less mature ecosystem, not Pydantic-native

### Implementation Notes
- Use `Field()` for column definitions with validation
- Leverage `sa_column_kwargs` for PostgreSQL-specific features (JSON, ARRAY)
- Automatic migration via `SQLModel.metadata.create_all(engine)`

---

## 3. JWT Library: python-jose vs PyJWT vs jose

### Decision
**python-jose[cryptography]** selected for JWT handling

### Rationale
- **Industry standard**: Widely used in FastAPI community
- **Full JWT support**: Signing, verification, expiration handling
- **Algorithm support**: HS256 (HMAC-SHA256) for symmetric signing with shared secret
- **Better Auth compatibility**: Matches Better Auth's JWT format expectations
- **Security**: Includes cryptography library for robust encryption

### Alternatives Considered
- **PyJWT**: Simpler but lacks some advanced features (JWE support)
- **authlib**: More features but overkill for this use case
- **jose**: JavaScript library, not applicable for Python backend

### Implementation Notes
```python
from jose import jwt, JWTError

# Decode and verify
payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
user_id = payload.get("user_id") or payload.get("sub")
```

- Use `HS256` algorithm (symmetric)
- Shared `BETTER_AUTH_SECRET` with frontend (32+ characters)
- Validate `exp` claim for expiration

---

## 4. Task Tags Storage: JSON vs ARRAY vs Separate Table

### Decision
**PostgreSQL JSON column** (or TEXT[] array) for task tags

### Rationale
- **Flexibility**: Users can add arbitrary tags without schema changes
- **Simplicity**: No join queries needed for tag filtering
- **Performance**: PostgreSQL JSON containment operators are highly optimized
- **Use case**: Tags are simple strings, not complex entities requiring normalization
- **Query support**: `tags @> '["work"]'` for efficient tag filtering

### Alternatives Considered
- **Separate tags table + many-to-many**: Overkill for simple string tags, adds complexity
- **Comma-separated string**: Poor query performance, no type safety
- **TEXT[] array**: Equivalent to JSON for this use case, chosen based on PostgreSQL dialect

### Implementation Notes
- SQLModel: `tags: Optional[List[str]] = Field(default=None, sa_column_kwargs={"type_": JSON})`
- Query example: `Task.tags.contains(["work"])` for filtering by tag
- Frontend sends tags as JSON array: `["work", "urgent", "home"]`

---

## 5. User ID Format: UUID vs Integer vs String

### Decision
**String (flexible)** to accommodate Better Auth's user ID format

### Rationale
- **Better Auth compatibility**: Frontend auth system determines user ID format
- **Flexibility**: String type supports UUID, integer, or custom formats
- **Foreign key**: Backend references users table managed by Better Auth
- **No backend user management**: Backend only validates user_id from JWT, doesn't create users

### Alternatives Considered
- **UUID**: Requires Better Auth to use UUID format (may not be configurable)
- **Integer**: Simpler but assumes auto-increment IDs (Better Auth may use UUIDs)
- **String**: Most flexible, allows Better Auth to define format

### Implementation Notes
- SQLModel: `user_id: str = Field(foreign_key="users.id", index=True, nullable=False)`
- JWT payload includes `user_id` claim as string
- Path parameter validation: `{user_id}` in URL as string

---

## 6. Task Priority: Enum vs String vs Integer

### Decision
**Enum (string-based)** for task priority levels

### Rationale
- **Type safety**: Python Enum prevents invalid values
- **Readability**: "high", "medium", "low" more intuitive than integers
- **Database storage**: Stored as string (VARCHAR) in PostgreSQL
- **API clarity**: JSON responses show human-readable priority values
- **Validation**: Pydantic automatically validates against enum values

### Alternatives Considered
- **Integer (1, 2, 3)**: Less readable, requires mapping to display values
- **Raw string**: No type safety, allows typos ("hihg" instead of "high")
- **Database enum type**: More overhead, less flexible for future changes

### Implementation Notes
```python
class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
```

- Default priority: "medium"
- Sorting order: high > medium > low

---

## 7. CORS Configuration: Strict Origin vs Wildcard

### Decision
**Strict origin** based on environment variable `FRONTEND_URL`

### Rationale
- **Security**: Prevents unauthorized domains from accessing API
- **Constitutional compliance**: CONSTITUTION.md § Security Requirements
- **Flexibility**: Different origins for development (localhost:3000) and production (Vercel URL)
- **User isolation**: Part of defense-in-depth strategy (JWT + CORS + user_id validation)

### Alternatives Considered
- **Wildcard (*) **: Rejected due to security risk (anyone can call API)
- **Multiple origins list**: Overkill for single frontend app

### Implementation Notes
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

- Development: `FRONTEND_URL=http://localhost:3000`
- Production: `FRONTEND_URL=https://todo-app.vercel.app`

---

## 8. Timestamp Management: Auto vs Manual

### Decision
**Automatic timestamps** with database defaults

### Rationale
- **Consistency**: Database controls timestamps, no client manipulation possible
- **Accuracy**: Server time is authoritative source
- **Simplicity**: No manual `datetime.utcnow()` calls in route handlers
- **Constitutional compliance**: Database spec requires automatic created_at and updated_at

### Alternatives Considered
- **Manual timestamps**: Requires explicit assignment in every route, error-prone
- **Middleware timestamps**: Adds complexity, database-level is simpler

### Implementation Notes
```python
created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
updated_at: datetime = Field(
    default_factory=datetime.utcnow,
    nullable=False,
    sa_column_kwargs={"onupdate": datetime.utcnow}
)
```

- `created_at`: Set once on insert
- `updated_at`: Automatically updates on every UPDATE query
- Timezone: Store in UTC, convert to user timezone in frontend

---

## 9. Query Filtering: Query Parameters vs Request Body

### Decision
**Query parameters** for GET /tasks endpoint

### Rationale
- **RESTful convention**: Filtering on GET requests uses query parameters
- **Cacheability**: URLs with query params can be cached by CDN/browser
- **Bookmarkability**: Users can bookmark filtered views
- **Simplicity**: No request body parsing needed for GET

### Alternatives Considered
- **Request body on GET**: Non-standard, some clients/proxies reject GET with body
- **POST for search**: Against REST conventions (POST implies mutation)

### Implementation Notes
```python
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    status: Optional[str] = Query(None, regex="^(all|pending|completed)$"),
    priority: Optional[str] = Query(None, regex="^(high|medium|low)$"),
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = Query("created_at", regex="^(due_date|priority|created_at)$"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    due_before: Optional[str] = None,
):
    # Build query dynamically based on provided parameters
```

- Use `Query()` from FastAPI for validation
- Optional parameters: omitted means "no filter"
- Combine with AND logic: `?status=pending&priority=high` → pending AND high priority

---

## 10. Error Response Format: Custom vs HTTP Problem Details

### Decision
**Simple JSON error format** with `error` and optional `detail` fields

### Rationale
- **Simplicity**: Easy to parse on frontend
- **Consistency**: All errors follow same structure
- **FastAPI compatibility**: HTTPException returns similar format
- **Spec compliance**: Matches error response examples in API spec

### Alternatives Considered
- **RFC 7807 Problem Details**: More structured but overkill for this app
- **Multiple error codes**: Complex, not needed for simple CRUD app

### Implementation Notes
```python
# Success response
{"id": 123, "title": "Buy groceries", ...}

# Error response
{"error": "Task not found"}
{"error": "Authentication required", "detail": "Missing Authorization header"}
```

- HTTP status code indicates error type (400, 401, 403, 404, 500)
- `error`: Short message (user-facing)
- `detail`: Optional longer explanation (developer-facing)

---

## 11. Pagination: Included vs Deferred

### Decision
**Deferred to future iteration** (not in MVP)

### Rationale
- **Scope management**: Not in hackathon success criteria
- **User scale**: Most users won't have >1000 tasks
- **Performance**: Database indexes make full-table scans acceptable for small datasets
- **Simplicity**: Reduces implementation complexity for Phase 2

### Future Implementation
- Add query parameters: `?limit=50&offset=100`
- Return metadata: `{"tasks": [...], "total": 250, "limit": 50, "offset": 100}`
- Cursor-based pagination for better performance: `?cursor=eyJpZCI6MTIzfQ==`

### Implementation Notes (MVP)
- Return all user's tasks in single response
- Frontend handles pagination client-side if needed
- Monitor performance and add server-side pagination if needed

---

## 12. Authentication Flow: Session vs JWT

### Decision
**JWT tokens** (stateless authentication)

### Rationale
- **Scalability**: No server-side session storage required
- **Decoupling**: Frontend and backend can be deployed separately
- **Better Auth integration**: Better Auth issues JWT tokens natively
- **Constitutional compliance**: CONSTITUTION.md specifies Better Auth with JWT

### Alternatives Considered
- **Session cookies**: Requires Redis/database for session storage, adds complexity
- **OAuth2 + JWT**: Overkill for this use case (no third-party login needed)

### Implementation Notes
- Frontend (Better Auth) issues JWT on successful login
- Backend verifies JWT signature using shared `BETTER_AUTH_SECRET`
- Token expiration: 24 hours (configurable)
- No refresh token in MVP (users re-authenticate after expiration)

---

## Summary of Technical Stack

| Component           | Technology Choice              | Rationale                          |
|---------------------|--------------------------------|------------------------------------|
| Database            | Neon PostgreSQL                | Serverless, PostgreSQL features    |
| ORM                 | SQLModel                       | Type safety, Pydantic integration  |
| Web Framework       | FastAPI                        | Async, OpenAPI, Pydantic support   |
| JWT Library         | python-jose                    | Better Auth compatibility          |
| Task Tags           | PostgreSQL JSON / TEXT[]       | Flexibility, query performance     |
| User ID Format      | String (flexible)              | Better Auth compatibility          |
| Task Priority       | String Enum                    | Type safety, readability           |
| CORS                | Strict origin (env var)        | Security, single frontend          |
| Timestamps          | Automatic (database)           | Consistency, accuracy              |
| Filtering           | Query parameters               | RESTful, cacheable                 |
| Error Format        | Simple JSON                    | Easy to parse                      |
| Pagination          | Deferred (not in MVP)          | Scope management                   |
| Authentication      | JWT (stateless)                | Scalability, Better Auth integration|

---

## Constitutional Compliance Verification

All decisions align with CONSTITUTION.md principles:

- **§ I (Spec-Driven Development)**: Decisions derived from spec requirements
- **§ III (Reusable Intelligence)**: Technologies chosen for subagent compatibility
- **§ IV (User Isolation and Security)**: User_id validation, JWT verification, CORS
- **§ VI (Monorepo Integrity)**: Shared BETTER_AUTH_SECRET, consistent API contracts

---

## Risk Mitigation

| Risk                          | Mitigation Strategy                                    |
|-------------------------------|--------------------------------------------------------|
| JWT secret mismatch           | Document shared secret requirement, validate in tests  |
| SQL injection                 | Use SQLModel parameterized queries                     |
| Cross-user data leakage       | Enforce user_id filtering in all queries               |
| Token expiration handling     | Frontend redirects to login on 401 Unauthorized        |
| CORS misconfiguration         | Use environment variable, test with deployed frontend  |
| Database connection pooling   | Neon handles automatically (serverless)                |
| Performance with large datasets | Indexes on user_id, due_date, completed              |

---

## Next Steps

1. Use @backend-builder to implement FastAPI application based on these decisions
2. Use @auth-specialist to implement JWT middleware with python-jose
3. Create `.env.example` with all required environment variables:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - `FRONTEND_URL`
   - `JWT_TOKEN_EXPIRY_HOURS` (optional, default 24)

---

**All research complete. Ready for Phase 1: Design & Contracts.**
