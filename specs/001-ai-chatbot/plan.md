# Implementation Plan: AI Todo Chatbot Integration

**Branch**: `001-ai-chatbot` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot/spec.md`

## Summary

Integrate an AI-powered chatbot into the existing Phase 2 fullstack Todo application to enable natural language task management. Users will interact with a floating chat interface to perform all CRUD operations (add, list, complete, delete, update tasks) and query user information through conversational commands in English and Urdu. The system uses Cohere API via OpenAI Agents SDK for natural language understanding, MCP tools for task operations, and maintains stateless architecture with conversation history persisted in Neon PostgreSQL.

**Key Technical Approach**:
- Stateless chat endpoint with JWT-based user isolation
- Six MCP tools wrapping existing Phase 2 task API
- Cohere LLM for intent detection and parameter extraction
- React chat UI with Web Speech API for voice input
- RTL layout support for Urdu language
- Conversation history stored in new database tables

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend with Next.js 16+)

**Primary Dependencies**:
- Backend: FastAPI 0.104+, SQLModel 0.14+, OpenAI Agents SDK (latest), Official MCP SDK, Cohere Python SDK
- Frontend: Next.js 16+, React 18+, Tailwind CSS 3.x, next-intl (i18n), Web Speech API (browser native)
- Database: Neon PostgreSQL (serverless)
- Authentication: Better Auth with JWT tokens (existing from Phase 2)

**Storage**: Neon PostgreSQL with new tables (conversations, chat_messages) and existing tables (tasks, users)

**Testing**: pytest (backend API and MCP tools), Jest + React Testing Library (frontend components), manual integration testing for chat flow

**Target Platform**: Web application - Linux server (backend), modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

**Project Type**: Web application (existing monorepo with /frontend and /backend directories)

**Performance Goals**:
- Chat response time: <3 seconds (95th percentile)
- Conversation history load: <500ms
- Intent detection accuracy: >90% for common phrases
- Voice transcription success: >85% in quiet environments

**Constraints**:
- Stateless architecture (no in-memory session state)
- JWT-based authentication (existing Phase 2 system)
- User isolation enforced on all operations
- Conversation history limited to 100 most recent messages
- Cohere API rate limits and quotas
- Browser compatibility for Web Speech API (voice feature)

**Scale/Scope**:
- Multi-user system with user-scoped data
- Expected: 10-100 concurrent users initially
- Conversation history: 100 messages per user displayed
- 6 MCP tools, 5 specialized agents
- 3 new database tables, 2 new API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase 2 Principles Compliance

✅ **I. Spec-Driven Development**: All chatbot features originate from refined specifications (chatbot-architecture.md, chatbot-tools.md, chatbot-frontend.md)

✅ **II. Zero Manual Coding**: Implementation will use specialized agents (chatbot-orchestrator, intent-parser, mcp-tool-executor, chatbot-frontend-integrator, chatbot-api-tester)

✅ **III. Reusable Intelligence**: Five specialized chatbot agents + existing Phase 2 agents utilized for +200 bonus points

✅ **IV. User Isolation and Security**: Chat endpoint follows `/api/{user_id}/chat` pattern with JWT validation and user-scoped operations

✅ **V. Bonus Feature Integration**: Urdu language support (+100) and voice commands (+200) integrated from the start

✅ **VI. Monorepo Integrity**: Uses existing /frontend and /backend directories, shares BETTER_AUTH_SECRET, maintains API contracts

### Phase 3 Principles Compliance

✅ **VII. Stateless Chat Architecture**: Chat endpoint is stateless, conversation history in Neon DB, no in-memory session state

✅ **VIII. Natural Language CRUD**: All task operations executable via natural language in English and Urdu

✅ **IX. Agent-Based Reusable Intelligence**: All five chatbot agents will be utilized (chatbot-orchestrator, intent-parser, mcp-tool-executor, chatbot-frontend-integrator, chatbot-api-tester)

✅ **X. User Context Isolation**: JWT-based user isolation, user info from JWT claims (not database queries)

### Technology Stack Compliance

✅ **Immutable Tech Stack**: Uses Next.js 16+, TypeScript, Tailwind CSS (frontend), Python FastAPI, SQLModel, Neon PostgreSQL (backend)

✅ **Authentication**: Uses existing Better Auth with JWT tokens (no alternative auth services)

✅ **Database**: Uses existing Neon PostgreSQL (no alternative databases)

✅ **Package Managers**: npm (frontend), pip (backend) only

### AI Feature Standards Compliance

✅ **Specifications**: Three refined specs (chatbot-architecture.md, chatbot-tools.md, chatbot-frontend.md) in `/specs/001-ai-chatbot/`

✅ **Cohere API**: Configured in OpenAI Agents SDK initialization

✅ **Conversation History**: Stored in `chat_messages` table with user_id foreign key

✅ **Intent Parsing**: Handles both English and Urdu with equivalent functionality

✅ **MCP Tools**: Six tools (add_task, list_tasks, complete_task, delete_task, update_task, get_user_info) with JWT validation

✅ **Frontend**: Floating chat icon in bottom-right corner, voice button, Urdu RTL support

### Gate Status: ✅ PASSED

All constitutional principles and standards are satisfied. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot/
├── spec.md                    # Main feature specification (COMPLETE)
├── chatbot-architecture.md    # System architecture (COMPLETE)
├── chatbot-tools.md           # MCP tool definitions (COMPLETE)
├── chatbot-frontend.md        # Frontend UI specification (COMPLETE)
├── plan.md                    # This file (IN PROGRESS)
├── research.md                # Phase 0 output (PENDING)
├── data-model.md              # Phase 1 output (PENDING)
├── quickstart.md              # Phase 1 output (PENDING)
├── contracts/                 # Phase 1 output (PENDING)
│   ├── chat-api.yaml          # OpenAPI spec for chat endpoint
│   └── mcp-tools.json         # MCP tool schemas
├── checklists/
│   └── requirements.md        # Quality validation (COMPLETE)
└── tasks.md                   # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py                    # Existing Phase 2 model
│   │   ├── user.py                    # Existing Phase 2 model
│   │   ├── conversation.py            # NEW: Conversation model
│   │   └── chat_message.py            # NEW: ChatMessage model
│   ├── services/
│   │   ├── task_service.py            # Existing Phase 2 service
│   │   ├── auth_service.py            # Existing Phase 2 service
│   │   ├── chat_service.py            # NEW: Chat orchestration
│   │   ├── intent_parser.py           # NEW: Natural language understanding
│   │   └── mcp_tools.py               # NEW: MCP tool implementations
│   ├── api/
│   │   ├── tasks.py                   # Existing Phase 2 endpoints
│   │   ├── auth.py                    # Existing Phase 2 endpoints
│   │   └── chat.py                    # NEW: Chat endpoint
│   ├── middleware/
│   │   └── jwt_auth.py                # Existing Phase 2 middleware
│   ├── config/
│   │   ├── database.py                # Existing Phase 2 config
│   │   └── cohere.py                  # NEW: Cohere API config
│   └── main.py                        # Existing FastAPI app
├── tests/
│   ├── test_chat_api.py               # NEW: Chat endpoint tests
│   ├── test_mcp_tools.py              # NEW: MCP tool tests
│   └── test_intent_parser.py          # NEW: Intent parsing tests
├── requirements.txt                    # Updated with new dependencies
└── alembic/                           # Database migrations
    └── versions/
        └── xxx_add_chat_tables.py     # NEW: Migration for chat tables

frontend/
├── src/
│   ├── components/
│   │   ├── tasks/                     # Existing Phase 2 components
│   │   └── chat/                      # NEW: Chat components
│   │       ├── ChatWidget.tsx         # Root chat component
│   │       ├── ChatIcon.tsx           # Floating icon button
│   │       ├── ChatWindow.tsx         # Main chat window
│   │       ├── ChatHeader.tsx         # Header with close button
│   │       ├── MessageList.tsx        # Scrollable message list
│   │       ├── Message.tsx            # Individual message bubble
│   │       ├── ChatInput.tsx          # Input field with buttons
│   │       └── VoiceButton.tsx        # Microphone button
│   ├── hooks/
│   │   ├── useChat.ts                 # NEW: Chat state management
│   │   ├── useVoiceInput.ts           # NEW: Voice recognition
│   │   └── useChatAPI.ts              # NEW: API integration
│   ├── services/
│   │   └── chatService.ts             # NEW: Chat API client
│   ├── app/
│   │   └── dashboard/
│   │       └── page.tsx               # Updated with ChatWidget
│   └── styles/
│       └── chat.css                   # NEW: Chat-specific styles
├── public/
│   └── locales/
│       ├── en/
│       │   └── chat.json              # NEW: English chat translations
│       └── ur/
│           └── chat.json              # NEW: Urdu chat translations
└── package.json                        # Updated with dependencies
```

