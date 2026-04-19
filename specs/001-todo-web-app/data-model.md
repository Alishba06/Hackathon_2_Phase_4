# Data Model: Todo Full-Stack Web Application

## Overview
This document defines the data models for the Todo Full-Stack Web Application, including entities, fields, relationships, and validation rules.

## Entity: User

### Fields
- `id` (UUID/Integer): Unique identifier for the user
- `email` (String): User's email address (unique, required)
- `password_hash` (String): Hashed password for authentication
- `first_name` (String, optional): User's first name
- `last_name` (String, optional): User's last name
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user account was last updated
- `is_active` (Boolean): Whether the user account is active

### Relationships
- One-to-Many: A user can have many tasks

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements
- Email and password are required for account creation

## Entity: Task

### Fields
- `id` (UUID/Integer): Unique identifier for the task
- `title` (String): Title of the task (required)
- `description` (Text, optional): Detailed description of the task
- `is_completed` (Boolean): Whether the task is completed (default: false)
- `due_date` (DateTime, optional): When the task is due
- `priority` (String/Enum): Priority level (e.g., low, medium, high)
- `user_id` (UUID/Integer): Foreign key linking to the owning user
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated

### Relationships
- Many-to-One: A task belongs to one user

### Validation Rules
- Title is required and must be between 1-255 characters
- Description, if provided, must be less than 10,000 characters
- Due date, if provided, must be a future date
- Priority must be one of the allowed values (low, medium, high)
- User_id must reference an existing, active user

## State Transitions

### Task State Transitions
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user unmarks task as complete

### User State Transitions
- `inactive` → `active`: When user completes registration
- `active` → `inactive`: When user deactivates account

## Database Constraints

### Indexes
- Index on `users.email` for fast lookup during authentication
- Index on `tasks.user_id` for efficient filtering by user
- Index on `tasks.is_completed` for filtering completed/incomplete tasks

### Foreign Key Constraints
- `tasks.user_id` references `users.id` with cascade delete prevention
- Prevents deletion of users who have associated tasks

## API Response Formats

### User Response Format
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "is_active": true
}
```

### Task Response Format
```json
{
  "id": "uuid-string",
  "title": "Complete project",
  "description": "Finish the todo application project",
  "is_completed": false,
  "due_date": "2023-12-31T23:59:59Z",
  "priority": "high",
  "user_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Security Considerations

### Data Access
- All task queries must be filtered by the authenticated user's ID
- Users cannot access tasks owned by other users
- API responses should not expose sensitive user information beyond what's necessary

### Data Validation
- All inputs must be validated before database insertion
- Sanitize inputs to prevent injection attacks
- Validate user permissions before allowing operations