# Data Model: Frontend Application & Authentication Integration

## Overview
This document describes the data models used in the frontend application for the Todo web application with Better Auth integration. These models represent the client-side representation of the data structures used in the application.

## User Entity

### Properties
- **id**: string - Unique identifier for the user
- **email**: string - Email address used for authentication
- **firstName**: string (optional) - User's first name
- **lastName**: string (optional) - User's last name
- **isActive**: boolean - Account status indicator
- **createdAt**: Date - Account creation timestamp
- **updatedAt**: Date - Last account update timestamp

### Relationships
- Has many: tasks - Associated tasks owned by the user

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- firstName and lastName must be less than 255 characters if provided

## Task Entity

### Properties
- **id**: string - Unique identifier for the task
- **title**: string - Task title (required, 1-255 characters)
- **description**: string (optional) - Detailed task description (max 10000 characters)
- **isCompleted**: boolean - Completion status (default: false)
- **dueDate**: Date (optional) - Deadline for the task
- **priority**: string - Priority level ('low', 'medium', 'high') (default: 'medium')
- **userId**: string - Reference to the owning user
- **createdAt**: Date - Task creation timestamp
- **updatedAt**: Date - Last task update timestamp

### Relationships
- Belongs to: user - The user who owns this task

### Validation Rules
- Title is required and must be between 1-255 characters
- Description, if provided, must be less than 10000 characters
- Priority must be one of 'low', 'medium', or 'high'
- userId must reference an existing user

## Authentication Session

### Properties
- **jwtToken**: string - JWT token received after successful authentication
- **expiresAt**: Date - Expiration time of the JWT token
- **user**: User - The authenticated user object
- **refreshToken**: string (optional) - Token for refreshing the session

### Validation Rules
- jwtToken must be a valid JWT format
- expiresAt must be in the future
- user must be a valid User object

## API Request/Response Models

### User Registration Request
- **email**: string - User's email address
- **password**: string - User's password (minimum 8 characters)
- **firstName**: string (optional) - User's first name
- **lastName**: string (optional) - User's last name

### User Login Request
- **email**: string - User's email address
- **password**: string - User's password

### User Login Response
- **jwtToken**: string - JWT token for authentication
- **user**: User - The authenticated user object
- **expiresIn**: number - Token expiration time in seconds

### Task Creation Request
- **title**: string - Task title
- **description**: string (optional) - Task description
- **dueDate**: string (optional) - Due date in ISO format
- **priority**: string (optional) - Priority level ('low', 'medium', 'high')

### Task Response
- **id**: string - Task identifier
- **title**: string - Task title
- **description**: string (optional) - Task description
- **isCompleted**: boolean - Completion status
- **dueDate**: string (optional) - Due date in ISO format
- **priority**: string - Priority level
- **userId**: string - Owner user identifier
- **createdAt**: string - Creation timestamp in ISO format
- **updatedAt**: string - Update timestamp in ISO format

### Task Update Request
- **title**: string (optional) - Updated task title
- **description**: string (optional) - Updated task description
- **isCompleted**: boolean (optional) - Updated completion status
- **dueDate**: string (optional) - Updated due date in ISO format
- **priority**: string (optional) - Updated priority level