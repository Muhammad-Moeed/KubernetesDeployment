---

description: "Task list for Phase 4 Local Kubernetes Deployment"
---

# Tasks: Phase 4 - Local Kubernetes Deployment

**Input**: Design documents from `/specs/001-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required), k8s-architecture.md, k8s-deployment.md, k8s-testing.md

**Tests**: Tests are NOT explicitly requested in the specification. Focus on implementation and validation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/`, `backend/`, `helm/`
- Paths shown below follow the monorepo structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and prerequisite verification

- [x] T001 Verify Minikube is installed and accessible (minikube version)
- [x] T002 Verify Docker is installed and running (docker version)
- [x] T003 Verify kubectl is installed and configured (kubectl version)
- [x] T004 Verify Helm 3.x is installed (helm version)
- [x] T005 [P] Verify Gordon AI tool is available for Dockerfile generation
- [x] T006 [P] Verify kubectl-ai tool is available for AI-powered deployments
- [x] T007 [P] Verify kagent tool is available for cluster health checks
- [x] T008 Create helm/ directory structure for Helm charts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Verify Phase 3 chatbot application is functional (frontend and backend running locally)
- [x] T010 Verify DATABASE_URL environment variable is set and accessible
- [x] T011 Verify COHERE_API_KEY environment variable is set and valid
- [x] T012 Verify BETTER_AUTH_SECRET environment variable is set
- [x] T013 Test database connectivity from local machine to Neon PostgreSQL
- [x] T014 Test Cohere API connectivity from local machine

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Containerize Application (Priority: P1) 🎯 MVP

**Goal**: Create optimized Docker images for frontend and backend that can run consistently across environments

**Independent Test**: Build Docker images locally, run containers with docker run, verify application works identically to non-containerized version

### Implementation for User Story 1

- [x] T015 [P] [US1] Generate optimized Dockerfile for Next.js frontend using Gordon AI in frontend/Dockerfile
- [x] T016 [P] [US1] Create .dockerignore file for frontend in frontend/.dockerignore
- [x] T017 [P] [US1] Generate optimized Dockerfile for FastAPI backend using Gordon AI in backend/Dockerfile
- [x] T018 [P] [US1] Create .dockerignore file for backend in backend/.dockerignore
- [x] T019 [US1] Configure Docker to use Minikube's Docker daemon (eval $(minikube docker-env))
- [x] T020 [US1] Build frontend Docker image with tag todo-frontend:latest
- [x] T021 [US1] Build backend Docker image with tag todo-backend:latest
- [x] T022 [US1] Verify frontend image size is under 200MB
- [x] T023 [US1] Verify backend image size is under 500MB
- [x] T024 [US1] Test frontend container locally with docker run (port 3000)
- [x] T025 [US1] Test backend container locally with docker run (port 8000, with env vars)
- [x] T026 [US1] Verify frontend health endpoint responds correctly (/api/health)
- [x] T027 [US1] Verify backend health endpoint responds correctly (/health)
- [x] T028 [US1] Verify application functionality in containers (authentication, tasks, chatbot)
- [x] T029 [US1] Load frontend image into Minikube registry
- [x] T030 [US1] Load backend image into Minikube registry

**Checkpoint**: At this point, User Story 1 should be fully functional - Docker images built, tested, and loaded into Minikube

---

## Phase 4: User Story 2 - Deploy to Local Kubernetes (Priority: P2)

**Goal**: Deploy containerized application to Minikube cluster and verify all features work in Kubernetes environment

**Independent Test**: Deploy to Minikube, access application via Minikube IP, verify all Phase 3 features work

### Implementation for User Story 2

#### Helm Chart Creation

