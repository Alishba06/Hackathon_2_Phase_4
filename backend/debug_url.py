#!/usr/bin/env python3
"""
Debug script to check the database URL format.
"""

import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

print(f"DATABASE_URL from environment: {DATABASE_URL}")
print(f"URL Type: {type(DATABASE_URL)}")

# Parse the URL to see if it's valid
try:
    parsed = urlparse(DATABASE_URL)
    print(f"Parsed URL: {parsed}")
    print("URL parsing successful!")
except Exception as e:
    print(f"Error parsing URL: {e}")

# Check if it's a PostgreSQL URL
if DATABASE_URL.startswith("postgresql://"):
    print("\nThis is a PostgreSQL URL")
    # Check for potential problematic characters
    if '&' in DATABASE_URL:
        print("URL contains '&' character - this might cause issues")
        
        # Split the URL to separate the connection string from query parameters
        parts = DATABASE_URL.split('?')
        conn_string = parts[0]
        query_params = parts[1] if len(parts) > 1 else ""
        
        print(f"Connection string: {conn_string}")
        print(f"Query params: {query_params}")
        
        # Check if query params contain special characters
        if '&' in query_params:
            param_parts = query_params.split('&')
            print(f"Query parameters split: {param_parts}")
else:
    print("\nThis is not a PostgreSQL URL")