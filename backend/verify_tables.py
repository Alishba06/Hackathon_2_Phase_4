#!/usr/bin/env python3
"""
Script to verify that all tables exist in the database.
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Import models to register them with SQLModel metadata
from src.models.user import User
from src.models.task import Task
from src.models.security_log import SecurityLog

# Import the database engine configuration
from src.config.database import engine

def verify_tables_exist():
    """Verify that all tables exist in the database."""
    print("Verifying that all tables exist...")
    
    with engine.connect() as conn:
        # Query to get all table names in the public schema
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables in database: {tables}")
        
        # Check for our specific tables
        expected_tables = ['user', 'task', 'securitylog']
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            print(f"Missing tables: {missing_tables}")
        else:
            print("All expected tables exist!")
            
        # Check the structure of the task table specifically
        print("\nChecking Task table structure:")
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'task'
            ORDER BY ordinal_position;
        """))
        
        for row in result.fetchall():
            print(f"  {row[0]}: {row[1]}, nullable: {row[2]}")

if __name__ == "__main__":
    verify_tables_exist()