- [x] T031 [P] [US2] Create frontend Helm chart structure in helm/todo-frontend/
- [x] T032 [P] [US2] Create frontend Chart.yaml with metadata in helm/todo-frontend/Chart.yaml
- [x] T033 [P] [US2] Create frontend values.yaml with parameterized config in helm/todo-frontend/values.yaml
- [x] T034 [P] [US2] Create frontend Deployment template in helm/todo-frontend/templates/deployment.yaml
- [x] T035 [P] [US2] Create frontend Service template (NodePort) in helm/todo-frontend/templates/service.yaml
- [x] T036 [P] [US2] Create frontend ConfigMap template in helm/todo-frontend/templates/configmap.yaml
- [x] T037 [P] [US2] Create frontend helpers template in helm/todo-frontend/templates/_helpers.tpl
- [x] T038 [P] [US2] Create backend Helm chart structure in helm/todo-backend/
- [x] T039 [P] [US2] Create backend Chart.yaml with metadata in helm/todo-backend/Chart.yaml
- [x] T040 [P] [US2] Create backend values.yaml with parameterized config in helm/todo-backend/values.yaml
- [x] T041 [P] [US2] Create backend Deployment template in helm/todo-backend/templates/deployment.yaml
- [x] T042 [P] [US2] Create backend Service template (ClusterIP) in helm/todo-backend/templates/service.yaml
- [x] T043 [P] [US2] Create backend Secret template in helm/todo-backend/templates/secret.yaml
- [x] T044 [P] [US2] Create backend helpers template in helm/todo-backend/templates/_helpers.tpl
- [x] T045 [US2] Configure resource requests and limits in frontend values.yaml (256Mi/512Mi RAM, 0.25/0.5 CPU)
- [x] T046 [US2] Configure resource requests and limits in backend values.yaml (512Mi/1Gi RAM, 0.5/1 CPU)
- [x] T047 [US2] Configure liveness probe for frontend in deployment template (/api/health)
- [x] T048 [US2] Configure readiness probe for frontend in deployment template (/api/health)
- [x] T049 [US2] Configure liveness probe for backend in deployment template (/health)
- [x] T050 [US2] Configure readiness probe for backend in deployment template (/health)
- [x] T051 [US2] Validate frontend Helm chart with helm lint
- [x] T052 [US2] Validate backend Helm chart with helm lint
- [x] T053 [US2] Test frontend chart rendering with helm template
- [x] T054 [US2] Test backend chart rendering with helm template

#### Minikube Cluster Setup

- [x] T055 [US2] Start Minikube cluster with 2 CPU cores and 4GB RAM (minikube start --cpus=2 --memory=4096)
- [x] T056 [US2] Verify Minikube cluster is running (kubectl cluster-info)
- [x] T057 [US2] Enable metrics-server addon (minikube addons enable metrics-server)
- [x] T058 [US2] Create todo-app namespace using kubectl-ai
- [x] T059 [US2] Set kubectl context to todo-app namespace

#### Kubernetes Resources Deployment

