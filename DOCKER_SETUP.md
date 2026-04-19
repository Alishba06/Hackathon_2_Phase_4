# Docker Setup Guide

## Overview
This project uses Docker Compose to containerize both the frontend (Next.js) and backend (FastAPI) applications.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Frontend      │────▶│    Backend      │────▶│ Neon Serverless  │
│   Next.js:3000  │     │   FastAPI:8000  │     │ PostgreSQL:5433  │
└─────────────────┘     └─────────────────┘     └──────────────────┘
```

## Services

### 1. Frontend (Next.js)
- **Port**: 3000
- **Dockerfile**: `frontend/Dockerfile`
- **Build Stage**: Multi-stage build (deps → builder → runner)
- **Base Image**: Node 20 Alpine
- **Optimizations**: 
  - Standalone output for smaller image size
  - Multi-stage build to exclude dev dependencies
  - Non-root user for security

### 2. Backend (FastAPI)
- **Port**: 8000
- **Dockerfile**: `backend/Dockerfile`
- **Base Image**: Python 3.11 Slim
- **Features**:
  - GCC installed for native dependencies
  - Uvicorn ASGI server
  - Auto table creation on startup

### 3. Neon DB Proxy
- **Port**: 5433
- **Image**: `ghcr.io/neondatabase/serverless-proxy:latest`
- **Purpose**: Proxy connection to Neon Serverless PostgreSQL

## Building Images

### Build All Services
```bash
docker-compose build
```

### Build Specific Service
```bash
# Build only frontend
docker-compose build frontend

# Build only backend
docker-compose build backend
```

### Build with No Cache
```bash
docker-compose build --no-cache
```

## Running the Application

### Start All Services
```bash
docker-compose up
```

### Start in Detached Mode
```bash
docker-compose up -d
```

### Start with Build
```bash
docker-compose up --build
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5433/dbname

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Frontend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Testing the Containers

### Check Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Stopping the Application

### Stop All Services
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

## Dockerfile Details

### Frontend Dockerfile
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN npm ci

# Stage 2: Builder
FROM node:20-alpine AS builder
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
CMD ["node", "server.js"]
```

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Frontend Build Fails
1. Check Node version compatibility
2. Clear npm cache: `npm cache clean --force`
3. Remove node_modules and rebuild

### Backend Build Fails
1. Check Python dependencies in requirements.txt
2. Ensure GCC is installed for native modules
3. Check database connection string

### Container Won't Start
1. Check logs: `docker-compose logs <service>`
2. Verify environment variables
3. Check port conflicts: `netstat -ano | findstr :3000`

## Production Considerations

1. **Security**:
   - Use non-root users (already implemented)
   - Don't expose unnecessary ports
   - Use secrets management for sensitive data

2. **Performance**:
   - Use multi-stage builds (already implemented)
   - Minimize layer count
   - Use .dockerignore files (already created)

3. **Monitoring**:
   - Health checks configured
   - Logs should be collected
   - Consider adding Prometheus metrics

## Next Steps

After building:
1. Run `docker-compose up -d` to start services
2. Access frontend at http://localhost:3000
3. Test API at http://localhost:8000/docs
4. Monitor logs with `docker-compose logs -f`
