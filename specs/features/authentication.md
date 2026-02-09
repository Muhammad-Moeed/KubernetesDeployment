# Authentication Specification: JWT-Based User Isolation

**Created**: 2026-01-05
**Status**: Draft
**Related**: See `/specs/api/rest-endpoints.md` for protected endpoints, `/specs/database/schema.md` for user references
**Constitutional Reference**: CONSTITUTION.md § IV (User Isolation and Security), § VI (Monorepo Integrity)

## Overview

This specification defines the authentication and authorization architecture for the Todo application. The system uses Better Auth on the frontend to issue JWT tokens and FastAPI backend middleware to verify those tokens on every protected request. The shared `BETTER_AUTH_SECRET` environment variable ensures token integrity across the frontend and backend, while strict user_id validation prevents cross-user data access.

## User Scenarios & Testing

### User Story 1 - Register and Login via Frontend (Priority: P1)

As a new user, I must be able to register an account and log in through the frontend, which issues me a JWT token that I can use to access protected backend APIs.

**Why this priority**: Authentication is the foundation - without it, the multi-user application cannot function or enforce user isolation.

**Independent Test**: Open the frontend registration page, create a new account with email/password, verify the frontend receives a JWT token, then make an authenticated API request to verify the token works.

**Acceptance Scenarios**:

1. **Given** a new user visits the registration page, **When** they submit valid email and password, **Then** Better Auth creates the user account and returns a JWT token to the frontend
2. **Given** an existing user visits the login page, **When** they submit correct credentials, **Then** Better Auth authenticates them and returns a JWT token to the frontend
3. **Given** a user has a valid JWT token stored in the frontend, **When** they make API requests to `/api/{user_id}/tasks`, **Then** the token is included in the Authorization header and the backend validates it successfully

---

### User Story 2 - Backend Validates JWT Tokens (Priority: P1)

As the backend system, I must verify every incoming JWT token using the shared secret to ensure only authenticated users can access protected endpoints.

**Why this priority**: Core security requirement - without token validation, any client could forge requests and access any user's data.

**Independent Test**: Make an API request without Authorization header (expect 401), with invalid token (expect 401), with valid token but mismatched user_id (expect 403), and with valid matching token (expect 200).

**Acceptance Scenarios**:

1. **Given** a client makes a request to a protected endpoint without an Authorization header, **When** the backend processes the request, **Then** it returns 401 Unauthorized with error message "Authentication required"
2. **Given** a client sends an invalid JWT token (expired, malformed, or signed with wrong secret), **When** the backend attempts to verify it, **Then** it returns 401 Unauthorized with error message "Invalid or expired token"
3. **Given** a client sends a valid JWT token, **When** the backend decodes it, **Then** it successfully extracts the user_id claim from the token payload
4. **Given** a token contains user_id "user123", **When** the client requests `/api/user456/tasks`, **Then** the backend returns 403 Forbidden with error message "Access denied"

---

### User Story 3 - User Identity Validation (Priority: P1)

As a security enforcement mechanism, the backend must extract the user_id from the JWT token and verify it matches the user_id in the URL path before processing any request.

**Why this priority**: Prevents horizontal privilege escalation - ensures users can only access their own resources even if they have a valid token.

**Independent Test**: Authenticate as user A, obtain JWT token, then attempt to access `/api/userB/tasks` with user A's token, verify backend returns 403 Forbidden.

**Acceptance Scenarios**:

1. **Given** an authenticated user with user_id "abc123", **When** they request `/api/abc123/tasks` with their JWT token, **Then** the backend validates the match and processes the request successfully (200 OK)
2. **Given** an authenticated user with user_id "abc123", **When** they request `/api/xyz789/tasks` with their JWT token, **Then** the backend detects the mismatch and returns 403 Forbidden before querying the database
3. **Given** a valid JWT token with user_id extracted, **When** the backend queries the database for tasks, **Then** it filters by the JWT user_id (not the URL parameter) to ensure data isolation

---

### User Story 4 - Logout and Token Invalidation (Priority: P2)

As a logged-in user, I must be able to log out, which clears my JWT token from the client and prevents further authenticated requests.

