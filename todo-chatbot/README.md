# Hackathon App - Helm Chart for Minikube Deployment

This Helm chart deploys the Hackathon Phase 2 application (Next.js Frontend + FastAPI Backend) to a local Minikube Kubernetes cluster.

## Prerequisites

1. **Minikube** installed and running
2. **Helm 3** installed
3. **Docker images** built locally

## Quick Start

### 1. Start Minikube

```bash
minikube start --memory=4096 --cpus=2
```

### 2. Enable Ingress Controller

```bash
minikube addons enable ingress
```

### 3. Build Docker Images (if not already built)

```bash
# Build backend image
docker build -t hackathon-backend:latest ./backend

# Build frontend image
docker build -t hackathon-frontend:latest ./frontend
```

### 4. Load Images into Minikube

```bash
# Load backend image
minikube image load hackathon-backend:latest

# Load frontend image
minikube image load hackathon-frontend:latest

# Verify images are loaded
minikube image list
```

### 5. Deploy with Helm

```bash
# Navigate to the chart directory
cd todo-chatbot

# Install the chart
helm install hackathon-app .

# Or with a custom release name
helm install my-hackathon . --namespace default
```

### 6. Check Deployment Status

```bash
# List releases
helm list

# Check pod status
kubectl get pods

# Check services
kubectl get services

# Check ingress
kubectl get ingress
```

### 7. Access the Application

#### Option A: Via Minikube IP

```bash
# Get Minikube IP
minikube ip

# Add to hosts file (Windows - run as Administrator)
# Open C:\Windows\System32\drivers\etc\hosts and add:
# <minikube-ip> hackathon.local

# Or use minikube tunnel for external access
minikube tunnel
```

#### Option B: Via Port Forward

```bash
# Forward backend port
kubectl port-forward service/hackathon-app-backend 8000:8000

# In another terminal, forward frontend port
kubectl port-forward service/hackathon-app-frontend 3000:3000

# Access at:
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/docs
```

#### Option C: Via Minikube Service Command

```bash
# Open frontend in browser
minikube service hackathon-app-frontend

# Open backend in browser
minikube service hackathon-app-backend
```

## Configuration

### Default Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.image.repository` | Backend Docker image | `hackathon-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.service.port` | Backend service port | `8000` |
| `frontend.image.repository` | Frontend Docker image | `hackathon-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.service.port` | Frontend service port | `3000` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.hosts[0].host` | Ingress hostname | `hackathon.local` |

### Custom Values

Create a `custom-values.yaml` file:

```yaml
backend:
  env:
    DATABASE_URL: "your-database-url"
  
secrets:
  betterAuthSecret: "your-secret-key"
  groqApiKey: "your-groq-api-key"

ingress:
  hosts:
    - host: myapp.local
      paths:
        - path: /
          pathType: Prefix
          backend:
            service: hackathon-frontend
            port: 3000
```

Deploy with custom values:

```bash
helm install hackathon-app . -f custom-values.yaml
```

## Upgrade/Update

```bash
# Upgrade existing deployment
helm upgrade hackathon-app .

# Upgrade with new values
helm upgrade hackathon-app . -f custom-values.yaml

# Rollback to previous version
helm rollback hackathon-app
```

## Uninstall

```bash
# Uninstall the chart
helm uninstall hackathon-app

# Clean up all resources
kubectl delete all -l app.kubernetes.io/instance=hackathon-app
```

## Troubleshooting

### Check Pod Logs

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/component=backend

# Frontend logs
kubectl logs -l app.kubernetes.io/component=frontend

# Follow logs in real-time
kubectl logs -f -l app.kubernetes.io/component=backend
```

### Describe Resources

```bash
# Describe pod
kubectl describe pod <pod-name>

# Describe deployment
kubectl describe deployment hackathon-app-backend

# Describe service
kubectl describe service hackathon-app-backend
```

### Test Connection

```bash
# Run Helm test
helm test hackathon-app
```

### Common Issues

#### ImagePullBackOff

Make sure images are loaded into Minikube:

```bash
minikube image load hackathon-backend:latest
minikube image load hackathon-frontend:latest
```

#### Ingress Not Working

1. Ensure ingress addon is enabled:
   ```bash
   minikube addons enable ingress
   ```

2. Add host entry to `/etc/hosts` or `C:\Windows\System32\drivers\etc\hosts`:
   ```
   <minikube-ip> hackathon.local
   ```

#### Database Connection Failed

Check the DATABASE_URL in `values.yaml` and ensure it's correct.

## Architecture

```
                    ┌─────────────────┐
                    │     Ingress     │
                    │  (nginx)        │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼─────────┐       ┌──────────▼──────────┐
    │    Frontend       │       │      Backend        │
    │   (Next.js)       │       │    (FastAPI)        │
    │   Port: 3000      │       │    Port: 8000       │
    └───────────────────┘       └──────────┬──────────┘
                                           │
                                   ┌───────▼────────┐
                                   │    Database    │
                                   │   (Neon PG)    │
                                   └────────────────┘
```

## Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
