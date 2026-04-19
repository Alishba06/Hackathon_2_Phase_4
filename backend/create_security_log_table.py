#!/usr/bin/env python3
"""
Script to create only the SecurityLog table after User and Task tables exist.
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Import the SecurityLog model
from src.models.security_log import SecurityLog

# Import the database engine configuration
from src.config.database import engine

def create_security_log_table():
    """Create only the SecurityLog table."""
    print("Creating SecurityLog table...")
    
    # Create only the SecurityLog table
    with engine.connect() as conn:
        # Check if the table already exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'securitylog'
            );
        """))
        table_exists = result.scalar()
        
        if table_exists:
            print("SecurityLog table already exists.")
        else:
            # Create the SecurityLog table
            SecurityLog.metadata.create_all(engine, tables=[SecurityLog.__table__])
            print("SecurityLog table created successfully!")

if __name__ == "__main__":
    create_security_log_table()