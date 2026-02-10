# Implementation Plan: Phase 4 - Local Kubernetes Deployment

**Branch**: `001-k8s-deployment`
**Created**: 2026-02-10
**Status**: Ready for Implementation

## Phase Goal

Deploy the Phase 3 AI Todo Chatbot application on a local Kubernetes cluster (Minikube) using spec-driven infrastructure automation and AI-powered deployment tools.

**Key Objectives**:
- Containerize Next.js frontend and FastAPI backend with Docker
- Create production-ready Helm charts for Kubernetes deployment
- Deploy to Minikube using AI tools (kubectl-ai, kagent, Gordon)
- Validate deployment with comprehensive testing
- Demonstrate scalability and resilience
- Maintain 100% Phase 3 feature parity

**Success Criteria**:
- Application runs on Minikube and is accessible via Minikube IP
- All Phase 3 features work (authentication, tasks, chatbot, voice, Urdu)
- Pods scale horizontally and recover from failures
- Demo video shows complete deployment process
- Repository includes all infrastructure specs and documentation

## Current Status

**Completed**:
- ✅ Phase 2: Full-stack Todo application with authentication
- ✅ Phase 3: AI chatbot with natural language task management
- ✅ CONSTITUTION.md updated with Phase 4 principles
- ✅ Phase 4 specifications created:
  - `specs/001-k8s-deployment/spec.md` (main specification)
  - `specs/001-k8s-deployment/k8s-architecture.md` (architecture design)
  - `specs/001-k8s-deployment/k8s-deployment.md` (deployment procedures)
  - `specs/001-k8s-deployment/k8s-testing.md` (testing procedures)
- ✅ All 5 Phase 4 agents ready:
  - k8s-orchestrator
  - docker-builder
  - helm-chart-builder
  - k8s-ai-deployer
  - k8s-deployment-tester

**Ready to Start**: Implementation phase

## Implementation Steps

### Step 1: Containerize Frontend and Backend

**Agent**: `docker-builder`

**Tasks**:
1. Generate optimized Dockerfile for Next.js frontend using Gordon AI
   - Multi-stage build (build → production)
   - Alpine base image for minimal size (<200MB)
   - Non-root user execution
   - Health check endpoint
2. Generate optimized Dockerfile for FastAPI backend using Gordon AI
   - Multi-stage build (dependencies → runtime)
   - Python slim base image (<500MB)
   - Non-root user execution
   - Health check endpoint
3. Create .dockerignore files for both services
4. Build Docker images locally
5. Test images with docker run to verify functionality
6. Load images into Minikube registry

**Deliverables**:
- `frontend/Dockerfile`
- `frontend/.dockerignore`
- `backend/Dockerfile`
- `backend/.dockerignore`
- Built and tested Docker images

**Validation**:
- Frontend image size <200MB
- Backend image size <500MB
- Images run successfully with docker run
- Health endpoints respond correctly

---

### Step 2: Create Helm Charts

**Agent**: `helm-chart-builder`

**Tasks**:
1. Create Helm chart structure for frontend
   - Chart.yaml with metadata
   - values.yaml with parameterized configuration
   - templates/deployment.yaml with pod specification
   - templates/service.yaml with NodePort service
   - templates/configmap.yaml for environment variables
   - templates/_helpers.tpl for template functions
2. Create Helm chart structure for backend
   - Chart.yaml with metadata
   - values.yaml with parameterized configuration
   - templates/deployment.yaml with pod specification
   - templates/service.yaml with ClusterIP service
   - templates/secret.yaml for sensitive data
   - templates/_helpers.tpl for template functions
3. Configure resource requests and limits
   - Frontend: 256Mi/512Mi RAM, 0.25/0.5 CPU
   - Backend: 512Mi/1Gi RAM, 0.5/1 CPU
4. Configure liveness and readiness probes
5. Validate Helm charts with helm lint

