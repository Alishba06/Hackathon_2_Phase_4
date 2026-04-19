#!/bin/bash
# Minikube Deployment Script for Hackathon App
# Run this script to deploy the application to Minikube

set -e

echo "========================================="
echo "Hackathon App - Minikube Deployment"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_cyan() {
    echo -e "${CYAN}$1${NC}"
}

# Check if minikube is running
print_info "Checking Minikube status..."
if ! minikube status > /dev/null 2>&1; then
    print_error "Minikube is not running. Starting Minikube..."
    minikube start --memory=4096 --cpus=2
else
    print_info "Minikube is already running"
fi

# Enable ingress addon
print_info "Enabling Ingress addon..."
minikube addons enable ingress

# Get the chart directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CHART_DIR="$SCRIPT_DIR/todo-chatbot"

# Check if chart directory exists
if [ ! -d "$CHART_DIR" ]; then
    print_error "Chart directory not found: $CHART_DIR"
    exit 1
fi

cd "$CHART_DIR"

# Load images into Minikube
print_info "Loading Docker images into Minikube..."
minikube image load hackathon-backend:latest
minikube image load hackathon-frontend:latest

# Verify images
print_info "Verifying loaded images..."
minikube image list | grep hackathon || true

# Check if Helm release exists
if helm list 2>/dev/null | grep -q "hackathon-app"; then
    print_warning "Existing deployment found. Upgrading..."
    helm upgrade hackathon-app . --wait --timeout=5m
else
    print_info "Installing Helm chart..."
    helm install hackathon-app . --wait --timeout=5m
fi

# Wait for deployment
print_info "Waiting for deployments to be ready..."
print_info "This may take a few minutes for the first time..."

# Check deployment status
echo ""
print_cyan "=== Checking Deployment Status ==="
kubectl get deployments -l app.kubernetes.io/instance=hackathon-app

echo ""
print_cyan "=== Checking Pods ==="
kubectl get pods -l app.kubernetes.io/instance=hackathon-app

# Wait with longer timeout
kubectl wait --for=condition=available deployment/hackathon-app-backend --timeout=300s
kubectl wait --for=condition=available deployment/hackathon-app-frontend --timeout=300s

# Show status
echo ""
print_info "Deployment complete! Showing status..."
echo ""
print_cyan "=== Pods ==="
kubectl get pods -l app.kubernetes.io/instance=hackathon-app

echo ""
print_cyan "=== Services ==="
kubectl get services -l app.kubernetes.io/instance=hackathon-app

echo ""
print_cyan "=== Ingress ==="
kubectl get ingress -l app.kubernetes.io/instance=hackathon-app

echo ""
print_info "Getting Minikube IP..."
MINIKUBE_IP=$(minikube ip)
print_info "Minikube IP: $MINIKUBE_IP"

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Access the application:"
echo ""
echo "  OPTION 1: Add to hosts file:"
echo "     $MINIKUBE_IP hackathon.local"
echo "     Then open: http://hackathon.local"
echo ""
echo "  OPTION 2: Use port-forward (Recommended for testing):"
echo "     kubectl port-forward service/hackathon-app-frontend 3000:3000"
echo "     Then open: http://localhost:3000"
echo ""
echo "  OPTION 3: Use minikube service command:"
echo "     minikube service hackathon-app-frontend --url"
echo "     minikube service hackathon-app-backend --url"
echo ""
echo "  OPTION 4: Use minikube tunnel (for LoadBalancer):"
echo "     minikube tunnel"
echo ""
echo "Troubleshooting:"
echo "  - View logs: kubectl logs -l app.kubernetes.io/instance=hackathon-app"
echo "  - Check events: kubectl get events --sort-by='.lastTimestamp'"
echo "  - Restart pods: kubectl rollout restart deployment/hackathon-app-backend"
echo ""
echo "========================================="
