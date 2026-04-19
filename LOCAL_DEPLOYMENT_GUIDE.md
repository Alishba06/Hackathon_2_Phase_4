# Local Minikube Deployment Guide

This guide provides step-by-step instructions for deploying the Hackathon Phase 2 application (Next.js Frontend + FastAPI Backend) to Minikube.

## Prerequisites

Before deploying, ensure you have the following installed:

- **Minikube** v1.30+ - Local Kubernetes cluster
- **Helm** v3.10+ - Kubernetes package manager
- **kubectl** - Kubernetes CLI
- **Docker** - For building container images

## Quick Start

### Step 1: Build Docker Images

Build the backend and frontend Docker images:

```bash
# Build backend image
docker build -t hackathon-backend:latest -f backend/Dockerfile backend/

# Build frontend image
docker build -t hackathon-frontend:latest -f frontend/Dockerfile frontend/
```

### Step 2: Start Minikube

```bash
# Start Minikube with adequate resources
minikube start --memory=4096 --cpus=2

# Enable ingress addon
minikube addons enable ingress
```

### Step 3: Load Images into Minikube

```bash
# Load backend image
minikube image load hackathon-backend:latest

# Load frontend image
minikube image load hackathon-frontend:latest

# Verify images are loaded
minikube image list | grep hackathon
```

### Step 4: Deploy Using Helm

#### Option A: Using Deployment Scripts (Recommended)

**Windows (PowerShell):**
```powershell
.\deploy-minikube.ps1
```

**Linux/Mac (Bash):**
```bash
chmod +x deploy-minikube.sh
./deploy-minikube.sh
```

#### Option B: Manual Helm Commands

```bash
cd todo-chatbot

# Install Helm chart
helm install hackathon-app . --wait --timeout=5m

# Or upgrade if already installed
helm upgrade hackathon-app . --wait --timeout=5m
```

#### Option C: Using Kubernetes Manifests (Without Helm)

```bash
kubectl apply -f todo-chatbot/k8s-manifests.yaml
```

### Step 5: Verify Deployment

```bash
# Check pods
kubectl get pods -l app.kubernetes.io/instance=hackathon-app

# Check services
kubectl get services -l app.kubernetes.io/instance=hackathon-app

# Check ingress
kubectl get ingress -l app.kubernetes.io/instance=hackathon-app

# Wait for deployments to be ready
kubectl wait --for=condition=available deployment/hackathon-app-backend --timeout=300s
kubectl wait --for=condition=available deployment/hackathon-app-frontend --timeout=300s
```

## Accessing the Application

### Option 1: Port Forward (Recommended for Testing)

```bash
# Forward frontend port
kubectl port-forward service/hackathon-app-frontend 3000:3000

# In another terminal, forward backend port (optional)
kubectl port-forward service/hackathon-app-backend 8000:8000
```

Then open: **http://localhost:3000**

### Option 2: Minikube Service Command

```bash
# Get frontend URL
minikube service hackathon-app-frontend --url

# Get backend URL
minikube service hackathon-app-backend --url

# Or open in browser automatically
minikube service hackathon-app-frontend
```

### Option 3: Ingress with Host File

1. Get Minikube IP:
   ```bash
   minikube ip
   ```

2. Add to hosts file:
   
   **Windows (Run PowerShell as Administrator):**
   ```powershell
   # Add to C:\Windows\System32\drivers\etc\hosts
   <MINIKUBE_IP> hackathon.local
   ```
   
   **Linux/Mac:**
   ```bash
   # Add to /etc/hosts
   sudo echo "<MINIKUBE_IP> hackathon.local" >> /etc/hosts
   ```

3. Open in browser: **http://hackathon.local**

### Option 4: Minikube Tunnel (For LoadBalancer)

```bash
# Start tunnel in a separate terminal
minikube tunnel

# Access via LoadBalancer IP
```

## Configuration

### Environment Variables

The application is configured via `todo-chatbot/values.yaml`. Key configurations:

#### Backend Configuration

```yaml
backend:
  env:
    DATABASE_URL: "postgresql://..."  # Your Neon database URL
    BACKEND_CORS_ORIGINS: '["http://localhost:3000"]'
    USE_GROQ: "true"
```

#### Frontend Configuration

```yaml
frontend:
  env:
    NEXT_PUBLIC_API_BASE_URL: "http://hackathon-app-backend:8000"
    NEXT_PUBLIC_BETTER_AUTH_URL: "http://hackathon-app-backend:8000/api/auth"
```