**Deliverables**:
- `helm/todo-frontend/` (complete Helm chart)
- `helm/todo-backend/` (complete Helm chart)

**Validation**:
- helm lint passes for both charts
- values.yaml contains all required parameters
- Templates render correctly with helm template

---

### Step 3: Deploy to Minikube

**Agent**: `k8s-ai-deployer`

**Tasks**:
1. Start Minikube cluster with required resources
   - 2 CPU cores, 4GB RAM
   - Docker driver
2. Create todo-app namespace using kubectl-ai
3. Create ConfigMap for non-sensitive configuration
   - NEXT_PUBLIC_API_URL=http://todo-backend:8000
4. Create Secret for sensitive data
   - DATABASE_URL (Neon PostgreSQL)
   - COHERE_API_KEY
   - BETTER_AUTH_SECRET
5. Deploy backend using helm install
   - 2 replicas
   - ClusterIP service
6. Deploy frontend using helm install
   - 2 replicas
   - NodePort service (port 30080)
7. Verify deployment with kagent health-check
8. Get Minikube IP and access application

**Deliverables**:
- Running Minikube cluster
- Deployed frontend and backend pods
- Accessible application via Minikube IP

**Validation**:
- All pods in Running state
- Services created correctly
- Application accessible at http://<minikube-ip>:30080
- kagent health-check passes

---

### Step 4: Test Deployment

**Agent**: `k8s-deployment-tester`

**Tasks**:
1. Run infrastructure validation tests
   - Verify namespace, ConfigMap, Secrets
   - Verify deployments and services
   - Verify pod status and resource limits
   - Verify probes configuration
2. Run connectivity validation tests
   - Backend health endpoint
   - Frontend health endpoint
   - Frontend → Backend connectivity
   - Backend → Database connectivity
   - External access to frontend
3. Run functionality validation tests
   - User registration and login
   - Task CRUD operations
   - Chatbot functionality
   - Voice commands
   - Urdu language support
4. Run performance validation tests
   - Resource usage monitoring
   - Response time testing
   - Concurrent user testing
5. Run resilience validation tests
   - Pod failure recovery
   - Liveness probe failure
   - Readiness probe failure
6. Run scaling validation tests
   - Scale up frontend to 3 replicas
   - Scale up backend to 3 replicas
   - Scale down to 1 replica
   - Load distribution verification

**Deliverables**:
- Test report with all results
- Screenshots of passing tests
- Performance metrics

**Validation**:
- All 35+ tests pass
- No pod restarts or failures
- Resource usage within limits
- 100% Phase 3 feature parity

---

### Step 5: Full Integration Test

**Agent**: `k8s-orchestrator` (coordinates all agents)

**Tasks**:
1. End-to-end user journey test
   - Register new user
   - Login with credentials
   - Create tasks via UI
   - Create tasks via chatbot (English)
   - Create tasks via chatbot (Urdu)
   - Use voice commands
   - Verify all tasks persist
2. Scaling demonstration
   - Scale frontend to 3 replicas
   - Scale backend to 3 replicas
   - Verify load distribution
   - Scale back down
3. Failure recovery demonstration
   - Delete a backend pod
   - Verify automatic recovery
   - Verify zero data loss
4. Rolling update demonstration
   - Update frontend image tag
   - Verify rolling update
   - Verify zero downtime

**Deliverables**:
- Complete integration test results
- Evidence of all features working
- Scaling and recovery demonstrations

**Validation**:
- All user journeys complete successfully
- Scaling works as expected
- Recovery is automatic and fast
- Rolling updates work without downtime

---

### Step 6: Update Documentation

**Agent**: `k8s-orchestrator`

**Tasks**:
1. Update main README.md with Phase 4 section
   - Prerequisites (Minikube, Docker, Helm, kubectl)
   - Quick start guide
   - Deployment commands
   - Access instructions
   - Troubleshooting tips
