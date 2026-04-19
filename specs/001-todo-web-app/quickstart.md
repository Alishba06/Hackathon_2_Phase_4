# Quickstart Guide: Todo Full-Stack Web Application

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Docker and Docker Compose (optional, for containerized setup)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup (FastAPI)

#### Install Python Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
```

#### Run Migrations
```bash
# Using Alembic for database migrations
alembic upgrade head
```

#### Start the Backend Server
```bash
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup (Next.js)

#### Install Node Dependencies
```bash
cd frontend
npm install
```

#### Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/api/auth
```

#### Start the Frontend Development Server
```bash
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration
- `POST /api/auth/logout` - User logout

### Task Management
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Development Workflow

### Backend Development
1. Make changes to the backend code
2. The server will automatically reload due to `--reload` flag
3. Run tests: `pytest`

### Frontend Development
1. Make changes to the frontend code
2. The development server will hot-reload changes
3. Run tests: `npm run test`

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Environment Configuration

### Development
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- JWT tokens are validated using the `BETTER_AUTH_SECRET`

### Production
- Update API endpoints in frontend to production URLs
- Use production-grade JWT secret
- Configure SSL certificates for secure connections

## Troubleshooting

### Common Issues
1. **JWT Validation Errors**: Ensure `BETTER_AUTH_SECRET` is identical in both frontend and backend environments
2. **Database Connection Issues**: Verify PostgreSQL is running and credentials are correct
3. **CORS Errors**: Check that frontend origin is allowed in backend CORS configuration

### Resetting the Database
```bash
# Reset database to initial state
alembic downgrade base
alembic upgrade head
```