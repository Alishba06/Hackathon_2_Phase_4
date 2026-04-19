#!/usr/bin/env python3
"""
Debug script to check the database URL format.
"""

import os
from dotenv import load_dotenv

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

print(f"Current working directory: {os.getcwd()}")
print(f"DATABASE_URL from environment: {repr(DATABASE_URL)}")
print(f"DATABASE_URL length: {len(DATABASE_URL)}")

# Check if the URL starts with the expected format
if DATABASE_URL.startswith("postgresql://"):
    print("URL starts with postgresql:// - this is correct")
else:
    print("URL does NOT start with postgresql:// - this is the issue!")

# Print each character to see if there are hidden characters
print("\nCharacter-by-character breakdown:")
for i, char in enumerate(DATABASE_URL[:100]):  # Just first 100 chars
    print(f"{i:2}: '{char}' (ASCII: {ord(char)})")