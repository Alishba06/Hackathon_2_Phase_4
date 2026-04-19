# Quickstart Guide: Security & Spec-Driven Validation

## Overview
This guide provides instructions for implementing and testing the security and validation features for the Todo web application. This includes JWT-based authentication, user isolation, and spec-driven validation.

## Prerequisites
- Python 3.11+ (for backend)
- Node.js 18.x+ (for frontend)
- Access to the backend API (FastAPI server running)
- Valid JWT secret for Better Auth (shared with backend via `BETTER_AUTH_SECRET`)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to Backend Directory
```bash
cd backend
```

### 3. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 4. Navigate to Frontend Directory
```bash
cd ../frontend
```

### 5. Install Frontend Dependencies
```bash
npm install
# or
yarn install
```

### 6. Environment Configuration
Create a `.env` file in both backend and frontend directories with the required variables:

**Backend (.env):**
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/api/auth
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-key-here
```

### 7. Run the Backend Server
```bash
cd backend
uvicorn src.main:app --reload
```

### 8. Run the Frontend Development Server
```bash
cd frontend
npm run dev
# or
yarn dev
```

The frontend application will be available at `http://localhost:3000`.

## Security Implementation

### Backend JWT Enforcement
1. The backend implements middleware to extract JWT from Authorization header
2. Token signature is verified using the shared secret (`BETTER_AUTH_SECRET`)
3. Token is decoded to extract user ID
4. All database queries are filtered by authenticated user ID
5. Returns 401 Unauthorized for missing or invalid tokens

### Frontend Enforcement
1. Protected routes are implemented in Next.js App Router
2. Access to pages is blocked without valid session
3. Frontend displays only authenticated user's tasks
4. Handles token expiration (redirects to login if expired)

## Testing Security Features

### 1. Test Unauthorized Access
```bash
# Test API call without token
curl -X GET http://localhost:8000/api/123/tasks
# Should return 401 Unauthorized

# Test API call with invalid token
curl -X GET http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer invalid.token.here"
# Should return 401 Unauthorized
```

### 2. Test User Isolation
1. Register and log in as User A
2. Create a few tasks for User A
3. Register and log in as User B
4. Attempt to access User A's tasks via API or frontend
5. Verify that User B cannot access User A's tasks

### 3. Test Frontend Route Protection
1. Log out of the application
2. Try to navigate directly to `/dashboard` or `/tasks`
3. Verify that you're redirected to the login page

## Running Spec-Driven Validation

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm run test
# or
yarn test
```

### Automated Spec-Driven Checks
```bash
# Run Qwen Code + Spec-Kit Plus automated checks
# This validates:
# - API endpoints correctness (methods, routes, payloads)
# - Security enforcement (JWT verification, user isolation)
# - Data integrity (tasks correctly filtered per user)

# Example command (specific to your setup):
python -m pytest tests/security_tests.py -v
```

## Security Validation Results

### Expected Outcomes
- All API endpoints reject unauthenticated requests with 401 Unauthorized
- JWT tokens are verified using the shared secret
- Backend filters all task queries by authenticated user ID
- Frontend cannot display or modify tasks of other users
- All invalid requests are logged and rejected appropriately
- Automated spec-driven validation suite passes all tests

### Verification Steps
1. Confirm all endpoints return proper HTTP status codes
2. Verify that user isolation is maintained across all operations
3. Check that security rules are enforced during runtime
4. Review security logs for any violations

## Troubleshooting

### Common Issues
1. **JWT Token Not Verified**: Ensure `BETTER_AUTH_SECRET` matches between frontend and backend
2. **User Accessing Other User's Tasks**: Check that backend is filtering queries by authenticated user ID
3. **Frontend Route Protection Not Working**: Verify that AuthProvider is wrapping the application
4. **Spec-Driven Tests Failing**: Review test output for specific validation failures

### Debugging Tips
1. Check backend logs for authentication and authorization failures
2. Verify that environment variables are correctly set
3. Ensure the JWT token is properly attached to requests
4. Confirm that user IDs in tokens match the expected values