---
name: database-skill
description: Design and manage database tables, schemas, and migrations with best practices. Use for backend and full-stack applications.
---

# Database Skill – Schema Design & Migrations

## Instructions

1. **Schema Design**
   - Identify entities and relationships
   - Normalize tables (avoid data redundancy)
   - Define primary keys and foreign keys
   - Choose appropriate data types
   - Enforce constraints (NOT NULL, UNIQUE, CHECK)

2. **Table Creation**
   - Create scalable and extensible table structures
   - Use naming conventions (snake_case, plural tables)
   - Add timestamp fields (`created_at`, `updated_at`)
   - Design indexes for frequently queried columns

3. **Migrations**
   - Write forward and backward (rollback) migrations
   - Keep migrations atomic and reversible
   - Version control all migration files
   - Avoid destructive changes in production
   - Seed essential data when required

4. **Relationships**
   - One-to-One
   - One-to-Many
   - Many-to-Many (junction tables)
   - Enforce referential integrity

## Best Practices
- Prefer UUIDs for distributed systems
- Index foreign keys and search fields
- Avoid over-indexing
- Plan for future scalability
- Document schema decisions clearly
- Keep business logic out of the database
- Use transactions for critical operations

## Example Structure
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  is_completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
