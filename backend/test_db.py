import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
print(f"DATABASE_URL: {repr(DATABASE_URL)}")
print(f"Starts with postgresql: {DATABASE_URL.startswith('postgresql')}")

if DATABASE_URL.startswith("postgresql"):
    # For PostgreSQL, we need to handle async/await differently
    # For now, let's use a synchronous connection
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    print(f"Updated DATABASE_URL: {repr(DATABASE_URL)}")

from sqlalchemy import create_engine
try:
    engine = create_engine(DATABASE_URL, echo=True)
    print("Engine created successfully!")
except Exception as e:
    print(f"Error creating engine: {e}")