2. Create DEPLOYMENT.md with detailed instructions
   - Step-by-step Minikube setup
   - Docker image building
   - Helm chart deployment
   - Testing procedures
   - Cleanup instructions
3. Document AI tools usage
   - Gordon AI for Dockerfiles
   - kubectl-ai for deployments
   - kagent for health checks
4. Update architecture diagrams
   - Add Kubernetes layer
   - Show pod and service relationships

**Deliverables**:
- Updated README.md
- New DEPLOYMENT.md
- Architecture diagrams

**Validation**:
- Documentation is clear and complete
- Commands are copy-paste ready
- New users can follow instructions

---

### Step 7: Record Demo Video

**Agent**: `k8s-orchestrator`

**Tasks**:
1. Prepare demo script
   - Introduction to Phase 4
   - Show existing Phase 3 application
   - Demonstrate containerization process
   - Show Helm chart creation
   - Deploy to Minikube
   - Access application via Minikube IP
   - Test chatbot functionality
   - Demonstrate scaling
   - Show pod recovery
2. Record screen with narration
   - Clear audio
   - Smooth transitions
   - Show all key features
   - Highlight AI tools usage
3. Edit video
   - Add titles and annotations
   - Trim unnecessary parts
   - Add conclusion
4. Upload to YouTube or Google Drive
   - Public or unlisted link
   - Include in submission

**Deliverables**:
- Demo video (5-10 minutes)
- Video link for submission

**Validation**:
- Video shows complete deployment process
- All Phase 4 features demonstrated
- AI tools usage highlighted
- Video is clear and professional

---

### Step 8: Final Submission

**Agent**: `k8s-orchestrator`

**Tasks**:
1. Verify repository is complete
   - All code committed
   - All specs in /specs folder
   - Dockerfiles and Helm charts included
   - Documentation updated
   - .gitignore excludes secrets
2. Verify deployment is working
   - Fresh Minikube deployment
   - All tests pass
   - Application accessible
3. Prepare submission materials
   - Repository URL (public GitHub)
   - Demo video URL
   - WhatsApp number
   - Brief description
4. Submit via Google Form
   - Fill all required fields
   - Double-check links
   - Submit before deadline

**Deliverables**:
- Complete GitHub repository
- Submitted Google Form
- Confirmation receipt

**Validation**:
- Repository is public and accessible
- All links work
- Submission confirmed

## Agent Usage Guide

### k8s-orchestrator Agent

**Role**: Main coordinator for Phase 4 deployment

**Responsibilities**:
- Coordinate all other agents
- Manage workflow sequencing
- Handle agent handoffs
- Ensure spec compliance
- Oversee integration testing
- Manage documentation updates
- Coordinate demo video creation
- Handle final submission

**When to Use**:
- Starting Phase 4 implementation
- Coordinating multiple agents
- Integration testing
- Documentation updates
- Final submission preparation

**Example Invocation**:
```
@k8s-orchestrator coordinate Phase 4 deployment following specs/001-k8s-deployment/plan.md
```

---

### docker-builder Agent

**Role**: Containerization specialist

**Responsibilities**:
- Generate Dockerfiles with Gordon AI
- Optimize Docker images for size and security
- Create .dockerignore files
- Build and test Docker images
- Load images into Minikube registry
- Validate image security and best practices

**When to Use**:
- Step 1: Containerization phase
- When Dockerfiles need optimization
- When images need rebuilding

**Example Invocation**:
```
@docker-builder create optimized Dockerfiles for frontend and backend following specs/001-k8s-deployment/k8s-architecture.md
```

---

### helm-chart-builder Agent

**Role**: Helm chart generation specialist

**Responsibilities**:
- Create Helm chart structure
- Generate Kubernetes manifests (Deployment, Service, ConfigMap, Secret)
- Configure resource limits and probes
- Parameterize values.yaml
- Validate Helm charts with helm lint
- Follow Helm best practices

