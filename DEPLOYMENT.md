# Kubernetes Deployment Guide - Todo App

## Overview

This guide provides detailed instructions for deploying the Todo App to a local Kubernetes cluster using Minikube and Helm.

## Architecture

### Components
- **Frontend**: Next.js 16+ application (2 replicas)
- **Backend**: FastAPI application (2 replicas)
- **Database**: External Neon PostgreSQL (not in-cluster)
- **Services**:
  - Frontend: NodePort (30080) for external access
  - Backend: ClusterIP (8000) for internal communication

### Resource Allocation
- **Frontend Pods**: 256Mi/512Mi RAM, 0.25/0.5 CPU (request/limit)
- **Backend Pods**: 512Mi/1Gi RAM, 0.5/1 CPU (request/limit)
- **Total Cluster**: ~3Gi RAM, ~3 CPU (with 2 replicas each)

## Prerequisites

### Required Tools
1. **Docker Desktop** or **Docker Engine**
   - Version: 28.5.1+
   - Running and accessible

2. **Minikube**
   - Version: v1.38.0+
   - Installation: https://minikube.sigs.k8s.io/docs/start/

3. **kubectl**
   - Version: v1.34.0+
   - Installation: https://kubernetes.io/docs/tasks/tools/

4. **Helm**
   - Version: v4.1.0+
   - Installation: https://helm.sh/docs/intro/install/

### Environment Variables
You'll need the following credentials:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `COHERE_API_KEY`: Cohere API key for chatbot
- `BETTER_AUTH_SECRET`: Better Auth secret key
- `JWT_SECRET`: JWT signing secret

## Step-by-Step Deployment

### Step 1: Start Minikube Cluster

```bash
# Start Minikube with required resources
minikube start --cpus=2 --memory=4096 --driver=docker

# Verify cluster is running
minikube status
kubectl cluster-info
```

### Step 2: Configure Docker Environment

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Verify configuration
docker ps
```

### Step 3: Build Docker Images

```bash
# Navigate to project root
cd /path/to/Phase4-KubernetesDeployment

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .

# Build backend image
cd ../backend
docker build -t todo-backend:latest .

# Verify images
docker images | grep todo
```

**Expected Output:**
```
todo-frontend   latest   <image-id>   <time>   280MB
todo-backend    latest   <image-id>   <time>   282MB
```

### Step 4: Create Kubernetes Namespace

```bash
# Create dedicated namespace
kubectl create namespace todo-app

# Set as default namespace
kubectl config set-context --current --namespace=todo-app

# Verify namespace
kubectl get namespace todo-app
```

### Step 5: Deploy Backend

```bash
# Deploy backend with Helm
helm install todo-backend helm/todo-backend \
  --set secrets.DATABASE_URL="postgresql://user:pass@host/db?sslmode=require" \
  --set secrets.COHERE_API_KEY="your-cohere-api-key" \
  --set secrets.BETTER_AUTH_SECRET="your-auth-secret" \
  --set secrets.JWT_SECRET="your-jwt-secret" \
  --namespace todo-app

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=120s

# Verify deployment
kubectl get pods -l app=todo-backend -n todo-app
```

**Expected Output:**
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-xxxxxxxxxx-xxxxx   1/1     Running   0          60s
todo-backend-xxxxxxxxxx-xxxxx   1/1     Running   0          60s
```

### Step 6: Deploy Frontend

```bash
# Deploy frontend with Helm
helm install todo-frontend helm/todo-frontend --namespace todo-app

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=120s

# Verify deployment
kubectl get pods -l app=todo-frontend -n todo-app
```

**Expected Output:**
```
NAME                             READY   STATUS    RESTARTS   AGE
todo-frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          60s
todo-frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          60s
```

### Step 7: Access the Application

```bash
# Get Minikube IP
minikube ip

# Access application at http://<minikube-ip>:30080
# Or use Minikube service command
minikube service todo-frontend --url -n todo-app
```

## Verification and Testing

### Health Checks

```bash
# Test backend health endpoint (from within cluster)
kubectl run curl-test --image=curlimages/curl --rm -i --restart=Never -n todo-app \
  -- curl -s http://todo-backend:8000/health

# Test frontend health endpoint
kubectl run curl-test --image=curlimages/curl --rm -i --restart=Never -n todo-app \
  -- curl -s http://todo-frontend:3000/api/health
```

### Pod Status

```bash
# Check all pods
kubectl get pods -n todo-app

# Get detailed pod information
kubectl get pods -n todo-app -o wide

# Check pod events
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Resource Usage

```bash
# Check resource consumption
kubectl top pods -n todo-app

