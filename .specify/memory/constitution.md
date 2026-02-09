<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0
Bump Rationale: MINOR - Added new Phase 3 section with AI Chatbot principles and standards

Modified Principles:
- None (existing principles unchanged)

Added Sections:
- Phase 3 Update - AI Chatbot (complete new section with principles, standards, constraints, success criteria)

Removed Sections:
- None

Templates Requiring Updates:
✅ plan-template.md - Reviewed, no updates needed (Constitution Check section is generic)
✅ spec-template.md - Reviewed, no updates needed (template structure remains compatible)
✅ tasks-template.md - Reviewed, no updates needed (task organization principles remain valid)

Follow-up TODOs:
- None (all placeholders filled, all templates validated)

Date: 2026-02-09
-->

# Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All features must originate from refined specifications in `/specs`. No code shall be written without a corresponding specification document that has been reviewed and approved. The workflow is: Specification → Refinement → Review → Implementation.

### II. Zero Manual Coding
All implementation is performed exclusively by Claude Code subagents following specifications. Direct manual code editing is prohibited except for emergency hotfixes. Subagents are the sole code generators to maintain consistency and compliance.

### III. Reusable Intelligence
Development leverages six specialized subagents (spec-refiner, fullstack-todo-agent, nextjs-frontend-builder, backend-builder, auth-specialist, deployment-prep) and seven custom skills to maximize code generation efficiency and earn the +200 bonus points for reusable intelligence.

### IV. User Isolation and Security
All API endpoints follow the `/api/{user_id}/tasks` pattern with strict user-scoped data access. JWT tokens are validated on every request, and user identity from tokens must match URL parameters. No cross-user data leakage permitted.

### V. Bonus Feature Integration
Urdu language support (i18n with RTL layout, +100 points) and voice commands (Web Speech API, +200 points) are first-class features, not afterthoughts. Both must be integrated from the start of any feature implementation.

### VI. Monorepo Integrity
Frontend and backend exist as separate directories within a single repository, sharing authentication secrets (`BETTER_AUTH_SECRET`) and maintaining consistent API contracts defined in `/specs/api/`.

## Key Standards

### Code Generation Rules
- All backend routes must implement user isolation via JWT middleware
- All frontend components must support Urdu language toggling and RTL layout
- Voice command integration must be available on task creation and management pages
- Shared `BETTER_AUTH_SECRET` environment variable must be configured identically in both frontend and backend

### Security Requirements
- JWT tokens validated on every protected API request
- User ID in URL must match authenticated user ID from token
- SQL injection prevention via SQLModel parameterized queries
- CORS configured to allow only frontend origin
- No sensitive data in client-side code or logs

### Internationalization Standards
- English and Urdu language support with next-intl
- RTL layout automatically applied for Urdu
- All UI text externalized to translation files
- No hardcoded strings in components

### Voice Commands Standards
- Web Speech API integration for hands-free task management
- Microphone permission handling with graceful fallback
- Voice input for adding, editing, and searching tasks
- Clear visual feedback during voice recognition

### Testing Requirements
- API endpoints must be manually testable via provided HTTP client examples
- Frontend must render without console errors
- Authentication flow must be demonstrable end-to-end
- Each bonus feature must have a documented test scenario

## Technology Constraints

### Immutable Tech Stack
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel, Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Database: Neon.tech serverless Postgres
- Development Tools: Claude Code, Spec-Kit Plus

### Prohibited Substitutions
- No alternative authentication services (must use Better Auth with JWT)
- No alternative databases (must use Neon PostgreSQL)
- No additional package managers beyond npm (frontend) and pip (backend)
- No technology changes without constitutional amendment

### Spec-Kit Structure Compliance
All specifications must follow Spec-Kit Plus organizational conventions:
- `/specs/overview.md` → Project status
- `/specs/features/` → Feature specs
- `/specs/api/` → REST endpoints
- `/specs/database/` → Schema and models
- `/specs/ui/` → Components and pages

## Success Criteria

### Core Functionality
Users can register, log in, create/read/update/delete tasks, and log out with full user isolation.

### Deployment Readiness
Application runs locally via Docker Compose and is deployable to Vercel (frontend) and Render/Railway (backend).

### Bonus Features Demonstrated
- Urdu language toggle works with proper RTL layout (+100)
- Voice commands successfully create and manage tasks (+200)
- Reusable intelligence (6 subagents + 7 skills) documented and utilized (+200)

### Submission Requirements
README with setup instructions, demo video, deployed URLs, and specification artifacts complete and accurate.

