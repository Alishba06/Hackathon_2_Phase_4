#!/usr/bin/env python3
"""
Script to connect to Neon Postgres and create all required tables for the Todo app.
"""

import os
import sys
import subprocess
from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv
from urllib.parse import urlparse

# Add backend/src to the Python path so we can import the models
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Load environment variables from .env file
load_dotenv()

# Import models to register them with SQLModel metadata
from models.user import User
from models.task import Task


def validate_database_url():
    """Validate the DATABASE_URL format."""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        # Try to load from the corrected env file
        load_dotenv('.env.corrected')
        database_url = os.getenv("DATABASE_URL")
        
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set in .env file")
    
    # Check if the URL starts with psql command (incorrect format)
    if database_url.startswith('psql'):
        raise ValueError("DATABASE_URL format is incorrect. It should be a PostgreSQL connection string, not a psql command.")
    
    # Validate the URL format
    try:
        parsed = urlparse(database_url)
        if not all([parsed.scheme, parsed.hostname, parsed.path]):
            raise ValueError("Invalid PostgreSQL URL format")
    except Exception:
        raise ValueError("Invalid PostgreSQL URL format")
    
    return database_url


def create_tables():
    """Connect to Neon Postgres and create all required tables."""
    try:
        # Validate and get the database URL
        database_url = validate_database_url()
        
        print(f"Connecting to Neon Postgres database...")
        
        # Create the database engine
        engine = create_engine(database_url, echo=True)
        
        # Create all tables defined in the models
        print("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\nTables created: {tables}")
        
        if 'user' in tables and 'task' in tables:
            print("\n✅ All required tables for the Todo app have been created successfully!")
        else:
            print("\n❌ Some required tables may be missing.")
            
    except Exception as e:
        print(f"❌ Error connecting to database or creating tables: {str(e)}")
        raise


if __name__ == "__main__":
    create_tables()