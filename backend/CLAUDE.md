
### 3. backend/CLAUDE.md

```markdown
# Backend Guidelines - FastAPI Todo API

You are working on the Python FastAPI backend in /backend folder.

## Stack & Rules
- FastAPI
- SQLModel as ORM
- Neon Serverless PostgreSQL
- Uvicorn for running
- Python 3.13+

## Project Structure
- main.py → FastAPI app entry
- models.py → SQLModel models
- routes/ → API route handlers
- db.py → Database session management
- middleware/ → JWT verification

## API Conventions
- All routes under /api/
- Endpoints use {user_id} in path
- All requests must include JWT in Authorization: Bearer header
- Every query MUST filter by authenticated user_id
- Return proper HTTP status codes
- Use Pydantic models for request/response

## JWT Security (Critical)
- Verify JWT using BETTER_AUTH_SECRET
- Extract user_id from token
- Compare with path user_id
- Enforce user isolation on every operation

## Database
- Connection string from DATABASE_URL env var
- Use SQLModel session dependency
- Models must include user_id foreign key

Run with: uvicorn main:app --reload --port 8000

Implement only from refined specs. Reference @specs/api/* and @specs/database/*.