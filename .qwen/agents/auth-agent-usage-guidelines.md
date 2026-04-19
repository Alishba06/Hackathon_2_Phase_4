# When to Use the Auth Agent

## Primary Use Cases

### 1. Authentication System Implementation
- When building new user authentication systems from scratch
- When integrating third-party authentication providers
- When implementing custom authentication flows
- When setting up social login features (Google, Facebook, GitHub, etc.)

### 2. Security Enhancement
- When reviewing existing authentication code for security vulnerabilities
- When upgrading legacy authentication systems to more secure implementations
- When implementing compliance requirements for authentication systems
- When conducting security audits of authentication-related code

### 3. Token Management
- When implementing JWT-based authentication
- When setting up refresh token mechanisms
- When configuring token validation and verification processes
- When implementing token-based authorization systems

### 4. Password Management
- When implementing secure password hashing and verification
- When adding password strength requirements
- When implementing password reset functionality
- When migrating password storage schemas

### 5. Session Management
- When implementing secure session handling
- When setting up session persistence mechanisms
- When configuring session timeout and cleanup processes
- When implementing concurrent session controls

### 6. Authorization Systems
- When implementing role-based access control (RBAC)
- When setting up permission-based authorization
- When creating authentication middleware
- When implementing API endpoint protection

### 7. Third-Party Integration
- When integrating Better Auth or similar authentication libraries
- When connecting to identity providers (Auth0, Firebase Auth, etc.)
- When implementing OAuth 2.0 or OpenID Connect flows
- When configuring single sign-on (SSO) solutions

### 8. Security Incident Response
- When investigating authentication-related security incidents
- When patching authentication vulnerabilities
- When implementing additional security measures after security events
- When reviewing authentication logs for suspicious activity

## Situations Requiring Consultation

### 1. Architecture Decisions
- When choosing between different authentication approaches
- When deciding on token storage strategies
- When selecting authentication libraries or frameworks
- When designing authentication system scalability

### 2. Compliance Requirements
- When implementing authentication for regulated industries
- When ensuring GDPR, CCPA, or HIPAA compliance for authentication data
- When meeting PCI DSS requirements for authentication systems
- When implementing government or enterprise security standards

### 3. Performance Optimization
- When optimizing authentication system performance
- When scaling authentication systems for high traffic
- When implementing caching strategies for authentication data
- When reducing authentication system latency

## Scenarios to Avoid Using This Agent

### 1. Non-Security Related Tasks
- When working on UI/UX elements unrelated to authentication
- When implementing business logic that doesn't involve authentication
- When performing general application maintenance tasks
- When working on non-sensitive data processing

### 2. Low-Risk Applications
- When working on internal tools with minimal security requirements
- When prototyping features that won't be deployed to production
- When working on applications with no user data or sensitive information
- When implementing authentication for demonstration purposes only

## Trigger Conditions

### Automatic Engagement
The Auth Agent should be automatically engaged when:
- Authentication-related code is being modified
- Security scanning tools flag authentication vulnerabilities
- New authentication features are being added to the application
- Authentication dependencies are being updated

### Manual Engagement
Manually engage the Auth Agent when:
- Planning new authentication system implementations
- Reviewing authentication code for security best practices
- Investigating authentication-related issues or bugs
- Consulting on authentication architecture decisions