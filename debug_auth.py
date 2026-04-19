import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend', 'src'))

from services.auth_service import authenticate_user

def test_auth():
    print("Testing authentication function directly...")
    
    # Test with a non-existent user
    result = authenticate_user("nonexistent@example.com", "somepassword")
    print(f"Result for non-existent user: {result}")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_auth()