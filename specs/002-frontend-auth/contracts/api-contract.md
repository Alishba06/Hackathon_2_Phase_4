# API Contract: Frontend Application & Authentication Integration

## Overview
This document defines the API contracts for the frontend application's interaction with the backend API for the Todo web application. These contracts specify the endpoints, request/response formats, and authentication requirements.

## Authentication Endpoints

### POST /api/auth/register
Register a new user account

**Headers:**
- Content-Type: application/json

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Responses:**
- 201 Created: User registered successfully
```json
{
  "jwtToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "isActive": true,
    "createdAt": "2026-01-24T10:00:00Z",
    "updatedAt": "2026-01-24T10:00:00Z"
  },
  "expiresIn": 3600
}
```

- 400 Bad Request: Invalid input data
- 409 Conflict: Email already exists

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
  "jwtToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "isActive": true,
    "createdAt": "2026-01-24T10:00:00Z",
    "updatedAt": "2026-01-24T10:00:00Z"
  },
  "expiresIn": 3600
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid credentials

### POST /api/auth/logout
Logout the current user

**Headers:**
- Authorization: Bearer {jwtToken}

**Responses:**
- 200 OK: Logout successful
```json
{
  "message": "Successfully logged out"
}
```

- 401 Unauthorized: Invalid or expired token

## Task Management Endpoints

For all task endpoints, the user ID is passed as a path parameter `{user_id}` which corresponds to the authenticated user's ID.

### GET /api/{user_id}/tasks
Retrieve all tasks for the authenticated user

**Headers:**
- Authorization: Bearer {jwtToken}

**Responses:**
- 200 OK: Tasks retrieved successfully
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Sample Task",
      "description": "Task description",
      "isCompleted": false,
      "dueDate": "2026-02-01T10:00:00Z",
      "priority": "medium",
      "userId": "user-uuid-string",
      "createdAt": "2026-01-24T10:00:00Z",
      "updatedAt": "2026-01-24T10:00:00Z"
    }
  ]
}
```

- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to access another user's tasks

### POST /api/{user_id}/tasks
Create a new task for the authenticated user

**Headers:**
- Authorization: Bearer {jwtToken}
- Content-Type: application/json

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "dueDate": "2026-02-01T10:00:00Z",
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
  "isCompleted": false,
  "dueDate": "2026-02-01T10:00:00Z",
  "priority": "high",
  "userId": "user-uuid-string",
  "createdAt": "2026-01-24T10:00:00Z",
  "updatedAt": "2026-01-24T10:00:00Z"
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to create task for another user

### GET /api/{user_id}/tasks/{task_id}
Retrieve a specific task for the authenticated user

**Headers:**
- Authorization: Bearer {jwtToken}

**Responses:**
- 200 OK: Task retrieved successfully
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Task description",
  "isCompleted": false,
  "dueDate": "2026-02-01T10:00:00Z",
  "priority": "medium",
  "userId": "user-uuid-string",
  "createdAt": "2026-01-24T10:00:00Z",
  "updatedAt": "2026-01-24T10:00:00Z"
}
```

- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to access another user's task
- 404 Not Found: Task does not exist

### PUT /api/{user_id}/tasks/{task_id}
Update a specific task for the authenticated user

**Headers:**
- Authorization: Bearer {jwtToken}
- Content-Type: application/json

**Request Body:**
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "isCompleted": true,
  "dueDate": "2026-02-01T10:00:00Z",
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
  "isCompleted": true,
  "dueDate": "2026-02-01T10:00:00Z",
  "priority": "low",
  "userId": "user-uuid-string",
  "createdAt": "2026-01-24T10:00:00Z",
  "updatedAt": "2026-01-24T11:00:00Z"
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to update another user's task
- 404 Not Found: Task does not exist

### PATCH /api/{user_id}/tasks/{task_id}
Partially update a specific task for the authenticated user (e.g., toggle completion status)

**Headers:**
- Authorization: Bearer {jwtToken}
- Content-Type: application/json

**Request Body:**
```json
{
  "isCompleted": true
}
```

**Responses:**
- 200 OK: Task updated successfully
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Task description",
  "isCompleted": true,
  "dueDate": "2026-02-01T10:00:00Z",
  "priority": "medium",
  "userId": "user-uuid-string",
  "createdAt": "2026-01-24T10:00:00Z",
  "updatedAt": "2026-01-24T11:00:00Z"
}
```

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to update another user's task
- 404 Not Found: Task does not exist

### DELETE /api/{user_id}/tasks/{task_id}
Delete a specific task for the authenticated user

**Headers:**
- Authorization: Bearer {jwtToken}

**Responses:**
- 200 OK: Task deleted successfully
```json
{
  "message": "Task deleted successfully"
}
```

- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Attempting to delete another user's task
- 404 Not Found: Task does not exist

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