## Phase 3 Update - AI Chatbot

### Project Scope
Integration of conversational AI chatbot into the existing Phase 2 full-stack Todo application, enabling natural language task management and user information queries through a chat interface.

### Stack Additions
- **OpenAI Agents SDK**: Agent orchestration framework (configured with Cohere API key)
- **Official MCP SDK**: Model Context Protocol for tool execution
- **Cohere API**: LLM provider for agent intelligence and natural language understanding

### Core Principles

#### VII. Stateless Chat Architecture
The chat endpoint (`POST /api/{user_id}/chat`) must be stateless, with conversation history persisted in Neon DB. Each request is self-contained with user context derived from JWT tokens. No in-memory session state permitted.

#### VIII. Natural Language CRUD
All task operations (add, list, complete, delete, update) must be executable through natural language chat messages in both English and Urdu. The chatbot must parse intent, extract parameters, and execute corresponding MCP tools without requiring structured input formats.

#### IX. Agent-Based Reusable Intelligence
Phase 3 implementation must utilize all five specialized chatbot agents:
- `chatbot-orchestrator`: Conversation flow management
- `intent-parser`: Natural language understanding
- `mcp-tool-executor`: Tool execution and API integration
- `chatbot-frontend-integrator`: UI component generation
- `chatbot-api-tester`: Endpoint validation and testing

No manual implementation of chatbot logic permitted. All code generation through agents only.

#### X. User Context Isolation
Chatbot must respect JWT-based user isolation. All task operations execute within the authenticated user's scope. User information queries (email, name) must derive from JWT claims, not database lookups.

### Key Standards

#### AI Feature Implementation
- All chatbot features must originate from refined specifications in `/specs/features/`:
  - `chatbot-architecture.md`: System design and agent orchestration
  - `chatbot-tools.md`: MCP tool definitions and contracts
  - `chatbot-frontend.md`: Chat UI components and integration
- Cohere API key must be configured in OpenAI Agents SDK initialization
- Conversation history stored in `chat_messages` table with user_id foreign key
- Intent parsing must handle both English and Urdu with equivalent functionality

#### Chatbot Standards
- Floating chat icon in bottom-right corner of dashboard
- Chat window with message history, input field, and voice button
- Voice input transcription via Web Speech API (bonus feature)
- Urdu language support with RTL layout in chat interface (bonus feature)
- Real-time response streaming for improved UX
- Error handling with user-friendly messages for failed operations

#### MCP Tool Requirements
- Six MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`, `get_user_info`
- Each tool must validate JWT token and enforce user isolation
- Tool responses must be structured JSON for agent parsing
- Tool execution errors must propagate to chat interface with actionable messages

### Constraints

#### Existing Infrastructure
- Must use existing `/frontend` and `/backend` folder structure
- Must integrate with existing Better Auth JWT authentication
- Must use existing Neon PostgreSQL database with new `chat_messages` table
- Must maintain compatibility with Phase 2 task CRUD endpoints

#### Implementation Restrictions
- No manual code writing for chatbot features
- All implementation through chatbot-specific agents only
- No modification of Phase 2 core functionality
- No introduction of new authentication mechanisms

### Success Criteria

#### Chatbot Functionality
- Users can add tasks via natural language chat (English and Urdu)
- Users can list, complete, delete, and update tasks through chat
- Users can query their email and name through chat
- Conversation history persists across sessions
- All operations respect user isolation and JWT authentication

#### Bonus Features Demonstrated
- Urdu chat messages processed with equivalent accuracy to English (+100)
- Voice input successfully transcribes and executes task commands (+200)
- All five chatbot agents documented and utilized in implementation (+200)

#### Submission Requirements
- Updated repository with Phase 3 chatbot implementation
- Deployed chatbot accessible via public URL
- Demo video showing natural language task management in English and Urdu
- Demo video showing voice input creating and managing tasks
- Specification artifacts for all three chatbot specs (architecture, tools, frontend)

## Governance

This Constitution supersedes all other development practices and documentation. All code generation, architectural decisions, and feature implementations must comply with these principles.

### Enforcement
Violations—including manual code edits, technology substitutions, or bypassing spec-driven workflows—will result in immediate rollback of changes and re-implementation via proper subagent channels.

### Amendments
Constitutional amendments require documented justification, stakeholder approval, and migration plan. Emergency amendments permitted only for critical security vulnerabilities.

### Compliance Verification
The project maintainer is responsible for ensuring all contributors and subagents adhere to these principles. All pull requests and code reviews must verify constitutional compliance.

**Version**: 1.1.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-02-09