**Structure Decision**: Web application (Option 2) - Existing monorepo with separate /frontend and /backend directories. This structure is already established in Phase 2 and will be extended with new chat-related files. No structural changes to the monorepo layout.

## Complexity Tracking

> **No violations - this section is not applicable**

All constitutional requirements are satisfied without exceptions. The implementation follows established patterns from Phase 2 and adds new functionality without violating any principles.

---

## Phase 0: Research (COMPLETE)

**Status**: ✅ All technical decisions finalized

**Output**: `research.md` - Comprehensive research document covering:
- OpenAI Agents SDK with Cohere API integration
- Model Context Protocol (MCP) for tool execution
- Stateless chat architecture patterns
- Web Speech API for voice input
- Urdu language support with RTL layout
- Database schema design (two-table approach)
- JWT validation and user isolation patterns
- Performance optimization strategies
- Security best practices
- Testing and deployment considerations

**Key Decisions**:
1. Use OpenAI Agents SDK configured with Cohere as LLM provider
2. Implement 6 MCP tools for task operations and user info
3. Stateless architecture with database-backed conversation history
4. Browser-native Web Speech API for voice transcription
5. CSS direction property for RTL layout (Urdu support)
6. Two-table design: conversations + chat_messages

---

## Phase 1: Design & Contracts (COMPLETE)

