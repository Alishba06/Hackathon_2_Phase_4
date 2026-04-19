#!/usr/bin/env python3
"""
Script to create database tables excluding the security log to avoid the UUID issue.
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

# Load environment variables
load_dotenv()

# Import models to register them with SQLModel metadata
from src.models.user import User
from src.models.task import Task
# Temporarily exclude security_log to avoid the UUID issue

# Import the database engine configuration
from src.config.database import engine

def create_tables_excluding_security_log():
    """Create tables excluding security log."""
    print("Creating database tables (excluding security log)...")
    
    # Create metadata for only the tables we want
    # We'll create a new MetaData object with only User and Task
    from sqlalchemy import MetaData
    
    # Create a new metadata object with only the tables we want to create
    custom_metadata = MetaData()
    
    # Get the tables we want to create
    user_table = User.__table__.to_metadata(custom_metadata)
    task_table = Task.__table__.to_metadata(custom_metadata)
    
    # Create only these tables
    custom_metadata.create_all(engine)
    
    print("User and Task tables created successfully!")

if __name__ == "__main__":
    create_tables_excluding_security_log()