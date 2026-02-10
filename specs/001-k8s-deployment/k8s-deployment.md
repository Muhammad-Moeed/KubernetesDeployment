# Kubernetes Deployment Specification

**Feature**: Phase 4 Local Kubernetes Deployment
**Branch**: `001-k8s-deployment`
**Created**: 2026-02-10
**Status**: Draft

## Overview

This document provides step-by-step deployment procedures for deploying the Phase 3 AI Todo Chatbot application to a local Minikube cluster. It covers Minikube setup, Docker image building, Helm chart deployment, and AI-powered deployment commands using kubectl-ai and kagent.

## Prerequisites

### Required Tools

- **Docker Desktop**: Version 4.x or higher (Windows/Mac) or Docker Engine (Linux)
- **Minikube**: Version 1.32.x or higher
- **kubectl**: Version 1.28.x or higher
- **Helm**: Version 3.x or higher
- **Gordon AI**: Latest version for Dockerfile generation
- **kubectl-ai**: Latest version for natural language Kubernetes operations
- **kagent**: Latest version for intelligent cluster management

### System Requirements

- **CPU**: Minimum 4 cores (2 cores allocated to Minikube)
- **RAM**: Minimum 8GB (4GB allocated to Minikube)
- **Disk**: Minimum 20GB free space
- **OS**: Windows 10/11, macOS 11+, or Linux

### Environment Variables

Prepare the following environment variables before deployment:

```bash
# Database connection (Neon PostgreSQL)
DATABASE_URL="postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/todo_db?sslmode=require"

# Cohere API key for chatbot
COHERE_API_KEY="your-cohere-api-key"

# Better Auth JWT secret (same as Phase 2/3)
BETTER_AUTH_SECRET="your-jwt-secret-key"
```

## Phase 1: Minikube Setup (k8s-orchestrator agent)

### Step 1.1: Start Minikube Cluster

**Command**:
```bash
minikube start --cpus=2 --memory=4096 --driver=docker
```

**Expected Output**:
```
😄  minikube v1.32.0 on Windows 11
✨  Using the docker driver based on user configuration
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔥  Creating docker container (CPUs=2, Memory=4096MB) ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster
```

**Verification**:
```bash
kubectl cluster-info
kubectl get nodes
```

**Expected Output**:
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.28.3
```

### Step 1.2: Enable Required Addons

**Command**:
```bash
minikube addons enable metrics-server
minikube addons enable ingress
```

**Verification**:
```bash
minikube addons list | grep -E "metrics-server|ingress"
```

### Step 1.3: Configure kubectl Context

**Command**:
```bash
kubectl config use-context minikube
kubectl config current-context
```

**Expected Output**:
```
minikube
```

### Step 1.4: Create Namespace

**Command** (using kubectl-ai):
```bash
kubectl-ai "create a namespace called todo-app"
```

**Alternative (standard kubectl)**:
```bash
kubectl create namespace todo-app
kubectl config set-context --current --namespace=todo-app
```

**Verification**:
```bash
kubectl get namespaces | grep todo-app
```

## Phase 2: Docker Image Building (docker-builder agent)

### Step 2.1: Generate Dockerfiles with Gordon AI

**Frontend Dockerfile Generation**:
```bash
cd frontend
gordon generate dockerfile \
  --language nodejs \
  --framework nextjs \
  --version 20 \
  --optimize size \
  --security hardened \
  --output Dockerfile
```

**Backend Dockerfile Generation**:
```bash
cd ../backend
gordon generate dockerfile \
  --language python \
  --framework fastapi \
  --version 3.11 \
  --optimize size \
  --security hardened \
  --output Dockerfile
```

**Verification**:
```bash
# Check generated Dockerfiles
cat frontend/Dockerfile
cat backend/Dockerfile
```

### Step 2.2: Create .dockerignore Files

**Frontend .dockerignore**:
```
node_modules
.next
.git
.env
.env.local
.env.*.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
*.md
.vscode
.idea
coverage
.cache
```

**Backend .dockerignore**:
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
*.md
.vscode
.idea
.pytest_cache
.coverage
htmlcov/
```

### Step 2.3: Build Docker Images

