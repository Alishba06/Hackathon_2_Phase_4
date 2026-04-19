#!/usr/bin/env python3
"""
Database initialization script for the Todo application.
This script creates the necessary tables in the Neon Postgres database.
"""

import asyncio
from sqlmodel import SQLModel
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models to register them with SQLModel metadata
from src.models.user import User
from src.models.task import Task


def init_db():
    """Initialize the database by creating all tables."""
    # Get database URL from environment variable
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    # Create the database engine
    engine = create_engine(database_url, echo=True)
    
    # Create all tables defined in the models
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()