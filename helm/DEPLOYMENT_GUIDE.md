# Helm Charts Deployment Guide

This guide provides instructions for deploying the Todo App to Kubernetes using Helm charts.

## Prerequisites

- Minikube installed and running
- kubectl configured to access Minikube cluster
- Helm 3.x installed
- Docker images built and loaded into Minikube:
  - `todo-frontend:latest`
  - `todo-backend:latest`

## Chart Structure

```
helm/
├── todo-frontend/          # Frontend Helm chart
│   ├── Chart.yaml         # Chart metadata
│   ├── values.yaml        # Configuration values
│   ├── .helmignore        # Files to ignore
│   └── templates/
│       ├── _helpers.tpl   # Template helpers
│       ├── deployment.yaml # Deployment resource
│       ├── service.yaml   # NodePort service (port 30080)
│       ├── configmap.yaml # Environment configuration
│       └── NOTES.txt      # Post-install instructions
│
└── todo-backend/           # Backend Helm chart
    ├── Chart.yaml         # Chart metadata
    ├── values.yaml        # Configuration values
    ├── .helmignore        # Files to ignore
    └── templates/
        ├── _helpers.tpl   # Template helpers
        ├── deployment.yaml # Deployment resource
        ├── service.yaml   # ClusterIP service (port 8000)
        ├── secret.yaml    # Sensitive data (secrets)
        └── NOTES.txt      # Post-install instructions
```

## Quick Start

### 1. Validate Charts

```bash
# Lint the charts to check for issues
helm lint helm/todo-frontend
helm lint helm/todo-backend

# Test chart rendering without installing
helm template todo-frontend helm/todo-frontend
helm template todo-backend helm/todo-backend
```

### 2. Deploy Backend

The backend must be deployed first as the frontend depends on it.

```bash
# Deploy backend with default values
helm install todo-backend helm/todo-backend \
  --set secrets.DATABASE_URL="your-database-url" \
  --set secrets.COHERE_API_KEY="your-cohere-api-key" \
  --set secrets.BETTER_AUTH_SECRET="your-auth-secret" \
  --set secrets.JWT_SECRET="your-jwt-secret"

# Verify backend deployment
kubectl get pods -l app=todo-backend
kubectl get svc todo-backend
```

### 3. Deploy Frontend

```bash
# Deploy frontend with default values
helm install todo-frontend helm/todo-frontend

# Verify frontend deployment
kubectl get pods -l app=todo-frontend
kubectl get svc todo-frontend
```

### 4. Access the Application

```bash
# Get Minikube IP
minikube ip

# Access frontend at http://<minikube-ip>:30080
# Or use Minikube service command
minikube service todo-frontend --url
```

## Configuration

### Frontend Configuration (values.yaml)

```yaml
replicaCount: 2                    # Number of frontend pods
image:
  repository: todo-frontend        # Image name
  tag: latest                      # Image tag
  pullPolicy: Never                # Use local images

service:
  type: NodePort                   # External access
  port: 3000                       # Internal port
  nodePort: 30080                  # External port

resources:
  requests:
    cpu: 250m                      # Guaranteed CPU
    memory: 256Mi                  # Guaranteed memory
  limits:
    cpu: 500m                      # Maximum CPU
    memory: 512Mi                  # Maximum memory

env:
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"
  NODE_ENV: "production"
  LOG_LEVEL: "info"
```

### Backend Configuration (values.yaml)

```yaml
replicaCount: 2                    # Number of backend pods
image:
  repository: todo-backend         # Image name
  tag: latest                      # Image tag
  pullPolicy: Never                # Use local images

service:
  type: ClusterIP                  # Internal only
  port: 8000                       # Service port

resources:
  requests:
    cpu: 500m                      # Guaranteed CPU
    memory: 512Mi                  # Guaranteed memory
  limits:
    cpu: 1000m                     # Maximum CPU
    memory: 1Gi                    # Maximum memory

secrets:
  DATABASE_URL: ""                 # PostgreSQL connection string
  COHERE_API_KEY: ""              # Cohere API key
  BETTER_AUTH_SECRET: ""          # Auth secret
  JWT_SECRET: ""                  # JWT signing secret
```

## Customization

### Override Values at Install Time

```bash
# Override specific values
helm install todo-frontend helm/todo-frontend \
  --set replicaCount=3 \
  --set resources.limits.memory=1Gi

# Use a custom values file
helm install todo-backend helm/todo-backend \
  -f custom-values.yaml
```

### Update Existing Deployment

```bash
# Upgrade with new values
helm upgrade todo-frontend helm/todo-frontend \
  --set replicaCount=3

# Upgrade with new secrets
helm upgrade todo-backend helm/todo-backend \
  --set secrets.DATABASE_URL="new-database-url"
```