**Configure Docker to Use Minikube's Docker Daemon**:
```bash
# Windows PowerShell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Linux/Mac
eval $(minikube docker-env)
```

**Build Frontend Image**:
```bash
cd frontend
docker build -t todo-frontend:latest .
```

**Expected Output**:
```
[+] Building 120.5s (15/15) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 450B
 => [internal] load .dockerignore
 => [stage-1 1/6] FROM docker.io/library/node:20-alpine
 => [builder 2/5] WORKDIR /app
 => [builder 3/5] COPY package*.json ./
 => [builder 4/5] RUN npm ci --only=production
 => [builder 5/5] RUN npm run build
 => [stage-1 2/6] RUN addgroup -g 1001 -S nodejs
 => [stage-1 3/6] COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
 => [stage-1 4/6] COPY --from=builder /app/node_modules ./node_modules
 => [stage-1 5/6] COPY --from=builder /app/package.json ./package.json
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/todo-frontend:latest
```

**Build Backend Image**:
```bash
cd ../backend
docker build -t todo-backend:latest .
```

**Verification**:
```bash
docker images | grep todo
```

**Expected Output**:
```
todo-frontend   latest   abc123   2 minutes ago   180MB
todo-backend    latest   def456   1 minute ago    450MB
```

### Step 2.4: Test Images Locally (Optional)

**Test Frontend**:
```bash
docker run -d -p 3000:3000 --name test-frontend todo-frontend:latest
curl http://localhost:3000
docker stop test-frontend && docker rm test-frontend
```

**Test Backend**:
```bash
docker run -d -p 8000:8000 \
  -e DATABASE_URL="$DATABASE_URL" \
  -e COHERE_API_KEY="$COHERE_API_KEY" \
  -e BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  --name test-backend todo-backend:latest
curl http://localhost:8000/health
docker stop test-backend && docker rm test-backend
```

## Phase 3: Helm Chart Deployment (helm-chart-builder agent)

### Step 3.1: Generate Helm Charts

**Create Helm Chart Directory Structure**:
```bash
mkdir -p helm/todo-frontend helm/todo-backend
```

**Generate Frontend Chart** (helm-chart-builder agent creates these files):
```bash
# Chart.yaml, values.yaml, templates/ are generated by agent
# See k8s-architecture.md for complete chart structure
```

**Generate Backend Chart** (helm-chart-builder agent creates these files):
```bash
# Chart.yaml, values.yaml, templates/ are generated by agent
# See k8s-architecture.md for complete chart structure
```

### Step 3.2: Validate Helm Charts

**Lint Frontend Chart**:
```bash
helm lint helm/todo-frontend
```

**Expected Output**:
```
==> Linting helm/todo-frontend
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```

**Lint Backend Chart**:
```bash
helm lint helm/todo-backend
```

### Step 3.3: Create ConfigMap

**Command** (using kubectl-ai):
```bash
kubectl-ai "create a configmap named todo-config in namespace todo-app with NEXT_PUBLIC_API_URL=http://todo-backend:8000"
```

**Alternative (standard kubectl)**:
```bash
kubectl create configmap todo-config \
  --from-literal=NEXT_PUBLIC_API_URL=http://todo-backend:8000 \
  --namespace=todo-app
```

**Verification**:
```bash
kubectl get configmap todo-config -n todo-app -o yaml
```

### Step 3.4: Create Secrets

**Command** (using kubectl-ai):
```bash
kubectl-ai "create a secret named todo-secrets in namespace todo-app with DATABASE_URL, COHERE_API_KEY, and BETTER_AUTH_SECRET"
```

**Alternative (standard kubectl)**:
```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --from-literal=COHERE_API_KEY="$COHERE_API_KEY" \
  --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  --namespace=todo-app
```

**Verification**:
```bash
kubectl get secret todo-secrets -n todo-app
```

**Security Note**: Never commit secrets to version control. Use environment variables or secure secret management tools.

### Step 3.5: Deploy Backend with Helm

**Command**:
```bash
helm install todo-backend helm/todo-backend \
  --namespace=todo-app \
  --set image.repository=todo-backend \
  --set image.tag=latest \
  --set replicaCount=2
```

