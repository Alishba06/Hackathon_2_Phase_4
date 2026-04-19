# Minikube Deployment Script for Hackathon App (PowerShell)
# Run this script to deploy the application to Minikube on Windows

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Hackathon App - Minikube Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Function to check if minikube is running
function Test-MinikubeRunning {
    try {
        $status = minikube status 2>&1
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Check if minikube is running
Write-Host "[INFO] Checking Minikube status..." -ForegroundColor Green
if (-not (Test-MinikubeRunning)) {
    Write-Host "[WARN] Minikube is not running. Starting Minikube..." -ForegroundColor Yellow
    minikube start --memory=4096 --cpus=2
} else {
    Write-Host "[INFO] Minikube is already running" -ForegroundColor Green
}

# Enable ingress addon
Write-Host "[INFO] Enabling Ingress addon..." -ForegroundColor Green
minikube addons enable ingress

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ChartDir = Join-Path $ScriptDir "todo-chatbot"

# Check if chart directory exists
if (-not (Test-Path $ChartDir)) {
    Write-Host "[ERROR] Chart directory not found: $ChartDir" -ForegroundColor Red
    exit 1
}

Set-Location $ChartDir

# Load images into Minikube
Write-Host "[INFO] Loading Docker images into Minikube..." -ForegroundColor Green
minikube image load hackathon-backend:latest
minikube image load hackathon-frontend:latest

# Verify images
Write-Host "[INFO] Verifying loaded images..." -ForegroundColor Green
minikube image list | Select-String "hackathon"

# Check if Helm release exists
$helmList = helm list 2>&1
if ($helmList -match "hackathon-app") {
    Write-Host "[WARN] Existing deployment found. Upgrading..." -ForegroundColor Yellow
    helm upgrade hackathon-app . --wait --timeout=5m
} else {
    Write-Host "[INFO] Installing Helm chart..." -ForegroundColor Green
    helm install hackathon-app . --wait --timeout=5m
}

# Wait for deployment
Write-Host "[INFO] Waiting for deployments to be ready..." -ForegroundColor Green
Write-Host "[INFO] This may take a few minutes for the first time..." -ForegroundColor Yellow

# Check deployment status
Write-Host ""
Write-Host "=== Checking Deployment Status ===" -ForegroundColor Cyan
kubectl get deployments -l app.kubernetes.io/instance=hackathon-app

Write-Host ""
Write-Host "=== Checking Pods ===" -ForegroundColor Cyan
kubectl get pods -l app.kubernetes.io/instance=hackathon-app

# Wait with longer timeout
kubectl wait --for=condition=available deployment/hackathon-app-backend --timeout=300s
kubectl wait --for=condition=available deployment/hackathon-app-frontend --timeout=300s

# Show status
Write-Host ""
Write-Host "[INFO] Deployment complete! Showing status..." -ForegroundColor Green
Write-Host ""
Write-Host "=== Pods ===" -ForegroundColor Cyan
kubectl get pods -l app.kubernetes.io/instance=hackathon-app

Write-Host ""
Write-Host "=== Services ===" -ForegroundColor Cyan
kubectl get services -l app.kubernetes.io/instance=hackathon-app

Write-Host ""
Write-Host "=== Ingress ===" -ForegroundColor Cyan
kubectl get ingress -l app.kubernetes.io/instance=hackathon-app

Write-Host ""
Write-Host "[INFO] Getting Minikube IP..." -ForegroundColor Green
$MinikubeIP = minikube ip
Write-Host "[INFO] Minikube IP: $MinikubeIP" -ForegroundColor Green

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  OPTION 1: Add to hosts file (Run as Administrator):" -ForegroundColor White
Write-Host "     $MinikubeIP hackathon.local" -ForegroundColor Gray
Write-Host "     Location: C:\Windows\System32\drivers\etc\hosts" -ForegroundColor Gray
Write-Host "     Then open: http://hackathon.local" -ForegroundColor Gray
Write-Host ""
Write-Host "  OPTION 2: Use port-forward (Recommended for testing):" -ForegroundColor White
Write-Host "     kubectl port-forward service/hackathon-app-frontend 3000:3000" -ForegroundColor Gray
Write-Host "     Then open: http://localhost:3000" -ForegroundColor Gray
Write-Host ""
Write-Host "  OPTION 3: Use minikube service command:" -ForegroundColor White
Write-Host "     minikube service hackathon-app-frontend --url" -ForegroundColor Gray
Write-Host "     minikube service hackathon-app-backend --url" -ForegroundColor Gray
Write-Host ""
Write-Host "  OPTION 4: Use minikube tunnel (for LoadBalancer):" -ForegroundColor White
Write-Host "     minikube tunnel" -ForegroundColor Gray
Write-Host ""
Write-Host "Troubleshooting:" -ForegroundColor Yellow
Write-Host "  - View logs: kubectl logs -l app.kubernetes.io/instance=hackathon-app" -ForegroundColor Gray
Write-Host "  - Check events: kubectl get events --sort-by='.lastTimestamp'" -ForegroundColor Gray
Write-Host "  - Restart pods: kubectl rollout restart deployment/hackathon-app-backend" -ForegroundColor Gray
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
