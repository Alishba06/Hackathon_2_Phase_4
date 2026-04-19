import requests
import json

# Test the registration endpoint
BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test registering a new user"""
    # Register a new user with a short password to avoid bcrypt 72-byte limit
    register_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "simple123"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Registration - Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Registration successful!")
        else:
            print("Registration failed")
            
    except Exception as e:
        print(f"Error during registration test: {str(e)}")

if __name__ == "__main__":
    print("Testing registration endpoint...")
    test_registration()
    print("Test completed.")