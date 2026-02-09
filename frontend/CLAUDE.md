# Frontend Guidelines - Next.js Todo App

You are working on the Next.js frontend in /frontend folder.

## Stack & Rules
- Next.js 16+ with App Router
- TypeScript only
- Tailwind CSS for styling (no inline styles)
- Server components by default
- Client components only when necessary (interactivity, hooks)

## Project Structure
- /app → Pages and layouts
- /components → Reusable UI components
- /lib/api.ts → API client (must attach JWT to headers)
- /messages → i18n files for Urdu support

## API Client Pattern
All API calls go through /lib/api.ts:
```ts
import { getSession } from '@better-auth/react';

export const api = {
  async getTasks() {
    const session = await getSession();
    return fetch('/api/tasks', {
      headers: { Authorization: `Bearer ${session?.token}` }
    });
  }
}