**Status**: ✅ All design artifacts generated

**Outputs**:

1. **data-model.md** - Complete database schema:
   - Conversation entity (UUID, user_id, timestamps)
   - ChatMessage entity (UUID, conversation_id, user_id, sender, text, metadata)
   - Relationships with existing User and Task entities
   - SQLModel definitions with validation rules
   - Query patterns and migration strategy
   - Performance considerations and indexing

2. **contracts/chat-api.yaml** - OpenAPI 3.0 specification:
   - POST /api/{user_id}/chat endpoint
   - Request/response schemas
   - Error responses (400, 401, 403, 429, 500, 503)
   - Authentication (Bearer JWT)
   - Examples for English and Urdu messages

3. **contracts/mcp-tools.json** - MCP tool schemas:
   - 6 tool definitions (add_task, list_tasks, complete_task, delete_task, update_task, get_user_info)
   - JSON Schema parameter validation
   - Return value structures
   - Error codes and usage examples

4. **quickstart.md** - Implementation guide:
   - 5 implementation phases with step-by-step instructions
   - Backend setup (database, models, config)
   - Backend implementation (MCP tools, intent parser, chat service, API endpoint)
   - Frontend implementation (components, hooks, UI integration)
   - Testing & validation (unit, integration, user isolation)
   - Deployment (environment variables, migrations, smoke tests)
   - Troubleshooting guide and success criteria checklist

**Agent Context Updated**: CLAUDE.md updated with Phase 3 technologies

---

## Constitution Check (POST-DESIGN RE-EVALUATION)

*GATE: Re-check after Phase 1 design - FINAL VALIDATION*

### Design Compliance Review

✅ **Spec-Driven Development**: All design artifacts (data-model, contracts, quickstart) derived from specifications

✅ **Zero Manual Coding**: Implementation guide references specialized agents for all code generation

✅ **Reusable Intelligence**: Quickstart explicitly uses 5 chatbot agents throughout implementation

✅ **User Isolation**: Data model enforces user_id foreign keys, API contract validates JWT user_id

✅ **Bonus Features**: Quickstart includes Urdu translations and voice input implementation steps

✅ **Monorepo Integrity**: Project structure maintains /frontend and /backend separation

✅ **Stateless Architecture**: Data model uses database-backed history, no in-memory state

✅ **Natural Language CRUD**: MCP tools cover all CRUD operations with natural language examples

✅ **Agent-Based Intelligence**: Quickstart references all 5 chatbot agents in implementation phases

✅ **User Context Isolation**: Data model and API contract enforce JWT-based isolation

### Technology Stack Validation

✅ **Backend**: Python 3.11+, FastAPI, SQLModel, Neon PostgreSQL (compliant)

✅ **Frontend**: Next.js 16+, TypeScript, Tailwind CSS (compliant)

✅ **Authentication**: Better Auth JWT (existing, reused)

✅ **Database**: Neon PostgreSQL (compliant, new tables added)

✅ **AI Stack**: OpenAI Agents SDK + Cohere API + MCP SDK (Phase 3 additions, approved)

### Final Gate Status: ✅ PASSED

All constitutional requirements satisfied. Design is complete, compliant, and ready for implementation via `/speckit.tasks` command.

---

## Planning Summary

**Branch**: `001-ai-chatbot`

**Planning Status**: ✅ COMPLETE

**Generated Artifacts**:
1. `plan.md` - This implementation plan
2. `research.md` - Technology research and decisions
3. `data-model.md` - Database schema and entities
4. `contracts/chat-api.yaml` - OpenAPI specification
5. `contracts/mcp-tools.json` - MCP tool schemas
6. `quickstart.md` - Implementation guide

**Existing Artifacts** (from `/speckit.specify`):
1. `spec.md` - Feature specification
2. `chatbot-architecture.md` - System architecture
3. `chatbot-tools.md` - MCP tool definitions
4. `chatbot-frontend.md` - Frontend UI specification
5. `checklists/requirements.md` - Quality validation

**Next Steps**:
1. Run `/speckit.tasks` to generate tasks.md with implementation tasks
2. Use specialized agents to implement:
   - chatbot-orchestrator (main control)
   - intent-parser (NLU)
   - mcp-tool-executor (tool execution)
   - chatbot-frontend-integrator (UI)
   - chatbot-api-tester (testing)
3. Follow quickstart.md for step-by-step implementation
4. Deploy and submit Phase 3

**Constitutional Compliance**: ✅ All principles satisfied, no violations

**Ready for Implementation**: ✅ Yes
