# Kubernetes Architecture Specification

**Feature**: Phase 4 Local Kubernetes Deployment
**Branch**: `001-k8s-deployment`
**Created**: 2026-02-10
**Status**: Draft

## Overview

This document defines the complete Kubernetes architecture for deploying the Phase 3 AI Todo Chatbot application to a local Minikube cluster. It covers containerization strategy, Helm chart structure, resource management, and integration with AI-powered deployment tools.

## Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOST MACHINE (Windows)                        │
├─────────────────────────────────────────────────────────────────┤
│  Docker Desktop                                                  │
│  ├─ Container Runtime                                           │
│  └─ Image Registry (local)                                      │
│                                                                  │
│  Minikube Cluster (VM or Container)                            │
│  ├─ 2 CPU cores, 4GB RAM                                       │
│  └─ Kubernetes v1.28+                                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  KUBERNETES CLUSTER (Minikube)                   │
├─────────────────────────────────────────────────────────────────┤
│  Namespace: todo-app                                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Frontend Deployment                                     │  │
│  │  ├─ Replicas: 2 (configurable)                         │  │
│  │  ├─ Image: todo-frontend:latest                        │  │
│  │  ├─ Port: 3000                                          │  │
│  │  ├─ Resources: 256Mi RAM, 0.25 CPU (request)          │  │
│  │  │             512Mi RAM, 0.5 CPU (limit)             │  │
│  │  ├─ Liveness Probe: HTTP GET /api/health              │  │
│  │  ├─ Readiness Probe: HTTP GET /api/health             │  │
│  │  └─ Env: NEXT_PUBLIC_API_URL (from ConfigMap)         │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Frontend Service (NodePort)                            │  │
│  │  ├─ Type: NodePort                                      │  │
│  │  ├─ Port: 3000 → NodePort: 30080                       │  │
│  │  └─ Selector: app=todo-frontend                        │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Backend Deployment                                      │  │
│  │  ├─ Replicas: 2 (configurable)                         │  │
│  │  ├─ Image: todo-backend:latest                         │  │
│  │  ├─ Port: 8000                                          │  │
│  │  ├─ Resources: 512Mi RAM, 0.5 CPU (request)           │  │
│  │  │             1Gi RAM, 1 CPU (limit)                 │  │
│  │  ├─ Liveness Probe: HTTP GET /health                  │  │
│  │  ├─ Readiness Probe: HTTP GET /health                 │  │
│  │  └─ Env: DATABASE_URL, COHERE_API_KEY (from Secrets)  │  │
│  │         BETTER_AUTH_SECRET (from Secrets)              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Backend Service (ClusterIP)                            │  │
│  │  ├─ Type: ClusterIP                                     │  │
│  │  ├─ Port: 8000                                          │  │
│  │  └─ Selector: app=todo-backend                         │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  ConfigMap: todo-config                                 │  │
│  │  ├─ NEXT_PUBLIC_API_URL: http://backend:8000          │  │
│  │  └─ LOG_LEVEL: info                                    │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Secret: todo-secrets                                   │  │
│  │  ├─ DATABASE_URL: postgresql://...                     │  │
│  │  ├─ COHERE_API_KEY: <encrypted>                        │  │
│  │  └─ BETTER_AUTH_SECRET: <encrypted>                    │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
├─────────────────────────────────────────────────────────────────┤
│  Neon PostgreSQL (External)                                     │
│  ├─ Host: ep-xxx.us-east-2.aws.neon.tech                      │
│  ├─ Port: 5432                                                  │
│  └─ Database: todo_db                                           │
│                                                                  │
│  Cohere API (External)                                          │
│  ├─ Endpoint: https://api.cohere.ai/v1                         │
│  └─ Model: command-r-plus                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Containerization Strategy

### Frontend Containerization (docker-builder agent)

**Base Image**: Node.js 20 Alpine (multi-stage build)

**Build Stage**:
- Install dependencies with npm ci
- Build Next.js production bundle with npm run build
- Output: .next/ directory with optimized static files

**Production Stage**:
- Copy built files from build stage
- Use minimal Node.js runtime
- Run as non-root user (node:node)
- Expose port 3000
- Health check endpoint: /api/health

**Dockerfile Structure** (generated by docker-builder agent with Gordon AI):
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
USER nextjs
EXPOSE 3000
CMD ["npm", "start"]
```

**Image Optimization**:
- Multi-stage build reduces final image size to <200MB
- .dockerignore excludes node_modules, .git, .env files
- Layer caching optimizes rebuild times
- No secrets or sensitive data in image layers

### Backend Containerization (docker-builder agent)

**Base Image**: Python 3.11 Slim (multi-stage build)

**Build Stage**:
- Install build dependencies
- Install Python packages with pip
- Compile dependencies

**Production Stage**:
- Copy installed packages from build stage
- Use minimal Python runtime
- Run as non-root user (appuser)
- Expose port 8000
- Health check endpoint: /health

**Dockerfile Structure** (generated by docker-builder agent with Gordon AI):
```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Image Optimization**:
- Multi-stage build reduces final image size to <500MB
- .dockerignore excludes __pycache__, .env, .git files
- Slim base image minimizes attack surface
- No root user execution

