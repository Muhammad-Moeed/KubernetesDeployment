<!--
SYNC IMPACT REPORT
==================
Version Change: 1.1.0 → 1.2.0
Bump Rationale: MINOR - Added new Phase 4 section with Local Kubernetes Deployment principles and standards

Modified Principles:
- None (existing principles unchanged)

Added Sections:
- Phase 4 Update - Local Kubernetes Deployment (complete new section with project scope, stack additions, core principles, key standards, constraints, success criteria, and Phase 4 agents)

Removed Sections:
- None

Templates Requiring Updates:
✅ plan-template.md - Reviewed, no updates needed (Constitution Check section is generic and applies to infrastructure)
✅ spec-template.md - Reviewed, no updates needed (template structure remains compatible with infrastructure specs)
✅ tasks-template.md - Reviewed, no updates needed (task organization principles apply to deployment tasks)

Follow-up TODOs:
- None (all placeholders filled, all templates validated)

Date: 2026-02-10
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

## Phase 4 Update - Local Kubernetes Deployment

### Project Scope
Deploy Phase 3 AI Todo Chatbot application on local Kubernetes cluster (Minikube) with containerized frontend and backend services, enabling scalable and production-ready infrastructure.

### Stack Additions
- **Docker**: Container runtime with Gordon AI for Dockerfile generation
- **Helm Charts**: Kubernetes package manager for deployment manifests
- **Minikube**: Local Kubernetes cluster for development and testing
- **kubectl-ai**: AI-powered Kubernetes command-line tool
- **kagent**: Kubernetes agent for intelligent cluster operations

### Core Principles

#### XI. Spec-Driven Infrastructure Automation
All infrastructure components (Dockerfiles, Helm charts, Kubernetes manifests) must originate from refined specifications in `/specs/infrastructure/`. No manual infrastructure code permitted. AI tools (Gordon, kubectl-ai, kagent) must be used for all deployment operations.

#### XII. Stateless and Scalable Deployment
Frontend and backend services must be deployed as stateless containers with horizontal scaling capabilities. Database connections must use external Neon PostgreSQL (not in-cluster). No persistent volumes for application state.

#### XIII. Containerization Best Practices
Dockerfiles must follow multi-stage build patterns, minimize image size, and use non-root users. Frontend container serves static Next.js build. Backend container runs FastAPI with production ASGI server (Gunicorn/Uvicorn).

#### XIV. Infrastructure as Code
All Kubernetes resources (Deployments, Services, ConfigMaps, Secrets) must be defined in Helm charts with parameterized values. No imperative kubectl commands for resource creation. Version control all infrastructure code.

#### XV. AI-Powered Deployment Workflow
Phase 4 implementation must utilize all five specialized Kubernetes agents:
- `k8s-orchestrator`: Coordinates full deployment workflow
- `docker-builder`: Creates optimized container images
- `helm-chart-builder`: Generates Kubernetes manifests
- `k8s-ai-deployer`: Executes deployment with AI tools
- `k8s-deployment-tester`: Validates cluster health

No manual deployment steps permitted. All operations through agents and AI tools only.

### Key Standards

#### Docker Standards
- Multi-stage builds for frontend (build → production) and backend (dependencies → runtime)
- Alpine or distroless base images for minimal attack surface
- Non-root user execution in containers
- `.dockerignore` files to exclude unnecessary files
- Health check endpoints exposed for Kubernetes probes
- Environment variables for configuration (no hardcoded values)

#### Helm Chart Standards
- Separate charts for frontend and backend services
- Parameterized values in `values.yaml` (replicas, resources, image tags)
- Kubernetes Deployments with rolling update strategy
- Services with ClusterIP (internal) or NodePort (external access)
- ConfigMaps for non-sensitive configuration
- Secrets for sensitive data (JWT secret, database URL, API keys)
- Resource requests and limits defined for all containers
- Liveness and readiness probes configured

#### Kubernetes Deployment Standards
- Deploy on Minikube with at least 2 CPU cores and 4GB RAM
- Frontend accessible via NodePort service on Minikube IP
- Backend accessible internally via ClusterIP service
- Use kubectl-ai for deployment commands with natural language
- Use kagent for cluster health checks and troubleshooting
- Namespace isolation (e.g., `todo-app` namespace)
- Labels and selectors for service discovery

#### Testing and Validation Standards
- Pod health checks pass (all pods in Running state)
- Service connectivity verified (frontend can reach backend)
- Scaling tests pass (scale replicas up/down successfully)
- Application functionality verified (chatbot works via Minikube IP)
- Resource utilization monitored (CPU/memory within limits)

### Constraints

#### Existing Infrastructure
- Must use existing `/frontend` and `/backend` folders for source code
- Must maintain Phase 3 chatbot functionality without modifications
- Must use existing Neon PostgreSQL database (external to cluster)
- Must preserve Better Auth JWT authentication flow

#### Implementation Restrictions
- No manual code modifications to frontend or backend
- All infrastructure code generated by agents only
- Local deployment only (no cloud providers yet)
- No in-cluster database (use external Neon PostgreSQL)
- No manual kubectl commands (use kubectl-ai/kagent)

#### Resource Constraints
- Minikube cluster with minimum 2 CPU cores and 4GB RAM
- Frontend container: max 512MB memory, 0.5 CPU
- Backend container: max 1GB memory, 1 CPU
- Total cluster resource usage under 3GB RAM

### Success Criteria

#### Deployment Success
- Application runs successfully on Minikube cluster
- All pods in Running state with 0 restarts
- Frontend accessible via Minikube NodePort service
- Backend accessible internally from frontend pods
- Database connectivity verified (Neon PostgreSQL external)

#### Functionality Validation
- Chatbot accessible via Minikube IP in browser
- Users can register, login, and manage tasks via chat
- Voice commands and Urdu language support functional
- JWT authentication works across containerized services
- All Phase 3 features operational in Kubernetes environment

#### Scaling and Health
- Horizontal pod autoscaling configured (optional)
- Manual scaling tests pass (scale frontend/backend replicas)
- Liveness probes prevent unhealthy pod traffic
- Readiness probes ensure zero-downtime deployments
- Resource limits prevent cluster resource exhaustion

#### Documentation and Submission
- Demo video shows complete deployment process using AI tools
- Infrastructure specs documented in `/specs/infrastructure/`
- Helm charts and Dockerfiles committed to repository
- README updated with Minikube setup and deployment instructions
- Submission includes working Kubernetes deployment

#### Phase 4 Agents Utilization
- `k8s-orchestrator`: Documented usage in deployment workflow
- `docker-builder`: Dockerfiles generated and optimized
- `helm-chart-builder`: Helm charts created with best practices
- `k8s-ai-deployer`: Deployment executed with kubectl-ai/kagent
- `k8s-deployment-tester`: Health checks and validation completed

## Governance

This Constitution supersedes all other development practices and documentation. All code generation, architectural decisions, and feature implementations must comply with these principles.

### Enforcement
Violations—including manual code edits, technology substitutions, or bypassing spec-driven workflows—will result in immediate rollback of changes and re-implementation via proper subagent channels.

### Amendments
Constitutional amendments require documented justification, stakeholder approval, and migration plan. Emergency amendments permitted only for critical security vulnerabilities.

### Compliance Verification
The project maintainer is responsible for ensuring all contributors and subagents adhere to these principles. All pull requests and code reviews must verify constitutional compliance.

**Version**: 1.2.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-02-10
