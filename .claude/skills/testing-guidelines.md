---
name: testing-guidelines
description: ALWAYS write basic tests for critical features
priority: medium
---

WHEN PREPARING FOR SUBMISSION:

Include these tests:

Backend (pytest):
- Test task creation with valid/invalid data
- Test user isolation (user A can't see user B's tasks)
- Test JWT required for protected routes

Frontend:
- Render test for main components (React Testing Library)
- Test voice button appears
- Test language switcher changes text

Add to README:
```bash
# Run tests
cd backend && pytest
cd frontend && npm test