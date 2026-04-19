"""
Debug script to test the authentication function directly
"""
import sys
import os

# Add the src directory to the Python path (we're already in the backend directory)
sys.path.insert(0, 'src')

from src.services.auth_service import authenticate_user

# Test the authentication function directly
print("Testing authentication function...")

try:
    # Try to authenticate with a test user
    user = authenticate_user("test@example.com", "password")
    print(f"Authentication result: {user}")
    
    if user is None:
        print("User not found or authentication failed")
    else:
        print(f"User authenticated: {user.email}")
        
except Exception as e:
    print(f"Error during authentication: {e}")
    import traceback
    traceback.print_exc()