## Helm Chart Structure (helm-chart-builder agent)

### Chart Organization

```
helm/
├── todo-frontend/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── _helpers.tpl
│   └── .helmignore
└── todo-backend/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── secret.yaml
    │   └── _helpers.tpl
    └── .helmignore
```

### Frontend Helm Chart (helm-chart-builder agent)

**Chart.yaml**:
```yaml
apiVersion: v2
name: todo-frontend
description: Todo App Frontend - Next.js
version: 1.0.0
appVersion: "1.0.0"
```

**values.yaml** (parameterized configuration):
```yaml
replicaCount: 2

image:
  repository: todo-frontend
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: NodePort
  port: 3000
  nodePort: 30080

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5

env:
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"
```

**deployment.yaml** (template):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-frontend.fullname" . }}
  labels:
    app: todo-frontend
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: frontend
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          valueFrom:
            configMapKeyRef:
              name: todo-config
              key: NEXT_PUBLIC_API_URL
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        livenessProbe:
          {{- toYaml .Values.livenessProbe | nindent 10 }}
        readinessProbe:
          {{- toYaml .Values.readinessProbe | nindent 10 }}
```

### Backend Helm Chart (helm-chart-builder agent)

**Chart.yaml**:
```yaml
apiVersion: v2
name: todo-backend
description: Todo App Backend - FastAPI
version: 1.0.0
appVersion: "1.0.0"
```

**values.yaml** (parameterized configuration):
```yaml
replicaCount: 2

image:
  repository: todo-backend
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8000

resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"

livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5

secrets:
  DATABASE_URL: ""  # Set via --set flag or values override
  COHERE_API_KEY: ""
  BETTER_AUTH_SECRET: ""
```

**deployment.yaml** (template):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-backend.fullname" . }}
  labels:
    app: todo-backend
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: backend
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: DATABASE_URL
        - name: COHERE_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: COHERE_API_KEY
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: BETTER_AUTH_SECRET
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        livenessProbe:
          {{- toYaml .Values.livenessProbe | nindent 10 }}
        readinessProbe:
          {{- toYaml .Values.readinessProbe | nindent 10 }}
```

## AI-Powered Deployment Tools

### Gordon AI (docker-builder agent)

**Purpose**: AI-assisted Dockerfile generation and optimization

**Usage**:
- Generate optimized Dockerfiles for frontend and backend
- Suggest best practices (multi-stage builds, security, size optimization)
- Validate Dockerfile syntax and structure
- Recommend base images and layer optimization

**Integration**:
```bash
# docker-builder agent uses Gordon to generate Dockerfiles
gordon generate dockerfile --language nodejs --framework nextjs --output frontend/Dockerfile
gordon generate dockerfile --language python --framework fastapi --output backend/Dockerfile
gordon optimize dockerfile --input frontend/Dockerfile --output frontend/Dockerfile.optimized
```

### kubectl-ai (k8s-ai-deployer agent)

**Purpose**: Natural language Kubernetes operations

**Usage**:
- Deploy applications with natural language commands
- Scale deployments conversationally
- Query cluster status in plain English
- Troubleshoot issues with AI assistance

**Integration**:
```bash
# k8s-ai-deployer agent uses kubectl-ai for deployment
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to 3 replicas"
kubectl-ai "show me all pods in the todo-app namespace"
kubectl-ai "why is the frontend pod crashing?"
```

### kagent (k8s-ai-deployer agent)

**Purpose**: Kubernetes agent for intelligent cluster operations

**Usage**:
- Automated health checks and diagnostics
- Intelligent resource optimization
- Proactive issue detection and remediation
- Deployment validation and testing

**Integration**:
```bash
# k8s-ai-deployer agent uses kagent for cluster management
kagent health-check --namespace todo-app
kagent optimize-resources --deployment todo-frontend
kagent diagnose --pod todo-backend-xyz
kagent validate-deployment --namespace todo-app
```

## Resource Management

### Resource Requests and Limits

**Frontend Pods**:
- Request: 256Mi RAM, 0.25 CPU
- Limit: 512Mi RAM, 0.5 CPU
- Rationale: Next.js static serving is lightweight

**Backend Pods**:
- Request: 512Mi RAM, 0.5 CPU
- Limit: 1Gi RAM, 1 CPU
- Rationale: FastAPI + Cohere API calls require more resources

**Total Cluster Resources** (2 frontend + 2 backend pods):
- Request: 1.5Gi RAM, 1.5 CPU
- Limit: 3Gi RAM, 3 CPU
- Fits within Minikube 4GB RAM allocation

### Quality of Service (QoS)

- **Guaranteed QoS**: Requests = Limits (not used to allow flexibility)
- **Burstable QoS**: Requests < Limits (used for both frontend and backend)
- Allows pods to use extra resources when available
- Prevents resource starvation under load

## Health Checks and Probes

### Liveness Probes

**Purpose**: Detect when a pod is unhealthy and needs restart

**Frontend**:
- HTTP GET /api/health on port 3000
- Initial delay: 30 seconds (allow startup time)
- Period: 10 seconds
- Failure threshold: 3 consecutive failures

