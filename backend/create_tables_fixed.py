#!/usr/bin/env python3
"""
Script to create database tables for the Todo application with proper UUID handling.
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import MetaData, Table, Column, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID  # Import PostgreSQL UUID type
from sqlalchemy.sql import func
import uuid

# Load environment variables
load_dotenv()

# Import models to register them with SQLModel metadata
from src.models.user import User
from src.models.task import Task
from src.models.security_log import SecurityLog

# Import the database engine configuration
from src.config.database import engine

def create_all_tables():
    """Create all tables in the database."""
    print("Creating database tables...")
    
    # Create all tables
    # Use checkfirst=True to avoid errors if tables already exist
    SQLModel.metadata.create_all(engine, checkfirst=True)
    
    print("Tables created successfully!")
    
    # Print table names that were registered
    table_names = [table.name for table in SQLModel.metadata.tables.values()]
    print(f"Registered tables: {table_names}")

if __name__ == "__main__":
    create_all_tables()