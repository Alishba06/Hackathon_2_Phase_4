# Security Implementation Guide

## Overview
This document provides details about the security implementation in the Todo web application. It covers authentication, authorization, and data isolation mechanisms.

## Authentication

### JWT-Based Authentication
The application uses JWT (JSON Web Tokens) for authentication. The system implements the following:

- **Token Generation**: When a user successfully logs in, a JWT token is generated containing:
  - User ID (`sub` claim)
  - Expiration time (`exp` claim)
  - Issuance time (`iat` claim)

- **Token Verification**: All protected endpoints validate the JWT token using:
  - Shared secret stored in `BETTER_AUTH_SECRET` environment variable
  - Signature verification using HS256 algorithm
  - Expiration check to ensure tokens are not expired

### Token Storage
- **Frontend**: JWT tokens are stored in browser's `localStorage` for persistence across sessions
- **Backend**: No token storage (stateless authentication)

## Authorization

### Route Protection
The application implements route protection at multiple levels:

#### Backend Middleware
- `AuthMiddleware` in `backend/src/middleware/auth_middleware.py` validates JWT tokens for all protected endpoints
- Automatically rejects requests without valid tokens with 401 Unauthorized
- Adds authenticated user information to request context

#### Frontend Protection
- `middleware.ts` implements Next.js middleware to protect routes
- `AuthProvider` component manages authentication state
- Automatic redirection to login for unauthenticated users

### User Isolation
The system ensures that users can only access their own data:

#### Backend Enforcement
- All task queries are filtered by the authenticated user's ID
- Path parameters are validated against the user ID in the JWT token
- Attempts to access other users' data result in 403 Forbidden responses

#### Frontend Enforcement
- Security validation utilities check user permissions before API calls
- UI only displays tasks belonging to the authenticated user

## Security Headers

### API Security Headers
The API includes the following security headers:

- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-XSS-Protection: 1; mode=block` - Enables XSS protection in older browsers
- `X-Requested-With: XMLHttpRequest` - Helps identify AJAX requests

### Input Validation
- All API inputs are validated using Pydantic models
- SQL injection prevention through parameterized queries
- XSS prevention through input sanitization

## Error Handling

### Security-Related Errors
The system handles security-related errors appropriately:

- **401 Unauthorized**: Returned when no valid authentication token is provided
- **403 Forbidden**: Returned when a user attempts to access resources they don't own
- **422 Unprocessable Entity**: Returned for validation errors in request data

### Logging
Security events are logged for monitoring and analysis:

- Failed authentication attempts
- Unauthorized access attempts
- User isolation violations
- Token validation failures

## Database Security

### User Data Isolation
- Each task is associated with a specific user via `user_id` foreign key
- All queries filter results by the authenticated user's ID
- No direct access to other users' data is possible

### Password Security
- Passwords are hashed using bcrypt algorithm
- Salt is automatically generated during hashing
- Plain text passwords are never stored

## API Endpoints Security

### Protected Endpoints
All `/api/{user_id}/**` endpoints require authentication:

- `/api/{user_id}/tasks` - Get/create user's tasks
- `/api/{user_id}/tasks/{task_id}` - Get/update/delete specific task
- All endpoints validate that `user_id` matches the authenticated user

### Request Validation
- All requests are validated against API contracts
- Malformed requests return 400 Bad Request
- Invalid data returns 422 Unprocessable Entity

## Security Best Practices

### Token Management
- JWT tokens have a limited lifetime (configurable via `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`)
- Tokens are invalidated on logout
- Automatic token refresh mechanisms are implemented

### Rate Limiting
- API endpoints are protected against excessive requests
- Configurable rate limits per IP address

### Audit Trail
- Security-relevant events are logged with timestamps
- IP addresses and user agents are recorded for security events
- Logs are stored securely and monitored for suspicious activity

## Testing Security Features

### Automated Tests
The security implementation is validated through automated tests:

- `backend/tests/test_security_compliance.py` - Security compliance tests
- `backend/tests/test_api_contracts.py` - API contract validation
- `backend/tests/test_security_rules.py` - Security rule validation
- `backend/tests/test_user_isolation_validation.py` - User isolation tests
- `backend/tests/test_invalid_request_logging.py` - Invalid request logging tests
- `frontend/src/__tests__/security.validation.test.ts` - Frontend security validation

### Validation Script
Run the complete security validation suite with:
```bash
python scripts/run_security_validation.py
```

## Environment Configuration

### Security Environment Variables
The following environment variables control security settings:

- `BETTER_AUTH_SECRET`: Secret key for JWT signing and verification
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time in days

## Security Monitoring

### Log Analysis
Security logs can be analyzed using the tools in `backend/src/tools/security_log_analyzer.py`:

- `analyze_security_logs_by_timeframe()` - Analyze logs within a specific timeframe
- `detect_brute_force_attempts()` - Detect potential brute force attacks
- `detect_ip_based_threats()` - Assess threats from specific IP addresses
- `get_security_summary()` - Get a summary of security events

## Compliance

This implementation complies with the security requirements specified in the feature specification:
- All API endpoints reject unauthenticated requests with 401 Unauthorized
- JWT tokens are verified using the shared secret
- Backend filters all task queries by authenticated user ID
- Frontend cannot display or modify tasks of other users
- Invalid requests are logged and rejected appropriately
- The system passes all automated spec-driven validation tests