**Backend**:
- HTTP GET /health on port 8000
- Initial delay: 30 seconds
- Period: 10 seconds
- Failure threshold: 3 consecutive failures

### Readiness Probes

**Purpose**: Detect when a pod is ready to receive traffic

**Frontend**:
- HTTP GET /api/health on port 3000
- Initial delay: 10 seconds
- Period: 5 seconds
- Failure threshold: 3 consecutive failures

**Backend**:
- HTTP GET /health on port 8000
- Initial delay: 10 seconds
- Period: 5 seconds
- Failure threshold: 3 consecutive failures

**Health Endpoint Implementation** (must be added to applications):
- Frontend: /api/health returns 200 OK with {"status": "healthy"}
- Backend: /health returns 200 OK with {"status": "healthy"}

## Networking and Service Discovery

### Frontend Service (NodePort)

**Type**: NodePort (external access)
**Port**: 3000 (internal)
**NodePort**: 30080 (external)
**Access**: http://<minikube-ip>:30080

**Rationale**: NodePort allows external access from host machine browser

### Backend Service (ClusterIP)

**Type**: ClusterIP (internal only)
**Port**: 8000
**Access**: http://todo-backend:8000 (from within cluster)

**Rationale**: Backend should not be directly accessible from outside cluster

### Service Discovery

- Frontend pods discover backend via Kubernetes DNS: `todo-backend.todo-app.svc.cluster.local`
- Simplified to `todo-backend` within same namespace
- Environment variable: `NEXT_PUBLIC_API_URL=http://todo-backend:8000`

## Configuration Management

### ConfigMaps (Non-Sensitive Data)

**todo-config**:
- NEXT_PUBLIC_API_URL: Backend service URL
- LOG_LEVEL: Logging verbosity
- NODE_ENV: production

**Usage**:
```yaml
env:
- name: NEXT_PUBLIC_API_URL
  valueFrom:
    configMapKeyRef:
      name: todo-config
      key: NEXT_PUBLIC_API_URL
```

### Secrets (Sensitive Data)

**todo-secrets**:
- DATABASE_URL: Neon PostgreSQL connection string
- COHERE_API_KEY: Cohere API key for chatbot
- BETTER_AUTH_SECRET: JWT signing secret

**Usage**:
```yaml
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: todo-secrets
      key: DATABASE_URL
```

**Security**:
- Secrets are base64 encoded (not encrypted by default in Minikube)
- Never commit secrets to version control
- Use --set flags or separate values file for secret injection

## Scaling Strategy

### Horizontal Pod Autoscaling (Optional)

**Frontend HPA**:
- Min replicas: 2
- Max replicas: 5
- Target CPU: 70%
- Target Memory: 80%

**Backend HPA**:
- Min replicas: 2
- Max replicas: 5
- Target CPU: 70%
- Target Memory: 80%

**Manual Scaling** (via kubectl-ai):
```bash
kubectl-ai "scale frontend to 3 replicas"
kubectl-ai "scale backend to 4 replicas"
```

### Stateless Design

- No local state in pods (all state in external database)
- Pods can be killed and recreated without data loss
- Multiple replicas can run simultaneously
- Load balancing across replicas via Kubernetes Service

## Agent Coordination (k8s-orchestrator)

### Deployment Workflow

**Phase 1: Containerization** (docker-builder agent)
1. Generate Dockerfiles with Gordon AI
2. Build frontend Docker image
3. Build backend Docker image
4. Tag images for Minikube registry
5. Load images into Minikube

**Phase 2: Helm Chart Generation** (helm-chart-builder agent)
1. Create frontend Helm chart structure
2. Create backend Helm chart structure
3. Generate deployment templates
4. Generate service templates
5. Generate ConfigMap and Secret templates
6. Validate Helm charts with helm lint

**Phase 3: Deployment** (k8s-ai-deployer agent)
1. Create todo-app namespace
2. Create ConfigMap with kubectl-ai
3. Create Secrets with kubectl-ai
4. Deploy backend with helm install
5. Deploy frontend with helm install
6. Verify deployment with kagent

**Phase 4: Testing** (k8s-deployment-tester agent)
1. Check pod status
2. Verify service endpoints
3. Test application functionality
4. Validate scaling operations
5. Test pod recovery

## Cross-References

- **@specs/001-k8s-deployment/spec.md**: Main Phase 4 specification
- **@specs/001-k8s-deployment/k8s-deployment.md**: Deployment procedures
- **@specs/001-k8s-deployment/k8s-testing.md**: Testing procedures
- **@specs/001-ai-chatbot/chatbot-architecture.md**: Phase 3 architecture to preserve
- **@.claude/agents/docker-builder.md**: Docker containerization agent
- **@.claude/agents/helm-chart-builder.md**: Helm chart generation agent
- **@.claude/agents/k8s-ai-deployer.md**: AI-powered deployment agent
- **@.claude/agents/k8s-orchestrator.md**: Main coordination agent
- **@.claude/agents/k8s-deployment-tester.md**: Testing and validation agent
