---
name: nextjs-best-practices
description: ALWAYS follow these Next.js 16+ App Router patterns
priority: high
---

WHEN IMPLEMENTING ANY NEXT.JS CODE:

1. Use App Router (/app folder)
2. Server components by default
3. 'use client' only when needed (hooks, events)

4. API calls pattern:
```ts
// In server component
const tasks = await fetch(`${process.env.BACKEND_URL}/api/tasks`, {
  headers: { Authorization: `Bearer ${token}` }
}).then(res => res.json());