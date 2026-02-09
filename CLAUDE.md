# Todo App - Hackathon II: Evolution of Todo (Phase 2)

## Project Overview
This is a monorepo for the Spec-Driven Development Hackathon II.
We are currently in **Phase 2**: Building a full-stack multi-user Todo web application using spec-driven development with Claude Code and Spec-Kit Plus.

## Tech Stack
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel, Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Database: Neon.tech serverless Postgres
- Development: Claude Code + Spec-Kit Plus + Subagents + Skills

## Spec-Kit Structure
All specifications are in the `/specs` folder and organized as per Spec-Kit Plus config:
- @specs/overview.md → Project status
- @specs/features/ → Feature specs (task-crud.md, authentication.md)
- @specs/api/ → REST endpoints
- @specs/database/ → Schema and models
- @specs/ui/ → Components and pages

## Reusable Intelligence (Bonus +200)
We are using Claude Code's built-in subagents and skills:
- Subagents in `.claude/agents/`:
  - spec-refiner
  - backend-builder
  - frontend-builder
  - auth-specialist
  - deployment-prep
- Skills in `.claude/skills/`:
  - urdu-support (+100 bonus)
  - voice-commands (+200 bonus)

## Bonus Features Implemented
- Multi-language Support: Urdu + RTL layout (+100 points)
- Voice Commands: Web Speech API for hands-free task management (+200 points)

## Development Workflow
1. Always start by refining specs: `@spec-refiner refine @specs/features/task-crud.md`
2. Implement backend: `@backend-builder implement refined spec`
3. Implement frontend: `@frontend-builder implement UI spec with urdu-support and voice-commands skills`
4. Handle auth: `@auth-specialist integrate JWT across stack`
5. Final prep: `@deployment-prep prepare submission`

## Commands to Run
- Frontend: `cd frontend && npm run dev`
- Backend: `cd backend && uvicorn main:app --reload`
- Both: `docker-compose up`

Never write code manually. Always refine spec until Claude Code generates correct implementation.