**Why this priority**: Security best practice and user expectation - allows users to end their session explicitly.

**Independent Test**: Log in, receive JWT token, make successful authenticated request, log out (token cleared), attempt another request, verify it fails with 401 Unauthorized.

**Acceptance Scenarios**:

1. **Given** a user is logged in with a JWT token stored in the frontend, **When** they click the logout button, **Then** the frontend clears the token from storage (localStorage/sessionStorage/cookies)
2. **Given** a user has logged out, **When** they attempt to access a protected page or make an API request, **Then** the frontend redirects to login or returns 401 Unauthorized due to missing token
3. **Given** the system uses JWT tokens (stateless), **When** a user logs out, **Then** the backend does not maintain a token blacklist (tokens remain valid until expiration; short expiry times mitigate this)

---

### Edge Cases

- **Expired token**: What happens when a JWT token expires while user is mid-session? (Expected: Backend returns 401, frontend detects and redirects to login)
- **Token refresh**: How does the user get a new token without re-entering credentials? (Assumption: Better Auth handles refresh tokens automatically; backend spec only validates access tokens)
- **Missing Authorization header**: What if request completely omits the header? (Expected: 401 Unauthorized immediately)
- **Malformed Bearer token**: What if header is "Authorization: abc123" instead of "Authorization: Bearer abc123"? (Expected: 401 Unauthorized with "Invalid token format")
- **User deleted after login**: What if JWT is valid but user account was deleted? (Expected: Backend queries user table, returns 401 if user not found)
- **Token signed with wrong secret**: What if attacker creates a JWT with correct structure but wrong signature? (Expected: Verification fails, 401 Unauthorized)
- **Very long token**: What if JWT token is abnormally large (>10KB)? (Expected: Backend rejects or validates only expected claims)
- **Multiple simultaneous sessions**: Can a user be logged in on multiple devices with different tokens? (Expected: Yes, JWT is stateless; each device has its own token)
- **Token in query string**: What if client sends token as `?token=xyz` instead of Authorization header? (Expected: Not supported; must use Authorization header for security)

## Requirements

### Functional Requirements

- **FR-001**: Frontend MUST use Better Auth library to handle user registration and login
- **FR-002**: Better Auth MUST issue JWT tokens upon successful authentication
- **FR-003**: Frontend MUST store JWT tokens securely (httpOnly cookies preferred, localStorage/sessionStorage acceptable)
- **FR-004**: Frontend MUST include JWT token in all protected API requests via `Authorization: Bearer {token}` header
- **FR-005**: Backend MUST read `BETTER_AUTH_SECRET` environment variable to verify JWT signatures
- **FR-006**: Backend MUST implement JWT verification middleware that runs before all protected route handlers
- **FR-007**: Middleware MUST extract the token from the `Authorization: Bearer {token}` header
- **FR-008**: Middleware MUST verify the token signature using the shared `BETTER_AUTH_SECRET`
- **FR-009**: Middleware MUST validate token expiration (exp claim) and reject expired tokens with 401 Unauthorized
- **FR-010**: Middleware MUST extract the user_id claim from the decoded JWT payload
- **FR-011**: Middleware MUST compare the extracted user_id with the user_id path parameter in the URL
- **FR-012**: Middleware MUST return 403 Forbidden if user_id from token does not match user_id in URL path
- **FR-013**: Middleware MUST return 401 Unauthorized for missing, malformed, invalid, or expired tokens
- **FR-014**: Middleware MUST attach the validated user_id to the request context for use by route handlers
- **FR-015**: All routes under `/api/{user_id}/` MUST be protected by JWT middleware
- **FR-016**: Logout functionality MUST be handled client-side by clearing the JWT token from storage
- **FR-017**: Backend MUST configure CORS to only accept requests from the authorized frontend origin (environment variable)
- **FR-018**: Backend MUST log all authentication failures (invalid tokens, mismatched user_ids) for security auditing
- **FR-019**: JWT tokens MUST include standard claims: iss (issuer), sub or user_id (subject), exp (expiration), iat (issued at)
- **FR-020**: Token expiration time MUST be configurable via environment variable (default: 24 hours)

### Key Entities