**Expected Output**:
```
NAME: todo-backend
LAST DEPLOYED: Mon Feb 10 10:00:00 2026
NAMESPACE: todo-app
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

**Verification**:
```bash
kubectl get pods -n todo-app -l app=todo-backend
```

**Expected Output**:
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-abc123-xyz         1/1     Running   0          30s
todo-backend-abc123-uvw         1/1     Running   0          30s
```

### Step 3.6: Deploy Frontend with Helm

**Command**:
```bash
helm install todo-frontend helm/todo-frontend \
  --namespace=todo-app \
  --set image.repository=todo-frontend \
  --set image.tag=latest \
  --set replicaCount=2
```

**Expected Output**:
```
NAME: todo-frontend
LAST DEPLOYED: Mon Feb 10 10:01:00 2026
NAMESPACE: todo-app
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

**Verification**:
```bash
kubectl get pods -n todo-app -l app=todo-frontend
```

**Expected Output**:
```
NAME                             READY   STATUS    RESTARTS   AGE
todo-frontend-def456-abc         1/1     Running   0          30s
todo-frontend-def456-xyz         1/1     Running   0          30s
```

## Phase 4: AI-Powered Deployment Operations (k8s-ai-deployer agent)

### Step 4.1: Verify Deployment with kubectl-ai

**Check All Pods**:
```bash
kubectl-ai "show me all pods in the todo-app namespace"
```

**Check Services**:
```bash
kubectl-ai "list all services in todo-app namespace"
```

**Check Deployments**:
```bash
kubectl-ai "describe the deployments in todo-app"
```

### Step 4.2: Health Check with kagent

**Run Comprehensive Health Check**:
```bash
kagent health-check --namespace todo-app
```

**Expected Output**:
```
✓ All pods are running
✓ All services are accessible
✓ Resource usage within limits
✓ No error logs detected
✓ Liveness probes passing
✓ Readiness probes passing

Health Status: HEALTHY
```

**Diagnose Specific Pod** (if issues):
```bash
kagent diagnose --pod todo-backend-abc123-xyz --namespace todo-app
```

### Step 4.3: Access Application

**Get Minikube IP**:
```bash
minikube ip
```

**Expected Output**:
```
192.168.49.2
```

**Get Frontend NodePort**:
```bash
kubectl get service todo-frontend -n todo-app -o jsonpath='{.spec.ports[0].nodePort}'
```

**Expected Output**:
```
30080
```

**Access Application**:
```
http://192.168.49.2:30080
```

**Alternative (Minikube Service Command)**:
```bash
minikube service todo-frontend -n todo-app
```

This command automatically opens the application in your default browser.

## Phase 5: Scaling Operations (k8s-ai-deployer agent)

### Step 5.1: Scale Frontend

**Using kubectl-ai**:
```bash
kubectl-ai "scale the todo-frontend deployment to 3 replicas in namespace todo-app"
```

**Alternative (standard kubectl)**:
```bash
kubectl scale deployment todo-frontend --replicas=3 -n todo-app
```

**Verification**:
```bash
kubectl get pods -n todo-app -l app=todo-frontend
```

**Expected Output**:
```
NAME                             READY   STATUS    RESTARTS   AGE
todo-frontend-def456-abc         1/1     Running   0          5m
todo-frontend-def456-xyz         1/1     Running   0          5m
todo-frontend-def456-new         1/1     Running   0          10s
```

### Step 5.2: Scale Backend

**Using kubectl-ai**:
```bash
kubectl-ai "scale the todo-backend deployment to 3 replicas in namespace todo-app"
```

**Verification**:
```bash
kubectl get pods -n todo-app -l app=todo-backend
```

### Step 5.3: Monitor Resource Usage

**Using kagent**:
```bash
kagent monitor-resources --namespace todo-app --duration 60s
```

**Expected Output**:
```
Monitoring resources for 60 seconds...

Frontend Pods:
  Average CPU: 15%
  Average Memory: 180Mi / 512Mi (35%)
  Peak CPU: 25%
  Peak Memory: 220Mi

Backend Pods:
  Average CPU: 40%
  Average Memory: 650Mi / 1Gi (63%)
  Peak CPU: 60%
  Peak Memory: 800Mi

