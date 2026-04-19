"""
Script to update the database schema with missing columns for the User table.
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Import the database engine configuration
from src.config.database import engine

def update_user_table_schema():
    """Add missing columns to the user table."""
    print("Updating user table schema...")
    
    with engine.connect() as conn:
        # Check if the columns exist, and if not, add them
        try:
            # Add last_login column if it doesn't exist
            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='user' AND column_name='last_login') THEN
                        ALTER TABLE "user" ADD COLUMN last_login TIMESTAMP WITH TIME ZONE DEFAULT NULL;
                    END IF;
                END $$;
            """))
            
            # Add failed_login_attempts column if it doesn't exist
            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='user' AND column_name='failed_login_attempts') THEN
                        ALTER TABLE "user" ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
                    END IF;
                END $$;
            """))
            
            # Add locked_until column if it doesn't exist
            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='user' AND column_name='locked_until') THEN
                        ALTER TABLE "user" ADD COLUMN locked_until TIMESTAMP WITH TIME ZONE DEFAULT NULL;
                    END IF;
                END $$;
            """))
            
            # Commit the transaction
            conn.commit()
            print("User table schema updated successfully!")
            
        except Exception as e:
            print(f"Error updating user table schema: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    update_user_table_schema()