### Updating Configuration

1. Edit `todo-chatbot/values.yaml`
2. Redeploy:
   ```bash
   helm upgrade hackathon-app todo-chatbot --wait
   ```

## Monitoring and Troubleshooting

### View Logs

```bash
# View all application logs
kubectl logs -l app.kubernetes.io/instance=hackathon-app

# View backend logs
kubectl logs -l app.kubernetes.io/component=backend

# View frontend logs
kubectl logs -l app.kubernetes.io/component=frontend

# Follow logs in real-time
kubectl logs -f -l app.kubernetes.io/instance=hackathon-app
```

### Check Events

```bash
# View recent events
kubectl get events --sort-by='.lastTimestamp'

# View events for specific resource
kubectl describe deployment/hackathon-app-backend
```

### Restart Deployments

```bash
# Restart backend
kubectl rollout restart deployment/hackathon-app-backend

# Restart frontend
kubectl rollout restart deployment/hackathon-app-frontend
```

### Debug Pod Issues

```bash
# Describe pod for detailed information
kubectl describe pod <pod-name>

# Execute into pod for debugging
kubectl exec -it <pod-name> -- /bin/sh

# Check pod logs
kubectl logs <pod-name>
```

## Managing the Deployment

### Upgrade Deployment

```bash
# Upgrade with new images
minikube image load hackathon-backend:latest
minikube image load hackathon-frontend:latest
helm upgrade hackathon-app todo-chatbot --wait
```

### Rollback Deployment

```bash
# View rollout history
kubectl rollout history deployment/hackathon-app-backend

# Rollback to previous version
kubectl rollout undo deployment/hackathon-app-backend
```

### Scale Deployment

```bash
# Scale backend replicas
kubectl scale deployment/hackathon-app-backend --replicas=2
```

### Uninstall Deployment

```bash
# Uninstall Helm release
helm uninstall hackathon-app

# Or delete all resources
kubectl delete -f todo-chatbot/k8s-manifests.yaml
```

## Health Checks

### Backend Health Endpoint

```bash
# Test backend health
kubectl port-forward service/hackathon-app-backend 8000:8000
curl http://localhost:8000/health
```

### Frontend Health

```bash
# Test frontend
kubectl port-forward service/hackathon-app-frontend 3000:3000
curl http://localhost:3000/
```

## Common Issues and Solutions

### Issue: ImagePullBackOff

**Solution:** Ensure images are loaded into Minikube:
```bash
minikube image load hackathon-backend:latest
minikube image load hackathon-frontend:latest
```

### Issue: CrashLoopBackOff

**Solution:** Check logs and environment variables:
```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

### Issue: Ingress Not Working

**Solution:** Ensure ingress addon is enabled:
```bash
minikube addons enable ingress
minikube addons list | grep ingress
```

### Issue: Service Not Accessible

**Solution:** Use port-forward or minikube service:
```bash
kubectl port-forward service/hackathon-app-frontend 3000:3000
# or
minikube service hackathon-app-frontend --url
```

### Issue: Database Connection Errors

**Solution:** Verify DATABASE_URL in values.yaml is correct and accessible from the cluster.

## Resource Limits

The application is configured with the following resource limits for Minikube:

### Backend
- CPU: 250m - 1000m
- Memory: 512Mi - 1024Mi

### Frontend
- CPU: 250m - 1000m
- Memory: 512Mi - 1024Mi

Adjust these in `values.yaml` based on your Minikube resources.

## Next Steps

After successful deployment:

1. **Test Authentication**: Sign up and login
2. **Test TODO Operations**: Create, read, update, delete tasks
3. **Test AI Chatbot**: Interact with the AI todo assistant
4. **Monitor Performance**: Check resource usage and response times

## Support

For issues or questions:
- Check application logs: `kubectl logs -l app.kubernetes.io/instance=hackathon-app`
- Review Helm values: `helm get values hackathon-app`
- Inspect Kubernetes resources: `kubectl get all -l app.kubernetes.io/instance=hackathon-app`

---

**Deployment Checklist:**
- [ ] Minikube is running
- [ ] Ingress addon is enabled
- [ ] Docker images are built
- [ ] Images are loaded into Minikube
- [ ] Helm chart is installed/upgraded
- [ ] Deployments are ready
- [ ] Services are accessible
- [ ] Health checks pass
- [ ] Application is accessible via browser