- **JWT Token Structure**:
  - Header: `{"alg": "HS256", "typ": "JWT"}`
  - Payload (claims):
    - `user_id` or `sub`: The authenticated user's unique identifier (string)
    - `exp`: Token expiration timestamp (Unix epoch seconds)
    - `iat`: Token issued-at timestamp (Unix epoch seconds)
    - `iss`: Issuer identifier (optional, e.g., "better-auth")
  - Signature: HMAC-SHA256(base64(header) + "." + base64(payload), BETTER_AUTH_SECRET)

- **AuthMiddleware Context**:
  - Input: HTTP request with Authorization header
  - Output: Validated user_id attached to request context or error response (401/403)
  - Flow: Extract token → Verify signature → Check expiration → Extract user_id → Validate path match → Attach to context

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of protected API endpoints require valid JWT token (test by accessing all endpoints without token, expect 401 for all)
- **SC-002**: Zero successful cross-user access attempts when testing 1,000 requests with valid tokens but mismatched user_ids (100% return 403 Forbidden)
- **SC-003**: Token validation completes in under 10ms per request (minimal performance overhead)
- **SC-004**: Authentication failure rate under 0.1% for legitimate users due to token issues (validates token reliability)
- **SC-005**: Security audit shows no hardcoded secrets in codebase; all secrets loaded from environment variables

## Authentication Flow Diagrams

### Registration and Login Flow

```
┌─────────┐                  ┌────────────────┐                ┌─────────────┐
│ User    │                  │ Frontend       │                │ Better Auth │
│ Browser │                  │ (Next.js)      │                │ Service     │
└────┬────┘                  └───────┬────────┘                └──────┬──────┘
     │                               │                                │
     │ 1. Visit /register            │                                │
     ├──────────────────────────────>│                                │
     │                               │                                │
     │ 2. Submit email/password      │                                │
     ├──────────────────────────────>│                                │
     │                               │ 3. Call Better Auth register   │
     │                               ├───────────────────────────────>│
     │                               │                                │
     │                               │ 4. Create user, issue JWT      │
     │                               │<───────────────────────────────┤
     │                               │   {token: "eyJhbG...", user_id}│
     │ 5. Store token (cookie/local) │                                │
     │<──────────────────────────────┤                                │
     │   Redirect to dashboard       │                                │
     │                               │                                │
```

### Protected API Request Flow

```
┌─────────┐         ┌────────────────┐         ┌──────────────────┐         ┌──────────┐
│ Frontend│         │ Backend API    │         │ JWT Middleware   │         │ Database │
│ Client  │         │ Route Handler  │         │                  │         │          │
└────┬────┘         └───────┬────────┘         └────────┬─────────┘         └─────┬────┘
     │                      │                           │                        │
     │ 1. GET /api/user123/tasks                        │                        │
     │      Authorization: Bearer eyJhbG...             │                        │
     ├──────────────────────┼──────────────────────────>│                        │
     │                      │                           │                        │
     │                      │                           │ 2. Extract token       │
     │                      │                           │    from header         │
     │                      │                           │                        │
     │                      │                           │ 3. Verify signature    │
     │                      │                           │    using SECRET        │
     │                      │                           │                        │
     │                      │                           │ 4. Check expiration    │
     │                      │                           │                        │
     │                      │                           │ 5. Extract user_id     │
     │                      │                           │    from payload        │
     │                      │                           │                        │
     │                      │                           │ 6. Compare JWT user_id │
     │                      │                           │    with path user_id   │
     │                      │                           │    ("user123")         │
     │                      │                           │                        │
     │                      │                           │ 7. Attach user_id to   │
     │                      │                           │    request context     │
     │                      │                           │                        │
     │                      │ 8. Process request with    │                       │
     │                      │<───validated user_id───────┤                        │
     │                      │                           │                        │
     │                      │ 9. Query tasks WHERE user_id = "user123"           │
     │                      ├────────────────────────────────────────────────────>│
     │                      │                           │                        │
     │                      │ 10. Return user's tasks    │                       │
     │                      │<────────────────────────────────────────────────────┤
     │                      │                           │                        │
     │ 11. Return 200 OK    │                           │                        │
     │<─────────────────────┤                           │                        │
     │    [tasks array]     │                           │                        │
     │                      │                           │                        │
```

