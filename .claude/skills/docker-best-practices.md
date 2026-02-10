---
name: docker-best-practices
description: Best practices for Docker in Phase 4
priority: high
---

- Use multi-stage builds for smaller images
- Frontend: Node.js base for Next.js build
- Backend: Python slim for FastAPI
- Add .dockerignore
- Use Gordon (Docker AI) when available
- Default ports: frontend 3000, backend 8000