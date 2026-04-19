# When to Use the Database Agent

## Primary Use Cases

### 1. Neon Serverless PostgreSQL Operations
- When setting up new Neon PostgreSQL instances
- When configuring Neon-specific features like branching and serverless scaling
- When optimizing database settings for Neon's serverless architecture
- When implementing Neon's unique features like isolated branches for development

### 2. Performance Issues
- When database queries are running slowly or inefficiently
- When experiencing high database load or resource utilization
- When identifying and resolving performance bottlenecks
- When optimizing database connections in serverless environments

### 3. Schema Design and Refactoring
- When designing new database schemas for PostgreSQL
- When refactoring existing database schemas for better performance
- When implementing database normalization or denormalization
- When adding new tables, relationships, or constraints

### 4. Migration Management
- When planning and executing database schema migrations
- When implementing zero-downtime migration strategies
- When handling backward compatibility during database changes
- When creating rollback procedures for database migrations

### 5. Security Enhancements
- When implementing database security measures
- When configuring user roles and permissions
- When securing database connections and credentials
- When implementing data encryption and access controls

### 6. Scaling and Capacity Planning
- When planning for database growth and scaling
- When optimizing database resources for traffic increases
- When implementing sharding or partitioning strategies
- When evaluating database performance under load

## Situations Requiring Consultation

### 1. Architecture Decisions
- When choosing between different database architectures
- When deciding on indexing strategies for specific use cases
- When selecting appropriate data types for specific requirements
- When designing complex relationships between entities

### 2. Performance Optimization
- When analyzing slow query logs and execution plans
- When identifying database performance bottlenecks
- When optimizing connection pooling for serverless environments
- When implementing caching strategies for database queries

### 3. Production Issues
- When diagnosing database-related production issues
- When investigating data inconsistency problems
- When resolving database locking or deadlock situations
- When handling database outage recovery

### 4. Compliance Requirements
- When implementing database changes to meet regulatory requirements
- When ensuring GDPR, HIPAA, or other compliance standards
- When implementing audit logging for database operations
- When securing sensitive data in the database

## Trigger Conditions

### Automatic Engagement
The Database Agent should be automatically engaged when:
- Database performance degrades significantly
- Slow query alerts are triggered
- Connection pool exhaustion occurs
- Database security vulnerabilities are detected

### Manual Engagement
Manually engage the Database Agent when:
- Planning new database features or schema changes
- Reviewing existing database code for optimization
- Investigating database-related bugs or issues
- Consulting on database architecture decisions

## Scenarios to Avoid Using This Agent

### 1. Non-Database Related Tasks
- When working on frontend UI/UX elements
- When implementing business logic unrelated to databases
- When performing general application maintenance
- When working on infrastructure outside the database layer

### 2. Different Database Technologies
- When working with non-PostgreSQL databases (MySQL, MongoDB, etc.)
- When using different database providers (not Neon)
- When implementing in-memory data stores (Redis, Memcached)
- When working with file-based data storage

### 3. Application-Level Optimizations
- When optimizing application code performance
- When implementing application-level caching
- When working on API response times unrelated to database queries
- When optimizing frontend performance

## Integration Points

### 1. Development Workflow
- During code reviews for database-related changes
- When onboarding new team members to database practices
- When establishing database development standards
- When creating database documentation

### 2. Deployment Process
- During pre-deployment database schema validation
- When implementing database deployment automation
- When verifying database migrations in different environments
- When setting up database monitoring for new deployments

### 3. Monitoring and Alerting
- When configuring database performance alerts
- When setting up database health checks
- When establishing database usage reporting
- When implementing database anomaly detection

## Collaboration Scenarios

### 1. Cross-Team Coordination
- When coordinating database changes across teams
- When implementing database changes affecting multiple services
- When establishing database governance policies
- When creating shared database standards

### 2. Stakeholder Communication
- When explaining database performance impacts to stakeholders
- When justifying database infrastructure costs
- When communicating database-related risks
- When reporting on database optimization results