### Authentication Failure Scenarios

```
┌─────────┐         ┌──────────────────┐
│ Client  │         │ JWT Middleware   │
└────┬────┘         └────────┬─────────┘
     │                       │
     │ Scenario A: Missing token
     │ GET /api/user123/tasks (no Auth header)
     ├──────────────────────>│
     │                       │ Check for Authorization header
     │                       │ → Not found
     │ 401 Unauthorized      │
     │<──────────────────────┤
     │ "Authentication required"
     │                       │
     │ Scenario B: Invalid/expired token
     │ GET /api/user123/tasks
     │ Authorization: Bearer <invalid_token>
     ├──────────────────────>│
     │                       │ Verify signature
     │                       │ → Signature invalid OR expired
     │ 401 Unauthorized      │
     │<──────────────────────┤
     │ "Invalid or expired token"
     │                       │
     │ Scenario C: User ID mismatch
     │ GET /api/user456/tasks
     │ Authorization: Bearer <valid_token_for_user123>
     ├──────────────────────>│
     │                       │ Verify signature → OK
     │                       │ Extract user_id → "user123"
     │                       │ Compare with path → "user456"
     │                       │ → Mismatch detected
     │ 403 Forbidden         │
     │<──────────────────────┤
     │ "Access denied"       │
     │                       │
```

## Implementation Requirements

### Frontend (Next.js + Better Auth)

**Environment Variables:**
```env
BETTER_AUTH_SECRET="your-super-secret-key-min-32-chars"
BETTER_AUTH_URL="http://localhost:3000"
```

**Better Auth Configuration:**
```typescript
// lib/auth.ts (pseudo-code, not implementation)
import { BetterAuth } from "better-auth"

export const auth = BetterAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  // Better Auth handles user registration, login, JWT issuance
  // JWT tokens include user_id claim
})
```

**API Request with Token:**
```typescript
// Example: Making authenticated request (pseudo-code)
const response = await fetch(`/api/${userId}/tasks`, {
  headers: {
    'Authorization': `Bearer ${jwtToken}`,
    'Content-Type': 'application/json'
  }
})
```

**Logout:**
```typescript
// Clear token from storage (pseudo-code)
function logout() {
  localStorage.removeItem('jwt_token')
  // or document.cookie = 'token=; Max-Age=0'
  window.location.href = '/login'
}
```

### Backend (FastAPI + JWT Verification)

**Environment Variables:**
```env
BETTER_AUTH_SECRET="your-super-secret-key-min-32-chars"  # MUST match frontend
JWT_TOKEN_EXPIRY_HOURS=24
FRONTEND_URL="http://localhost:3000"
```

**JWT Middleware Pseudo-Code:**
```python
# middleware/auth.py (pseudo-code for illustration)
from fastapi import Request, HTTPException
from jose import jwt, JWTError
import os

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

async def verify_jwt_middleware(request: Request):
    # 1. Extract Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authentication required")

    # 2. Parse Bearer token
    try:
        scheme, token = auth_header.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    # 3. Verify JWT signature and decode
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 4. Extract user_id from payload
    jwt_user_id = payload.get("user_id") or payload.get("sub")
    if not jwt_user_id:
        raise HTTPException(status_code=401, detail="Token missing user_id claim")

    # 5. Extract user_id from path parameter
    path_user_id = request.path_params.get("user_id")

    # 6. Validate user_id match
    if jwt_user_id != path_user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # 7. Attach validated user_id to request state
    request.state.user_id = jwt_user_id

    return jwt_user_id
```

**Protected Route Example:**
```python
# routes/tasks.py (pseudo-code)
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    validated_user_id: str = Depends(verify_jwt_middleware)
):
    # validated_user_id is guaranteed to match user_id at this point
    # Query database filtered by validated_user_id
    tasks = await db.query(Task).filter(Task.user_id == validated_user_id).all()
    return tasks
```

