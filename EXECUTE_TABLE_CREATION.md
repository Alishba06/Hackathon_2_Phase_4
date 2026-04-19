# Creating Tables in Neon Postgres for Todo Application

This guide explains how to create the required database tables in your Neon Postgres database for the Todo application.

## Method 1: Using psql command line

1. Connect to your Neon Postgres database using psql:
```bash
psql 'postgresql://neondb_owner:npg_QxwPX3uAly9t@ep-twilight-violet-ahbkcefb-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

2. Once connected, run the following command to execute the SQL script:
```sql
\i create_todo_tables.sql
```

## Method 2: Using the Neon Console

1. Log in to your Neon account at https://console.neon.tech/
2. Select your project
3. Click on the "SQL Editor" tab
4. Copy and paste the contents of `create_todo_tables.sql` into the editor
5. Click "Run" to execute the script

## Method 3: Using a Database Client

1. Connect to your Neon Postgres database using any PostgreSQL-compatible client (like DBeaver, pgAdmin, etc.)
2. Open the `create_todo_tables.sql` file
3. Execute the script

## Expected Output

After successful execution, you should see a confirmation message indicating that the tables were created successfully.

The script creates:

1. A `user` table with fields for user identification, authentication, and metadata
2. A `task` table with fields for task details, status, priority, and user association
3. Proper indexing for optimized queries
4. Triggers to automatically update timestamps
5. Foreign key constraints to maintain referential integrity

## Verification

To verify that the tables were created successfully, run these queries:

```sql
-- List all tables
\dt

-- Check the structure of the user table
\d user;

-- Check the structure of the task table
\d task;
```

## Troubleshooting

If you encounter any issues:

1. Make sure your connection string is correct
2. Verify that you have the necessary privileges to create tables
3. Check that the UUID extension is available (the script enables it if needed)
4. Ensure that the database is accessible and not in read-only mode