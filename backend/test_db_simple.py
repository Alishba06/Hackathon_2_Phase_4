"""
Simple test to check if the database connection works
"""
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, select
from src.models.user import User

# Load environment variables
load_dotenv(dotenv_path="../../.env.corrected")

# Import the database engine configuration
from src.config.database import engine, DATABASE_URL

print(f"Database URL: {DATABASE_URL}")

try:
    # Test basic connection
    with engine.connect() as conn:
        print("Database connection successful!")
        
        # Test if we can query the user table
        with Session(engine) as session:
            result = session.exec(select(User).limit(1)).first()
            print(f"Query successful. Found user: {result}")
            
except Exception as e:
    print(f"Database connection failed: {e}")
    import traceback
    traceback.print_exc()