# API Contract: Security & Spec-Driven Validation

## Overview
This document defines the API contracts for security and validation features in the Todo web application. These contracts specify the endpoints, request/response formats, authentication requirements, and security validation rules.

## Authentication Endpoints

### POST /api/auth/login
Authenticate a user and return JWT token

**Headers:**
- Content-Type: application/json

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Responses:**
- 200 OK: Authentication successful
```json
{
  "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-01-24T10:00:00Z",
    "updated_at": "2026-01-24T10:00:00Z"
  },
  "expires_in": 3600
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid credentials

### POST /api/auth/register
Register a new user account

**Headers:**
- Content-Type: application/json

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Responses:**
- 201 Created: User registered successfully
```json
{
  "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-01-24T10:00:00Z",
    "updated_at": "2026-01-24T10:00:00Z"
  },
  "expires_in": 3600
}
```

- 400 Bad Request: Invalid input data
- 409 Conflict: Email already exists

### POST /api/auth/logout
Logout the current user

**Headers:**
- Authorization: Bearer {jwt_token}

**Responses:**
- 200 OK: Logout successful
```json
{
  "message": "Successfully logged out"
}
```

- 401 Unauthorized: Invalid or expired token

## Task Management Endpoints (Security-Enhanced)

For all task endpoints, the user ID is passed as a path parameter `{user_id}` which corresponds to the authenticated user's ID. The backend will verify that the authenticated user matches the user_id in the path.

### GET /api/{user_id}/tasks
Retrieve all tasks for the authenticated user

**Headers:**
- Authorization: Bearer {jwt_token}

**Responses:**
- 200 OK: Tasks retrieved successfully
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Sample Task",
      "description": "Task description",
      "is_completed": false,
      "due_date": "2026-02-01T10:00:00Z",
      "priority": "medium",
      "user_id": "user-uuid-string",
      "created_at": "2026-01-24T10:00:00Z",
      "updated_at": "2026-01-24T10:00:00Z"
    }
  ]
}
```

- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to access another user's tasks (user_id mismatch)
- 404 Not Found: User does not exist

### POST /api/{user_id}/tasks
Create a new task for the authenticated user

**Headers:**
- Authorization: Bearer {jwt_token}
- Content-Type: application/json

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "due_date": "2026-02-01T10:00:00Z",
  "priority": "high"
}
```

**Responses:**
- 201 Created: Task created successfully
```json
{
  "id": "uuid-string",
  "title": "New Task",
  "description": "Task description",
  "is_completed": false,
  "due_date": "2026-02-01T10:00:00Z",
  "priority": "high",
  "user_id": "user-uuid-string",
  "created_at": "2026-01-24T10:00:00Z",
  "updated_at": "2026-01-24T10:00:00Z"
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to create task for another user (user_id mismatch)

### GET /api/{user_id}/tasks/{task_id}
Retrieve a specific task for the authenticated user

**Headers:**
- Authorization: Bearer {jwt_token}

**Responses:**
- 200 OK: Task retrieved successfully
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Task description",
  "is_completed": false,
  "due_date": "2026-02-01T10:00:00Z",
  "priority": "medium",
  "user_id": "user-uuid-string",
  "created_at": "2026-01-24T10:00:00Z",
  "updated_at": "2026-01-24T10:00:00Z"
}
```

- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to access another user's task (user_id mismatch or task doesn't belong to user)
- 404 Not Found: Task does not exist

### PUT /api/{user_id}/tasks/{task_id}
Update a specific task for the authenticated user

**Headers:**
- Authorization: Bearer {jwt_token}
- Content-Type: application/json

**Request Body:**
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "is_completed": true,
  "due_date": "2026-02-01T10:00:00Z",
  "priority": "low"
}
```

**Responses:**
- 200 OK: Task updated successfully
```json
{
  "id": "uuid-string",
  "title": "Updated Task Title",
  "description": "Updated description",
  "is_completed": true,
  "due_date": "2026-02-01T10:00:00Z",
  "priority": "low",
  "user_id": "user-uuid-string",
  "created_at": "2026-01-24T10:00:00Z",
  "updated_at": "2026-01-24T11:00:00Z"
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to update another user's task (user_id mismatch or task doesn't belong to user)
- 404 Not Found: Task does not exist

### PATCH /api/{user_id}/tasks/{task_id}
Partially update a specific task for the authenticated user (e.g., toggle completion status)

**Headers:**
- Authorization: Bearer {jwt_token}
- Content-Type: application/json

**Request Body:**
```json
{
  "is_completed": true
}
```

**Responses:**
- 200 OK: Task updated successfully
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Task description",
  "is_completed": true,
  "due_date": "2026-02-01T10:00:00Z",
  "priority": "medium",
  "user_id": "user-uuid-string",
  "created_at": "2026-01-24T10:00:00Z",
  "updated_at": "2026-01-24T11:00:00Z"
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to update another user's task (user_id mismatch or task doesn't belong to user)
- 404 Not Found: Task does not exist

### DELETE /api/{user_id}/tasks/{task_id}
Delete a specific task for the authenticated user

**Headers:**
- Authorization: Bearer {jwt_token}

**Responses:**
- 200 OK: Task deleted successfully
```json
{
  "message": "Task deleted successfully"
}
```

- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to delete another user's task (user_id mismatch or task doesn't belong to user)
- 404 Not Found: Task does not exist

## Security Validation Endpoints

### GET /api/auth/me
Get current authenticated user's profile

**Headers:**
- Authorization: Bearer {jwt_token}

**Responses:**
- 200 OK: User profile retrieved successfully
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-01-24T10:00:00Z",
    "updated_at": "2026-01-24T10:00:00Z"
  }
}
```

- 401 Unauthorized: Invalid or expired token

## Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "message": "Descriptive error message",
    "code": "ERROR_CODE",
    "timestamp": "2026-01-24T10:00:00Z",
    "path": "/api/users/123/tasks"
  }
}
```

## Security Validation Requirements

### JWT Token Validation
- All authenticated endpoints require the Authorization header with the JWT token
- JWT tokens must be verified using the shared secret (`BETTER_AUTH_SECRET`)
- Tokens must not be expired at the time of request
- User ID in the token must match the user ID in the request path

### User Isolation
- Backend must filter all task queries by the authenticated user ID
- Users cannot access or modify other users' tasks
- All database queries must be validated against the authenticated user context

### Request Validation
- All requests must be validated against the API contract
- Invalid requests must be logged and rejected with appropriate HTTP status codes
- Malformed requests should return 400 Bad Request
- Unauthorized requests should return 401 Unauthorized
- Forbidden access attempts should return 403 Forbidden

## Common Headers

### Authorization
All authenticated endpoints require the Authorization header with the JWT token:
```
Authorization: Bearer {jwt_token}
```

### Content-Type
Requests with a body must include:
```
Content-Type: application/json
```

## Security Logging
All security-relevant events must be logged, including:
- Failed authentication attempts
- Unauthorized access attempts
- Token validation failures
- User isolation violations