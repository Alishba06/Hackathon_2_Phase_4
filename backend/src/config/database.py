from sqlmodel import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - use environment variable or default to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)