**When to Use**:
- Step 2: Helm chart creation phase
- When charts need updates
- When adding new Kubernetes resources

**Example Invocation**:
```
@helm-chart-builder create Helm charts for frontend and backend following specs/001-k8s-deployment/k8s-architecture.md
```

---

### k8s-ai-deployer Agent

**Role**: AI-powered deployment specialist

**Responsibilities**:
- Start and configure Minikube cluster
- Deploy applications using kubectl-ai
- Manage scaling with kubectl-ai
- Perform health checks with kagent
- Execute rolling updates
- Handle rollbacks
- Troubleshoot deployment issues

**When to Use**:
- Step 3: Deployment phase
- When scaling applications
- When performing rolling updates
- When troubleshooting cluster issues

**Example Invocation**:
```
@k8s-ai-deployer deploy frontend and backend to Minikube using kubectl-ai and kagent following specs/001-k8s-deployment/k8s-deployment.md
```

---

### k8s-deployment-tester Agent

**Role**: Testing and validation specialist

**Responsibilities**:
- Execute all test phases (infrastructure, connectivity, functionality, performance, resilience, scaling)
- Validate pod health and resource usage
- Test application functionality
- Verify scaling operations
- Test failure recovery
- Generate test reports
- Document test results

**When to Use**:
- Step 4: Testing phase
- After any deployment changes
- Before final submission
- When validating fixes

**Example Invocation**:
```
@k8s-deployment-tester run all tests following specs/001-k8s-deployment/k8s-testing.md and generate test report
```

## Technical Context

**Project Type**: Web application (frontend + backend)

**Source Structure**:
```
/frontend          # Next.js 16+ application
/backend           # FastAPI application
/helm              # Helm charts (to be created)
  /todo-frontend   # Frontend Helm chart
  /todo-backend    # Backend Helm chart
/specs             # Specifications
  /001-k8s-deployment/
    spec.md
    k8s-architecture.md
    k8s-deployment.md
    k8s-testing.md
```

**Technology Stack**:
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, SQLModel
- **Database**: Neon PostgreSQL (external)
- **Authentication**: Better Auth with JWT
- **AI**: Cohere API via OpenAI Agents SDK
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes (Minikube)
- **Package Management**: Helm 3.x
- **AI Tools**: Gordon (Dockerfiles), kubectl-ai (deployments), kagent (health checks)

