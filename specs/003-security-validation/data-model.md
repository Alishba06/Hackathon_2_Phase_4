# Data Model: Security & Spec-Driven Validation

## Overview
This document describes the data models used for implementing security and validation features in the Todo web application. These models ensure proper authentication, authorization, and user isolation.

## User Entity

### Properties
- **id**: string - Unique identifier for the user (UUID)
- **email**: string - Email address used for authentication (unique)
- **first_name**: string (optional) - User's first name
- **last_name**: string (optional) - User's last name
- **password_hash**: string - Hashed password for authentication
- **is_active**: boolean - Account status indicator (default: true)
- **created_at**: DateTime - Account creation timestamp
- **updated_at**: DateTime - Last account update timestamp

### Relationships
- Has many: tasks - Associated tasks owned by the user

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Password must be hashed before storing
- first_name and last_name must be less than 255 characters if provided

## Task Entity

### Properties
- **id**: string - Unique identifier for the task (UUID)
- **title**: string - Task title (required, 1-255 characters)
- **description**: string (optional) - Detailed task description (max 10000 characters)
- **is_completed**: boolean - Completion status (default: false)
- **due_date**: DateTime (optional) - Deadline for the task
- **priority**: string - Priority level ('low', 'medium', 'high') (default: 'medium')
- **user_id**: string - Reference to the owning user (foreign key)
- **created_at**: DateTime - Task creation timestamp
- **updated_at**: DateTime - Last task update timestamp

### Relationships
- Belongs to: user - The user who owns this task

### Validation Rules
- Title is required and must be between 1-255 characters
- Description, if provided, must be less than 10000 characters
- Priority must be one of 'low', 'medium', or 'high'
- user_id must reference an existing user
- Only the owner can modify/delete the task

## JWT Token Entity (Conceptual)

### Properties
- **token**: string - The JWT token string
- **user_id**: string - Reference to the authenticated user
- **expires_at**: DateTime - Token expiration timestamp
- **issued_at**: DateTime - Token issuance timestamp
- **issuer**: string - The service that issued the token

### Validation Rules
- Token must be properly signed with the shared secret
- Token must not be expired at the time of validation
- Token must contain a valid user_id that exists in the system
- Token must be properly formatted according to JWT standards

## Security Log Entity

### Properties
- **id**: string - Unique identifier for the log entry (UUID)
- **user_id**: string (optional) - Reference to the user associated with the event
- **endpoint**: string - The API endpoint that was accessed
- **method**: string - HTTP method used (GET, POST, PUT, DELETE, etc.)
- **ip_address**: string - IP address of the requesting client
- **user_agent**: string (optional) - User agent string of the requesting client
- **status_code**: integer - HTTP status code returned
- **timestamp**: DateTime - When the event occurred
- **event_type**: string - Type of security event ('access_attempt', 'auth_failure', 'auth_success', 'unauthorized_access', etc.)
- **details**: string (optional) - Additional details about the event

### Validation Rules
- All fields must be recorded for proper audit trail
- IP address must be a valid IPv4 or IPv6 address
- Status code must be a valid HTTP status code
- Event type must be one of the predefined values
- Timestamp must be current at the time of logging

## API Request/Response Models

### Authenticated Request Headers
- **Authorization**: string - Bearer token format: "Bearer {jwt_token}"

### Successful Authentication Response
- **jwt_token**: string - JWT token for subsequent requests
- **user**: User object - The authenticated user's information
- **expires_in**: number - Token validity duration in seconds

### Error Response Format
- **error**: object - Error details
  - **message**: string - Human-readable error message
  - **code**: string - Machine-readable error code
  - **timestamp**: string - ISO 8601 formatted timestamp
  - **path**: string - The requested path that caused the error

### Security Violation Response
- **error**: object - Security violation details
  - **message**: string - Security violation message
  - **code**: string - Security error code (e.g., "SECURITY_VIOLATION", "UNAUTHORIZED_ACCESS")
  - **timestamp**: string - ISO 8601 formatted timestamp
  - **request_id**: string - Unique identifier for the request