Status: All pods within resource limits ✓
```

## Phase 6: Rolling Updates (k8s-ai-deployer agent)

### Step 6.1: Update Frontend Image

**Build New Image**:
```bash
cd frontend
docker build -t todo-frontend:v1.1 .
```

**Update Deployment**:
```bash
kubectl-ai "update the todo-frontend deployment to use image todo-frontend:v1.1 in namespace todo-app"
```

**Alternative (Helm upgrade)**:
```bash
helm upgrade todo-frontend helm/todo-frontend \
  --namespace=todo-app \
  --set image.tag=v1.1 \
  --reuse-values
```

**Monitor Rollout**:
```bash
kubectl rollout status deployment/todo-frontend -n todo-app
```

**Expected Output**:
```
Waiting for deployment "todo-frontend" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "todo-frontend" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "todo-frontend" rollout to finish: 3 new replicas are available...
deployment "todo-frontend" successfully rolled out
```

### Step 6.2: Rollback (if needed)

**Using kubectl-ai**:
```bash
kubectl-ai "rollback the todo-frontend deployment to the previous version in namespace todo-app"
```

**Alternative (standard kubectl)**:
```bash
kubectl rollout undo deployment/todo-frontend -n todo-app
```

## Phase 7: Troubleshooting Commands

### View Pod Logs

**Using kubectl-ai**:
```bash
kubectl-ai "show me the logs for the todo-backend pod in namespace todo-app"
```

**Alternative (standard kubectl)**:
```bash
kubectl logs -f deployment/todo-backend -n todo-app
```

### Describe Pod

**Using kubectl-ai**:
```bash
kubectl-ai "describe the todo-frontend pod that is crashing in namespace todo-app"
```

**Alternative (standard kubectl)**:
```bash
kubectl describe pod <pod-name> -n todo-app
```

### Execute Commands in Pod

**Using kubectl-ai**:
```bash
kubectl-ai "execute a shell in the todo-backend pod in namespace todo-app"
```

**Alternative (standard kubectl)**:
```bash
kubectl exec -it <pod-name> -n todo-app -- /bin/sh
```

### Check Events

**Using kubectl-ai**:
```bash
kubectl-ai "show me recent events in the todo-app namespace"
```

**Alternative (standard kubectl)**:
```bash
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

## Phase 8: Cleanup

### Step 8.1: Delete Helm Releases

**Delete Frontend**:
```bash
helm uninstall todo-frontend -n todo-app
```

**Delete Backend**:
```bash
helm uninstall todo-backend -n todo-app
```

### Step 8.2: Delete Namespace

**Command**:
```bash
kubectl delete namespace todo-app
```

### Step 8.3: Stop Minikube

**Command**:
```bash
minikube stop
```

### Step 8.4: Delete Minikube Cluster (Optional)

**Command**:
```bash
minikube delete
```

## Agent Coordination Summary

### k8s-orchestrator Agent
- Coordinates all deployment phases
- Manages agent handoffs
- Ensures proper sequencing

### docker-builder Agent
- Generates Dockerfiles with Gordon AI
- Builds and optimizes container images
- Validates image security

### helm-chart-builder Agent
- Creates Helm chart structure
- Generates Kubernetes manifests
- Validates chart syntax

### k8s-ai-deployer Agent
- Executes deployment with kubectl-ai
- Performs scaling operations with kagent
- Monitors cluster health

### k8s-deployment-tester Agent
- Validates deployment success
- Tests application functionality
- Verifies scaling and recovery

## Cross-References

- **@specs/001-k8s-deployment/spec.md**: Main Phase 4 specification
- **@specs/001-k8s-deployment/k8s-architecture.md**: Architecture details
- **@specs/001-k8s-deployment/k8s-testing.md**: Testing procedures
- **@.claude/agents/k8s-orchestrator.md**: Main coordination agent
- **@.claude/agents/docker-builder.md**: Docker containerization agent
- **@.claude/agents/helm-chart-builder.md**: Helm chart generation agent
- **@.claude/agents/k8s-ai-deployer.md**: AI-powered deployment agent