## Health Checks

Both charts include liveness and readiness probes:

### Frontend Probes
- **Liveness**: HTTP GET `/api/health` on port 3000
  - Initial delay: 30 seconds
  - Period: 10 seconds
  - Failure threshold: 3

- **Readiness**: HTTP GET `/api/health` on port 3000
  - Initial delay: 10 seconds
  - Period: 5 seconds
  - Failure threshold: 3

### Backend Probes
- **Liveness**: HTTP GET `/health` on port 8000
  - Initial delay: 30 seconds
  - Period: 10 seconds
  - Failure threshold: 3

- **Readiness**: HTTP GET `/health` on port 8000
  - Initial delay: 10 seconds
  - Period: 5 seconds
  - Failure threshold: 3

## Scaling

### Manual Scaling

```bash
# Scale frontend to 3 replicas
helm upgrade todo-frontend helm/todo-frontend \
  --set replicaCount=3

# Scale backend to 4 replicas
helm upgrade todo-backend helm/todo-backend \
  --set replicaCount=4

# Or use kubectl
kubectl scale deployment todo-frontend --replicas=3
kubectl scale deployment todo-backend --replicas=4
```

### Auto-scaling (Optional)

Enable HorizontalPodAutoscaler in values.yaml:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

## Monitoring

### Check Pod Status

```bash
# View all pods
kubectl get pods

# View pods with labels
kubectl get pods -l app=todo-frontend
kubectl get pods -l app=todo-backend

# Describe a pod
kubectl describe pod <pod-name>
```

### View Logs

```bash
# View frontend logs
kubectl logs -l app=todo-frontend --tail=50

# View backend logs
kubectl logs -l app=todo-backend --tail=50

# Follow logs in real-time
kubectl logs -f <pod-name>
```

### Check Resource Usage

```bash
# View resource usage (requires metrics-server)
kubectl top pods
kubectl top nodes

# View specific deployment
kubectl top pods -l app=todo-frontend
kubectl top pods -l app=todo-backend
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check if images are available
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}'
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints todo-frontend
kubectl get endpoints todo-backend

# Test service from within cluster
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -- \
  curl http://todo-backend:8000/health
```

### Configuration Issues

```bash
# View ConfigMap
kubectl get configmap todo-frontend-config -o yaml

# View Secret (base64 encoded)
kubectl get secret todo-backend-secret -o yaml

# Decode secret value
kubectl get secret todo-backend-secret -o jsonpath='{.data.DATABASE_URL}' | base64 -d
```

## Cleanup

### Uninstall Charts

```bash
# Uninstall frontend
helm uninstall todo-frontend

# Uninstall backend
helm uninstall todo-backend

# Verify removal
helm list
kubectl get all
```

### Delete Namespace (if used)

```bash
kubectl delete namespace todo-app
```

## Security Best Practices

1. **Never commit secrets to version control**
   - Use `--set` flags or separate values files
   - Add `*-secrets.yaml` to `.gitignore`

2. **Use strong secrets**
   ```bash
   # Generate secure secrets
   openssl rand -base64 32
   ```

3. **Limit resource access**
   - Backend uses ClusterIP (internal only)
   - Frontend uses NodePort (external access)

4. **Enable security contexts**
   - Run containers as non-root users
   - Set read-only root filesystem (if possible)

5. **Regular updates**
   - Keep images updated
   - Monitor for security vulnerabilities

## Advanced Features

### Using Ingress (Optional)

For production deployments, consider using Ingress instead of NodePort:

```yaml
# values.yaml
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
```

### Using Persistent Volumes (If Needed)

If your application requires persistent storage:

```yaml
# values.yaml
persistence:
  enabled: true
  storageClass: standard
  size: 1Gi
```

### Environment-Specific Configurations

Create separate values files for different environments:

```bash
# Development
helm install todo-backend helm/todo-backend -f values-dev.yaml

# Staging
helm install todo-backend helm/todo-backend -f values-staging.yaml

# Production
helm install todo-backend helm/todo-backend -f values-prod.yaml
```

## Next Steps

1. Deploy to Minikube cluster
2. Test all application features
3. Validate scaling operations
4. Test pod recovery and resilience
5. Monitor resource usage
6. Document any environment-specific configurations

## Support

For issues or questions:
- Check pod logs: `kubectl logs <pod-name>`
- Review Helm release: `helm status <release-name>`
- Consult Kubernetes documentation: https://kubernetes.io/docs/
- Consult Helm documentation: https://helm.sh/docs/

---

**Created**: 2026-02-10
**Version**: 1.0.0
**Helm Chart Versions**: Frontend 0.1.0, Backend 0.1.0