- [x] T060 [US2] Create ConfigMap for frontend configuration (NEXT_PUBLIC_API_URL=http://todo-backend:8000)
- [x] T061 [US2] Create Secret for sensitive data (DATABASE_URL, COHERE_API_KEY, BETTER_AUTH_SECRET)
- [x] T062 [US2] Deploy backend using helm install with 2 replicas
- [x] T063 [US2] Wait for backend pods to reach Running state
- [x] T064 [US2] Verify backend pods are healthy (kubectl get pods -l app=todo-backend)
- [x] T065 [US2] Deploy frontend using helm install with 2 replicas
- [x] T066 [US2] Wait for frontend pods to reach Running state
- [x] T067 [US2] Verify frontend pods are healthy (kubectl get pods -l app=todo-frontend)
- [x] T068 [US2] Verify backend service is created (ClusterIP)
- [x] T069 [US2] Verify frontend service is created (NodePort on port 30080)
- [x] T070 [US2] Get Minikube IP address (minikube ip)
- [x] T071 [US2] Access frontend via Minikube IP (http://<minikube-ip>:30080)

#### Deployment Validation

- [x] T072 [US2] Run kagent health-check on todo-app namespace
- [x] T073 [US2] Verify all pods show STATUS: Running and READY: 1/1
- [x] T074 [US2] Verify no pod restarts (RESTARTS: 0)
- [x] T075 [US2] Check backend pod logs for errors (kubectl logs -l app=todo-backend)
- [x] T076 [US2] Check frontend pod logs for errors (kubectl logs -l app=todo-frontend)
- [x] T077 [US2] Test backend health endpoint from within cluster (curl http://todo-backend:8000/health)
- [x] T078 [US2] Test frontend health endpoint from within cluster (curl http://todo-frontend:3000/api/health)
- [x] T079 [US2] Test frontend to backend connectivity
- [x] T080 [US2] Test backend to database connectivity (check logs for connection success)
- [x] T081 [US2] Verify external access to frontend via Minikube IP

#### Functionality Validation

- [x] T082 [US2] Test user registration via Kubernetes deployment
- [x] T083 [US2] Test user login via Kubernetes deployment
- [x] T084 [US2] Test task creation via Kubernetes deployment
- [x] T085 [US2] Test task listing via Kubernetes deployment
- [x] T086 [US2] Test task update via Kubernetes deployment
- [x] T087 [US2] Test task deletion via Kubernetes deployment
- [x] T088 [US2] Test chatbot functionality (English messages)
- [x] T089 [US2] Test chatbot functionality (Urdu messages)
- [x] T090 [US2] Test voice commands functionality
- [x] T091 [US2] Verify 100% Phase 3 feature parity

**Checkpoint**: At this point, User Story 2 should be fully functional - application deployed to Kubernetes and all features working

---

## Phase 5: User Story 3 - Scale and Monitor Deployment (Priority: P3)

**Goal**: Validate scalability and resilience of Kubernetes deployment

**Independent Test**: Scale replicas up and down, monitor resource usage, verify application continues to function correctly

### Implementation for User Story 3

#### Scaling Operations

- [x] T092 [US3] Scale frontend deployment to 3 replicas using kubectl-ai
- [x] T093 [US3] Verify all 3 frontend pods reach Running state
- [x] T094 [US3] Verify traffic is distributed across frontend pods
- [x] T095 [US3] Scale backend deployment to 3 replicas using kubectl-ai
- [x] T096 [US3] Verify all 3 backend pods reach Running state
- [x] T097 [US3] Verify backend pods maintain database consistency
- [x] T098 [US3] Test application functionality with scaled deployment
- [x] T099 [US3] Scale frontend back down to 1 replica
- [x] T100 [US3] Scale backend back down to 1 replica
- [x] T101 [US3] Verify graceful pod termination during scale down

#### Resource Monitoring

- [x] T102 [US3] Monitor frontend pod resource usage with kubectl top pods
- [x] T103 [US3] Monitor backend pod resource usage with kubectl top pods
- [x] T104 [US3] Verify frontend pods stay within limits (CPU <0.5, Memory <512Mi)
- [x] T105 [US3] Verify backend pods stay within limits (CPU <1, Memory <1Gi)
- [x] T106 [US3] Run kagent monitor-resources for 60 seconds
- [x] T107 [US3] Verify no OOMKilled events in pod status

#### Performance Testing

- [x] T108 [US3] Test frontend health endpoint response time (<100ms)
- [x] T109 [US3] Test backend health endpoint response time (<100ms)
- [x] T110 [US3] Run concurrent user test (10 users) using Apache Bench or similar
- [x] T111 [US3] Verify no failed requests during concurrent testing
- [x] T112 [US3] Verify no performance degradation under load

#### Resilience Testing

- [x] T113 [US3] Delete one backend pod to simulate failure
- [x] T114 [US3] Verify Kubernetes automatically creates replacement pod
- [x] T115 [US3] Verify replacement pod reaches Running state within 30 seconds
- [x] T116 [US3] Verify application remains accessible during pod recovery
- [x] T117 [US3] Verify zero data loss after pod recovery
- [x] T118 [US3] Delete one frontend pod to simulate failure
- [x] T119 [US3] Verify automatic frontend pod recovery
- [x] T120 [US3] Test liveness probe failure scenario (if possible)
- [x] T121 [US3] Test readiness probe failure scenario (if possible)

#### Rolling Update Testing

- [x] T122 [US3] Update frontend image tag to simulate new version
- [x] T123 [US3] Perform rolling update using helm upgrade
- [x] T124 [US3] Monitor rollout status (kubectl rollout status)
- [x] T125 [US3] Verify zero downtime during rolling update
- [x] T126 [US3] Verify all pods updated to new version
- [x] T127 [US3] Test rollback functionality (helm rollback)
- [x] T128 [US3] Verify successful rollback to previous version

**Checkpoint**: At this point, User Story 3 should be fully functional - scaling, monitoring, and resilience validated

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, demo video, and final submission

### Documentation Updates

- [x] T129 [P] Update README.md with Phase 4 section in README.md
- [x] T130 [P] Add prerequisites section (Minikube, Docker, Helm, kubectl) to README.md
- [x] T131 [P] Add quick start guide for Kubernetes deployment to README.md
- [x] T132 [P] Add deployment commands to README.md
- [x] T133 [P] Add access instructions (Minikube IP) to README.md
- [x] T134 [P] Add troubleshooting tips to README.md
- [x] T135 [P] Create DEPLOYMENT.md with detailed step-by-step instructions
- [x] T136 [P] Document Minikube setup in DEPLOYMENT.md
- [x] T137 [P] Document Docker image building in DEPLOYMENT.md
- [x] T138 [P] Document Helm chart deployment in DEPLOYMENT.md
- [x] T139 [P] Document testing procedures in DEPLOYMENT.md
- [x] T140 [P] Document cleanup instructions in DEPLOYMENT.md
- [x] T141 [P] Document Gordon AI usage in DEPLOYMENT.md
- [x] T142 [P] Document kubectl-ai usage in DEPLOYMENT.md
- [x] T143 [P] Document kagent usage in DEPLOYMENT.md
- [x] T144 Update architecture diagrams with Kubernetes layer

### Demo Video Creation

- [ ] T145 Prepare demo script covering all Phase 4 features
- [ ] T146 Record screen showing Phase 3 application running locally
- [ ] T147 Record Docker image building process
- [ ] T148 Record Helm chart creation and validation
- [ ] T149 Record Minikube cluster setup
- [ ] T150 Record application deployment to Minikube
- [ ] T151 Record accessing application via Minikube IP
- [ ] T152 Record chatbot functionality test (English and Urdu)
- [ ] T153 Record voice commands test
- [ ] T154 Record scaling demonstration (scale up to 3 replicas)
- [ ] T155 Record pod failure and recovery demonstration
- [ ] T156 Record resource monitoring with kagent
- [ ] T157 Highlight Gordon AI, kubectl-ai, and kagent usage in video
- [ ] T158 Edit video with titles, annotations, and smooth transitions
- [ ] T159 Add introduction and conclusion to video
- [ ] T160 Upload video to YouTube or Google Drive (public/unlisted)
- [ ] T161 Verify video link is accessible

### Final Submission Preparation

- [x] T162 Verify all source code is committed to repository
- [x] T163 Verify all Dockerfiles are committed (frontend/Dockerfile, backend/Dockerfile)
- [x] T164 Verify all Helm charts are committed (helm/todo-frontend/, helm/todo-backend/)
- [x] T165 Verify all specifications are committed (specs/001-k8s-deployment/)
- [x] T166 Verify CONSTITUTION.md includes Phase 4 principles
- [x] T167 Verify README.md is updated with Phase 4 content
- [x] T168 Verify DEPLOYMENT.md is created and complete
- [x] T169 Verify .gitignore excludes secrets and sensitive data
- [x] T170 Verify no hardcoded secrets in code or configs
- [ ] T171 Make repository public on GitHub
- [ ] T172 Test repository clone from fresh location
- [ ] T173 Perform fresh Minikube deployment from repository
- [ ] T174 Verify all tests pass on fresh deployment
- [ ] T175 Verify application is accessible on fresh deployment
- [ ] T176 Prepare submission materials (repo URL, video URL, WhatsApp, description)
- [ ] T177 Fill Google Form with all required information
- [ ] T178 Double-check all links work (repository, video)
- [ ] T179 Submit Google Form before deadline
- [ ] T180 Save submission confirmation receipt

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion (needs Docker images)
- **User Story 3 (Phase 5)**: Depends on User Story 2 completion (needs deployed application)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: DEPENDS on User Story 1 (needs Docker images and Helm charts)
- **User Story 3 (P3)**: DEPENDS on User Story 2 (needs deployed application to scale and monitor)

### Within Each User Story

**User Story 1 (Containerization)**:
- Dockerfiles can be generated in parallel (T015-T018)
- Images must be built sequentially after Dockerfiles (T020-T021)
- Testing happens after images are built (T022-T028)
- Loading into Minikube happens last (T029-T030)

**User Story 2 (Deployment)**:
- Helm charts can be created in parallel (T031-T044)
- Chart configuration happens after structure (T045-T054)
- Minikube setup is independent (T055-T059)
- Backend must be deployed before frontend (T062-T067)
- Validation happens after deployment (T072-T091)

**User Story 3 (Scaling)**:
- Scaling tests are sequential (T092-T101)
- Monitoring can happen in parallel with scaling (T102-T107)
- Performance tests are independent (T108-T112)
- Resilience tests are sequential (T113-T121)
- Rolling update tests are sequential (T122-T128)

### Parallel Opportunities

- **Setup Phase**: All verification tasks (T001-T007) can run in parallel
- **User Story 1**: Dockerfile generation (T015-T018) can run in parallel
- **User Story 2**:
  - Frontend Helm chart creation (T031-T037) can run in parallel
  - Backend Helm chart creation (T038-T044) can run in parallel
  - Both chart sets can be created in parallel with each other
- **Phase 6**: All documentation tasks (T129-T144) can run in parallel

---

## Parallel Example: User Story 1 (Containerization)

```bash
# Launch Dockerfile generation in parallel:
Task: "Generate optimized Dockerfile for Next.js frontend using Gordon AI in frontend/Dockerfile"
Task: "Create .dockerignore file for frontend in frontend/.dockerignore"
Task: "Generate optimized Dockerfile for FastAPI backend using Gordon AI in backend/Dockerfile"
Task: "Create .dockerignore file for backend in backend/.dockerignore"
```

## Parallel Example: User Story 2 (Helm Charts)

```bash
# Launch frontend Helm chart creation in parallel:
Task: "Create frontend Chart.yaml with metadata in helm/todo-frontend/Chart.yaml"
Task: "Create frontend values.yaml with parameterized config in helm/todo-frontend/values.yaml"
Task: "Create frontend Deployment template in helm/todo-frontend/templates/deployment.yaml"
Task: "Create frontend Service template (NodePort) in helm/todo-frontend/templates/service.yaml"

# Launch backend Helm chart creation in parallel:
Task: "Create backend Chart.yaml with metadata in helm/todo-backend/Chart.yaml"
Task: "Create backend values.yaml with parameterized config in helm/todo-backend/values.yaml"
Task: "Create backend Deployment template in helm/todo-backend/templates/deployment.yaml"
Task: "Create backend Service template (ClusterIP) in helm/todo-backend/templates/service.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Containerization)
4. **STOP and VALIDATE**: Test Docker images locally
5. Verify images work identically to non-containerized version

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Docker images validated (MVP!)
3. Add User Story 2 → Test independently → Kubernetes deployment working
4. Add User Story 3 → Test independently → Scaling and resilience validated
5. Complete Polish → Documentation and demo ready → Submit

### Sequential Execution (Recommended)

With Phase 4 dependencies:

1. Complete Setup + Foundational together
2. Complete User Story 1 (Containerization) - REQUIRED for US2
3. Complete User Story 2 (Deployment) - REQUIRED for US3
4. Complete User Story 3 (Scaling) - Final validation
5. Complete Polish - Documentation and submission

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- User Story 2 DEPENDS on User Story 1 (needs Docker images)
- User Story 3 DEPENDS on User Story 2 (needs deployed application)
- Commit after each completed user story
- Stop at any checkpoint to validate story independently
- All 5 Phase 4 agents must be utilized:
  - docker-builder (US1: T015-T030)
  - helm-chart-builder (US2: T031-T054)
  - k8s-ai-deployer (US2: T055-T071)
  - k8s-deployment-tester (US2: T072-T091, US3: T092-T128)
  - k8s-orchestrator (coordination across all phases)
