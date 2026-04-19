#!/usr/bin/env python3
"""
Debug script to check the database URL format.
"""

import os
from dotenv import load_dotenv
import sys

# Print where we're looking for .env
print(f"Current working directory: {os.getcwd()}")

# Load environment variables from the current directory only
env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_path):
    print(f"Loading .env from: {env_path}")
    load_dotenv(env_path)
else:
    print(f"No .env file found at: {env_path}")
    # Try loading from parent directory
    parent_env_path = os.path.join(os.pardir, '.env')
    if os.path.exists(parent_env_path):
        print(f"Loading .env from parent: {parent_env_path}")
        load_dotenv(parent_env_path)
    else:
        print(f"No .env file found at: {parent_env_path}")

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

print(f"DATABASE_URL from environment: {repr(DATABASE_URL)}")
print(f"DATABASE_URL length: {len(DATABASE_URL)}")

# Check if the URL starts with the expected format
if DATABASE_URL.startswith("postgresql://"):
    print("URL starts with postgresql:// - this is correct")
else:
    print("URL does NOT start with postgresql:// - this is the issue!")