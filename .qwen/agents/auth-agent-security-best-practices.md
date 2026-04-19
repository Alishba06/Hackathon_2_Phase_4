# Auth Agent – Security Best Practices

## Password Security
- Use bcrypt, argon2, or scrypt for password hashing with appropriate cost factors
- Never store passwords in plain text or use weak hashing algorithms like MD5 or SHA-1
- Implement proper salt generation for each password hash
- Enforce strong password policies (minimum length, complexity requirements)

## JWT Security
- Use strong secret keys for signing JWTs (at least 256 bits)
- Implement proper token expiration times (short-lived access tokens, longer refresh tokens)
- Store JWTs securely on the client-side (preferably in httpOnly cookies)
- Implement token blacklisting for logout functionality
- Use HTTPS exclusively for all JWT transmission

## Session Management
- Generate cryptographically secure session IDs
- Implement proper session timeout mechanisms
- Regenerate session IDs after login to prevent session fixation
- Store session data server-side with secure cleanup mechanisms
- Implement concurrent session limits

## Input Validation and Sanitization
- Validate and sanitize all user inputs to prevent injection attacks
- Implement proper output encoding to prevent XSS
- Use parameterized queries to prevent SQL injection
- Implement proper content security policies

## Rate Limiting and Brute Force Protection
- Implement account lockout mechanisms after failed attempts
- Use CAPTCHA or similar mechanisms for suspicious activity
- Apply rate limiting to authentication endpoints
- Monitor for unusual authentication patterns

## Transport Security
- Enforce HTTPS for all authentication-related communications
- Use HSTS headers to prevent protocol downgrade attacks
- Implement secure cookie attributes (Secure, HttpOnly, SameSite)
- Use TLS 1.2 or higher for encrypted connections

## Error Handling
- Avoid revealing sensitive information in error messages
- Log authentication failures for monitoring without exposing details to users
- Implement generic error messages that don't indicate the existence of accounts
- Use consistent timing for authentication responses to prevent timing attacks

## Storage Security
- Encrypt sensitive authentication data at rest
- Use secure key management practices
- Implement proper access controls for authentication databases
- Regularly rotate encryption keys and secrets

## Monitoring and Logging
- Log authentication events for security analysis
- Monitor for suspicious authentication patterns
- Implement alerts for multiple failed login attempts
- Track and audit token usage and session activities

## OWASP Compliance
- Follow OWASP Top 10 security guidelines
- Implement CSRF protection for state-changing operations
- Validate and sanitize redirects and forwards
- Implement proper authentication for all protected resources
- Follow secure coding practices to prevent vulnerabilities