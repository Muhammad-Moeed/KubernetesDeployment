---
name: fastapi-best-practices
description: ALWAYS apply these FastAPI patterns for clean, secure backend
priority: high
---

WHEN IMPLEMENTING ANY FASTAPI CODE:

1. Use dependency injection for database session:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()