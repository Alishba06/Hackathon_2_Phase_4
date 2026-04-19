# When to Use the FastAPI Backend Agent

## Primary Use Cases

### 1. API Development and Refactoring
- When building new FastAPI backend APIs from scratch
- When refactoring existing FastAPI applications for better structure
- When implementing new API endpoints or modifying existing ones
- When redesigning API architecture for better performance or maintainability
- When adding new API features while maintaining existing functionality

### 2. Authentication and Authorization Implementation
- When adding JWT-based authentication to FastAPI applications
- When implementing OAuth2 flows for third-party authentication
- When setting up API key-based authentication for service-to-service communication
- When creating role-based access control (RBAC) systems
- When implementing fine-grained permission systems

### 3. Database Integration
- When connecting FastAPI applications to SQL databases (PostgreSQL, MySQL, SQLite)
- When integrating with NoSQL databases (MongoDB, etc.) in FastAPI applications
- When designing SQLAlchemy or Tortoise ORM models
- When implementing CRUD operations with proper error handling
- When optimizing database queries for performance

### 4. Request and Response Validation
- When implementing Pydantic models for request validation
- When creating response models for consistent API outputs
- When validating complex nested data structures
- When implementing custom validators for domain-specific validation
- When handling file uploads and downloads in FastAPI

### 5. Error Handling and Standardization
- When implementing centralized exception handling
- When creating custom exception classes for domain-specific errors
- When standardizing error responses across the API
- When implementing proper HTTP status code usage
- When adding comprehensive logging for error tracking

### 6. Performance Optimization
- When implementing caching strategies in FastAPI applications
- When optimizing database queries to reduce response times
- When adding pagination for large datasets
- When implementing rate limiting to prevent API abuse
- When optimizing API endpoints for minimal resource usage

## Situations Requiring Consultation

### 1. Architecture Decisions
- When choosing between different architectural patterns for FastAPI applications
- When deciding on database integration strategies
- When selecting appropriate authentication mechanisms
- When designing API versioning strategies
- When planning for scalability and microservices architecture

### 2. Security Implementation
- When implementing security measures for production APIs
- When addressing security vulnerabilities in existing code
- When designing secure authentication and authorization flows
- When handling sensitive data in FastAPI applications
- When implementing security headers and best practices

### 3. Performance Issues
- When diagnosing slow API response times
- When identifying database query performance bottlenecks
- When optimizing resource usage in production environments
- When implementing background tasks for long-running operations
- When scaling FastAPI applications to handle increased load

### 4. Integration Challenges
- When integrating FastAPI with external services
- When connecting to multiple databases or data sources
- When implementing API gateways or proxy configurations
- When handling complex data transformations
- When managing API dependencies and service communication

## Trigger Conditions

### Automatic Engagement
The FastAPI Backend Agent should be automatically engaged when:
- API endpoints return unexpected errors or status codes
- Database queries show performance degradation
- Authentication or authorization failures occur
- Validation errors appear in API requests
- Security vulnerabilities are detected in the codebase

### Manual Engagement
Manually engage the FastAPI Backend Agent when:
- Planning new API features or functionality
- Reviewing existing backend code for optimization
- Investigating backend logic issues or bugs
- Consulting on backend architecture decisions
- Implementing new security measures or authentication flows

## Scenarios to Avoid Using This Agent

### 1. Frontend-Related Tasks
- When working on frontend UI/UX elements
- When implementing client-side JavaScript functionality
- When designing user interfaces or user experience flows
- When working on frontend frameworks (React, Vue, Angular)
- When handling browser-specific functionality

### 2. Non-Python Technologies
- When working with non-Python backend technologies (Node.js, Java, etc.)
- When implementing APIs in different frameworks (Express, Spring Boot, etc.)
- When working with different database technologies without Python integration
- When handling infrastructure outside the Python/FastAPI ecosystem

### 3. Infrastructure Management
- When managing cloud infrastructure directly (AWS, Azure, GCP)
- When configuring web servers (Nginx, Apache) without FastAPI integration
- When handling container orchestration without application context
- When managing networking or security at the infrastructure level

## Integration Points

### 1. Development Workflow
- During code reviews for FastAPI-related changes
- When onboarding new team members to FastAPI practices
- When establishing backend development standards
- When creating backend documentation and best practices

### 2. Deployment Process
- During pre-deployment backend validation
- When implementing backend deployment automation
- When verifying API functionality in different environments
- When setting up backend monitoring for new deployments

### 3. Testing and QA
- When creating comprehensive backend test suites
- When implementing API contract testing
- When setting up performance testing for APIs
- When establishing backend quality metrics

## Collaboration Scenarios

### 1. Cross-Team Coordination
- When coordinating backend changes across teams
- When implementing backend changes affecting multiple services
- When establishing backend governance policies
- When creating shared backend standards

### 2. Stakeholder Communication
- When explaining backend performance impacts to stakeholders
- When justifying backend architecture decisions
- When communicating backend-related risks
- When reporting on backend optimization results

## Emergency Scenarios

### 1. Production Issues
- When diagnosing production API failures
- When addressing database connection issues
- When handling authentication system failures
- When mitigating security vulnerabilities in production

### 2. Performance Emergencies
- When APIs experience sudden performance degradation
- When database queries cause system slowdowns
- When authentication systems become unresponsive
- When validation errors affect API availability

## Maintenance Scenarios

### 1. Routine Maintenance
- When performing regular backend code reviews
- When updating dependencies in FastAPI applications
- When refactoring legacy backend code
- When improving test coverage for backend services

### 2. Upgrades and Migrations
- When upgrading FastAPI or related dependencies
- When migrating to new database schemas
- When updating authentication systems
- When implementing new API versions