**Environment Variables**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `COHERE_API_KEY`: Cohere API key for chatbot
- `BETTER_AUTH_SECRET`: JWT signing secret
- `NEXT_PUBLIC_API_URL`: Backend service URL (http://todo-backend:8000)

**Resource Requirements**:
- **Minikube**: 2 CPU cores, 4GB RAM minimum
- **Frontend Pods**: 256Mi/512Mi RAM, 0.25/0.5 CPU (request/limit)
- **Backend Pods**: 512Mi/1Gi RAM, 0.5/1 CPU (request/limit)
- **Total Cluster**: ~3Gi RAM, ~3 CPU (with 2 replicas each)

**External Dependencies**:
- Neon PostgreSQL database (must be accessible from Minikube)
- Cohere API (must be accessible from Minikube)
- Docker Desktop or Docker Engine
- Minikube
- kubectl CLI
- Helm 3.x
- Gordon AI tool
- kubectl-ai tool
- kagent tool

## Bonus Strategy

### Reusable Intelligence (+200 points)

**Phase 4 Agents** (5 specialized agents):
1. k8s-orchestrator - Main coordination
2. docker-builder - Containerization with Gordon AI
3. helm-chart-builder - Helm chart generation
4. k8s-ai-deployer - AI-powered deployment
5. k8s-deployment-tester - Comprehensive testing

**Phase 4 Skills** (5 custom skills):
1. docker-best-practices - Docker optimization guidelines
2. helm-best-practices - Helm chart standards
3. k8s-ai-tools - kubectl-ai and kagent usage
4. minikube-setup - Local cluster configuration
5. spec-driven-infra - Infrastructure as code principles

**Documentation**:
- All agents documented in `.claude/agents/`
- All skills documented in `.claude/skills/`
- Agent coordination workflow in specs
- Clear usage examples in plan.md

### Spec-Driven Infrastructure

**Specifications First**:
- All infrastructure defined in specs before implementation
- No manual infrastructure code
- Agents generate all Dockerfiles and Helm charts
- AI tools execute all deployments

**Spec Artifacts**:
- `specs/001-k8s-deployment/spec.md` - Main specification
- `specs/001-k8s-deployment/k8s-architecture.md` - Architecture design
- `specs/001-k8s-deployment/k8s-deployment.md` - Deployment procedures
- `specs/001-k8s-deployment/k8s-testing.md` - Testing procedures

### AI-Powered Deployment

**Gordon AI**:
- Generates optimized Dockerfiles
- Suggests best practices
- Validates Dockerfile syntax
- Recommends security improvements

**kubectl-ai**:
- Natural language Kubernetes commands
- "deploy the todo frontend with 2 replicas"
- "scale the backend to 3 replicas"
- "show me all pods in the todo-app namespace"

**kagent**:
- Intelligent health checks
- Automated diagnostics
- Resource optimization
- Proactive issue detection

### Phase 3 Feature Preservation

**100% Feature Parity**:
- All Phase 2 features work (authentication, task CRUD)
- All Phase 3 features work (chatbot, natural language)
- Urdu language support (+100 points)
- Voice commands (+200 points)
- No code modifications required

## Submission Checklist

### Repository Requirements

- [ ] Public GitHub repository accessible
- [ ] All source code committed (frontend, backend)
- [ ] All Dockerfiles committed (frontend/Dockerfile, backend/Dockerfile)
- [ ] All Helm charts committed (helm/todo-frontend/, helm/todo-backend/)
- [ ] All specifications committed (specs/001-k8s-deployment/)
- [ ] CONSTITUTION.md updated with Phase 4 principles
- [ ] README.md updated with Phase 4 deployment instructions
- [ ] DEPLOYMENT.md created with detailed steps
- [ ] .gitignore excludes secrets and sensitive data
- [ ] No hardcoded secrets in code or configs

### Deployment Requirements

- [ ] Minikube cluster running successfully
- [ ] All pods in Running state (0 restarts)
- [ ] Frontend accessible via Minikube IP (http://<ip>:30080)
- [ ] Backend accessible internally (http://todo-backend:8000)
- [ ] Database connectivity verified (Neon PostgreSQL)
- [ ] All Phase 3 features working (authentication, tasks, chatbot)
- [ ] Urdu language support functional
- [ ] Voice commands functional
- [ ] Scaling works (scale up/down replicas)
- [ ] Pod recovery works (automatic restart after failure)

### Testing Requirements

- [ ] All infrastructure tests pass (10 tests)
- [ ] All connectivity tests pass (5 tests)
- [ ] All functionality tests pass (6 tests)
- [ ] All performance tests pass (3 tests)
- [ ] All resilience tests pass (4 tests)
- [ ] All scaling tests pass (4 tests)
- [ ] Test report generated with results
- [ ] No errors in pod logs
- [ ] Resource usage within limits

### Documentation Requirements

- [ ] README.md includes Phase 4 section
- [ ] DEPLOYMENT.md with step-by-step instructions
- [ ] Architecture diagrams updated
- [ ] AI tools usage documented
- [ ] Troubleshooting guide included
- [ ] All agents documented in .claude/agents/
- [ ] All skills documented in .claude/skills/
- [ ] Specifications complete and validated

### Demo Video Requirements

- [ ] Video recorded (5-10 minutes)
- [ ] Shows complete deployment process
- [ ] Demonstrates Minikube setup
- [ ] Shows Docker image building
- [ ] Shows Helm chart deployment
- [ ] Demonstrates application access via Minikube IP
- [ ] Tests chatbot functionality
- [ ] Demonstrates scaling operations
- [ ] Shows pod recovery
- [ ] Highlights AI tools usage (Gordon, kubectl-ai, kagent)
- [ ] Clear audio and video quality
- [ ] Uploaded to YouTube or Google Drive
- [ ] Public or unlisted link available

### Submission Form Requirements

- [ ] Google Form filled completely
- [ ] Repository URL provided (public GitHub)
- [ ] Demo video URL provided (YouTube/Drive)
- [ ] WhatsApp number provided
- [ ] Brief description written
- [ ] All links tested and working
- [ ] Submission confirmed before deadline

### Bonus Points Verification

- [ ] Reusable Intelligence: 5 agents + 5 skills documented (+200)
- [ ] Urdu Language Support: Working in Kubernetes (+100)
- [ ] Voice Commands: Working in Kubernetes (+200)
- [ ] Spec-Driven Infrastructure: All specs complete
- [ ] AI-Powered Deployment: Gordon, kubectl-ai, kagent used

## Risk Mitigation

### Potential Issues and Solutions

**Issue**: Docker images too large
- **Solution**: Use multi-stage builds, Alpine/slim base images, optimize layers
- **Agent**: docker-builder with Gordon AI

**Issue**: Minikube resource exhaustion
- **Solution**: Increase Minikube resources, optimize pod resource limits
- **Agent**: k8s-ai-deployer with kagent

**Issue**: Database connectivity from Minikube
- **Solution**: Verify external connectivity, check firewall rules, test with psql
- **Agent**: k8s-deployment-tester

**Issue**: Cohere API unreachable from pods
- **Solution**: Verify external connectivity, check API key, test with curl
- **Agent**: k8s-deployment-tester

**Issue**: Pods in CrashLoopBackOff
- **Solution**: Check logs, verify environment variables, test health endpoints
- **Agent**: k8s-ai-deployer with kagent

**Issue**: Helm chart validation fails
- **Solution**: Run helm lint, fix template errors, validate values.yaml
- **Agent**: helm-chart-builder

**Issue**: Phase 3 features not working
- **Solution**: Verify environment variables, check service connectivity, test endpoints
- **Agent**: k8s-deployment-tester

## Success Metrics

**Deployment Success**:
- ✅ Application runs on Minikube
- ✅ All pods in Running state
- ✅ Accessible via Minikube IP
- ✅ Zero pod restarts

**Functionality Success**:
- ✅ 100% Phase 3 feature parity
- ✅ Authentication works
- ✅ Task CRUD works
- ✅ Chatbot works (English + Urdu)
- ✅ Voice commands work

**Performance Success**:
- ✅ Resource usage within limits
- ✅ Response times <500ms
- ✅ Handles 10+ concurrent users

**Resilience Success**:
- ✅ Pods recover from failures
- ✅ Scaling works (up and down)
- ✅ Rolling updates work
- ✅ Zero downtime

**Documentation Success**:
- ✅ README complete
- ✅ DEPLOYMENT.md complete
- ✅ All specs validated
- ✅ Demo video recorded

**Submission Success**:
- ✅ Repository public
- ✅ All links working
- ✅ Form submitted
- ✅ Confirmation received

## Next Steps

1. **Start Implementation**: Invoke k8s-orchestrator agent to begin Phase 4
2. **Follow Plan**: Execute steps 1-8 sequentially
3. **Use All Agents**: Ensure all 5 agents are utilized
4. **Test Thoroughly**: Run all 35+ tests before submission
5. **Document Everything**: Update README and create DEPLOYMENT.md
6. **Record Demo**: Show complete deployment process
7. **Submit**: Complete Google Form before deadline

**Ready to Begin**: All specifications complete, all agents ready, plan validated ✅