**CORS Configuration:**
```python
# main.py (pseudo-code)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  # Only allow frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Constitutional Compliance

This specification adheres to the project Constitution:

- **§ IV (User Isolation and Security)**: JWT validation on every request; user_id extraction and validation prevents cross-user access; tokens signed with shared secret ensure integrity
- **§ VI (Monorepo Integrity)**: Shared `BETTER_AUTH_SECRET` environment variable configured identically in frontend and backend ensures token compatibility
- **§ I (Spec-Driven Development)**: No implementation code, only pseudo-code examples for illustration; auth-specialist subagent will generate actual FastAPI middleware
- **Security Requirements**: JWT tokens validated on every protected API request; user ID in URL must match authenticated user ID from token; no sensitive data in client-side code

## Urdu Translations (Authentication Messages)

| English Message                          | Urdu Translation (اردو)                          |
|------------------------------------------|-------------------------------------------------|
| "Authentication required"                | "تصدیق ضروری ہے"                                |
| "Invalid or expired token"               | "غلط یا میعاد ختم ٹوکن"                         |
| "Access denied"                          | "رسائی مسترد"                                    |
| "Invalid authentication scheme"          | "غلط تصدیق کی اسکیم"                             |
| "Invalid token format"                   | "غلط ٹوکن کی شکل"                               |
| "Token missing user_id claim"            | "ٹوکن میں صارف کی شناخت موجود نہیں"             |
| "Login successful"                       | "لاگ ان کامیاب"                                 |
| "Registration successful"                | "رجسٹریشن کامیاب"                               |
| "Logout successful"                      | "لاگ آؤٹ کامیاب"                                |
| "Please log in to continue"              | "جاری رکھنے کے لیے لاگ ان کریں"                 |
| "Session expired, please login again"    | "سیشن ختم ہو گیا، دوبارہ لاگ ان کریں"           |

## Assumptions

- Better Auth on the frontend handles all user registration, login, and JWT token issuance (backend does NOT have custom login endpoints)
- JWT tokens use HS256 algorithm (HMAC with SHA-256) for symmetric signing
- Token expiration is 24 hours by default (configurable via environment variable)
- No token refresh mechanism specified initially; users must log in again after expiration (refresh tokens can be added later)
- No token blacklist or revocation mechanism (stateless JWT design; short expiry mitigates logout security concern)
- User accounts are managed by Better Auth; backend assumes users table exists with id field
- Frontend stores JWT tokens in localStorage or httpOnly cookies (security trade-offs documented elsewhere)
- No rate limiting on authentication endpoints initially (can be added later)
- No multi-factor authentication (MFA) initially (can be added as Better Auth feature later)
- Password complexity requirements managed by Better Auth, not backend
- Account recovery (forgot password) managed by Better Auth, not backend

## Security Considerations

1. **Secret Management**: `BETTER_AUTH_SECRET` must be at least 32 characters, randomly generated, and stored securely in environment variables (never committed to Git)
2. **Token Storage**: Frontend should use httpOnly cookies for maximum security; if using localStorage, vulnerable to XSS attacks
3. **HTTPS Required**: All authentication traffic must use HTTPS in production to prevent token interception
4. **Token Expiration**: Short-lived tokens (24 hours) reduce risk if tokens are compromised; refresh tokens can extend session without re-authentication
5. **CORS Restrictions**: Backend only accepts requests from authorized frontend origin to prevent cross-site attacks
6. **Logging**: Authentication failures logged for security monitoring but without exposing sensitive token details
7. **No Password Storage**: Backend never handles raw passwords; Better Auth manages hashing and validation

## Next Steps

1. Use `@auth-specialist` to implement backend JWT middleware:
   - Install `python-jose` library for JWT verification
   - Create middleware function as specified
   - Integrate with FastAPI dependency injection
   - Test with valid/invalid/mismatched tokens
2. Use `@nextjs-frontend-builder` to integrate Better Auth:
   - Configure Better Auth with shared secret
   - Implement registration and login pages
   - Store JWT tokens securely
   - Include Authorization header in all API requests
3. Reference `/specs/api/rest-endpoints.md` for protected route implementation
4. Coordinate `BETTER_AUTH_SECRET` configuration between frontend and backend `.env` files