# Check resource limits
kubectl describe pods -n todo-app | grep -A 5 "Limits:"
```

### Logs

```bash
# View backend logs
kubectl logs -l app=todo-backend -n todo-app --tail=50

# View frontend logs
kubectl logs -l app=todo-frontend -n todo-app --tail=50

# Follow logs in real-time
kubectl logs -l app=todo-backend -n todo-app -f
```

## Scaling Operations

### Scale Up

```bash
# Scale frontend to 3 replicas
kubectl scale deployment todo-frontend --replicas=3 -n todo-app

# Scale backend to 3 replicas
kubectl scale deployment todo-backend --replicas=3 -n todo-app

# Verify scaling
kubectl get deployment -n todo-app
```

### Scale Down

```bash
# Scale back to 1 replica
kubectl scale deployment todo-frontend --replicas=1 -n todo-app
kubectl scale deployment todo-backend --replicas=1 -n todo-app
```

## Updating Deployments

### Update Docker Images

```bash
# Rebuild images with changes
eval $(minikube docker-env)
cd frontend && docker build -t todo-frontend:latest .
cd ../backend && docker build -t todo-backend:latest .

# Restart deployments to use new images
kubectl rollout restart deployment/todo-frontend -n todo-app
kubectl rollout restart deployment/todo-backend -n todo-app

# Monitor rollout status
kubectl rollout status deployment/todo-frontend -n todo-app
kubectl rollout status deployment/todo-backend -n todo-app
```

### Update Helm Configuration

```bash
# Update backend secrets
helm upgrade todo-backend helm/todo-backend \
  --set secrets.DATABASE_URL="new-database-url" \
  --namespace todo-app

# Update frontend configuration
helm upgrade todo-frontend helm/todo-frontend \
  --set env.NEXT_PUBLIC_API_URL="http://new-backend-url" \
  --namespace todo-app
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n todo-app

# Check pod logs
kubectl logs <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --field-selector involvedObject.name=<pod-name>
```

### CrashLoopBackOff

Common causes:
1. **Missing environment variables**: Check secrets and configmaps
2. **Database connection failure**: Verify DATABASE_URL is correct
3. **Image pull errors**: Ensure images are in Minikube's Docker daemon

```bash
# Check secrets
kubectl get secret todo-backend-secret -n todo-app -o yaml

# Check configmaps
kubectl get configmap todo-frontend-config -n todo-app -o yaml

# Test database connectivity
kubectl run psql-test --image=postgres:15 --rm -i --restart=Never -n todo-app \
  -- psql "your-database-url" -c "SELECT 1"
```

### Service Not Accessible

```bash
# Check service configuration
kubectl get svc -n todo-app

# Check service endpoints
kubectl get endpoints -n todo-app

# Test service from within cluster
kubectl run curl-test --image=curlimages/curl --rm -i --restart=Never -n todo-app \
  -- curl -v http://todo-backend:8000/health
```

### Image Pull Errors

```bash
# Verify images exist in Minikube
eval $(minikube docker-env)
docker images | grep todo

# If images are missing, rebuild them
cd frontend && docker build -t todo-frontend:latest .
cd ../backend && docker build -t todo-backend:latest .
```

## Cleanup

### Uninstall Applications

```bash
# Uninstall Helm releases
helm uninstall todo-frontend -n todo-app
helm uninstall todo-backend -n todo-app

# Delete namespace
kubectl delete namespace todo-app
```

### Stop Minikube

```bash
# Stop cluster
minikube stop

# Delete cluster (removes all data)
minikube delete
```

## Production Considerations

### Security
- Store secrets in Kubernetes Secrets (encrypted at rest)
- Use RBAC for access control
- Enable network policies for pod-to-pod communication
- Scan images for vulnerabilities

### High Availability
- Run multiple replicas (minimum 3 for production)
- Use pod anti-affinity to spread pods across nodes
- Configure horizontal pod autoscaling (HPA)
- Set up liveness and readiness probes (already configured)

### Monitoring
- Deploy Prometheus for metrics collection
- Use Grafana for visualization
- Set up alerting for critical issues
- Monitor resource usage and set appropriate limits

### Backup and Recovery
- Regular database backups
- Document disaster recovery procedures
- Test recovery processes regularly

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## Support

For issues or questions:
1. Check pod logs: `kubectl logs <pod-name> -n todo-app`
2. Review events: `kubectl get events -n todo-app`
3. Verify configuration: `kubectl describe deployment <deployment-name> -n todo-app`
4. Check resource usage: `kubectl top pods -n todo-app`
