---
name: helm-best-practices
description: Best practices for Helm charts in Phase 4
priority: high
---

- Create separate charts for frontend and backend
- Use values.yaml for configurable ports, replicas, env vars
- Include deployment, service, ingress (optional)
- Add readiness/liveness probes
- Use Helm templates for DB secrets