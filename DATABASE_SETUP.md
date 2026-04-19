# Database Setup for Todo Application

This document explains how to set up the database for the Todo application using Neon Postgres.

## Prerequisites

- Python 3.8+
- PostgreSQL client tools
- Access to a Neon Postgres database

## Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Update the `.env` file with your Neon Postgres connection string:
```bash
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

## Database Initialization

### Option 1: Using the initialization script (recommended)

```bash
cd backend
python init_db.py
```

### Option 2: Using Alembic migrations

1. Install alembic if not already installed:
```bash
pip install alembic
```

2. Configure the database URL in `alembic.ini`:
```ini
sqlalchemy.url = postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

3. Run the migration:
```bash
cd backend
alembic upgrade head
```

### Option 3: Manual SQL execution

Execute the SQL statements in `todo_database_schema.sql` directly in your Neon Postgres database.

## Database Schema

The application uses two main tables:

### User Table
- `id`: UUID, primary key
- `email`: String, unique and indexed
- `first_name`: String (optional)
- `last_name`: String (optional)
- `password_hash`: Text
- `is_active`: Boolean, default true
- `created_at`: Timestamp with timezone
- `updated_at`: Timestamp with timezone

### Task Table
- `id`: UUID, primary key
- `title`: String, required
- `description`: Text (optional)
- `is_completed`: Boolean, default false
- `due_date`: Timestamp with timezone (optional)
- `priority`: String, enum ('low', 'medium', 'high'), default 'medium'
- `user_id`: UUID, foreign key referencing user(id)
- `created_at`: Timestamp with timezone
- `updated_at`: Timestamp with timezone

## Indexes

- User email field is indexed for faster lookups
- Task user_id, is_completed, due_date, and priority fields are indexed for efficient queries

## Triggers

- Both tables have triggers that automatically update the `updated_at` field whenever a record is modified