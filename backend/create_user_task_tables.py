#!/usr/bin/env python3
"""
Script to create only the User and Task tables to fix the missing Task table issue.
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

# Import the database engine configuration
from src.config.database import engine

def create_user_and_task_tables():
    """Create only user and task tables in the database."""
    print("Creating User and Task tables...")
    
    # Create only User and Task tables
    # We'll use a targeted approach to avoid the security log issue for now
    with engine.connect() as conn:
        # Create the tables individually
        User.metadata.create_all(engine, checkfirst=True, tables=[User.__table__, Task.__table__])
    
    print("User and Task tables created successfully!")

if __name__ == "__main__":
    create_user_and_task_tables()