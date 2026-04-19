import requests
import json

# Test the registration endpoint with a simple request
BASE_URL = "http://127.0.0.1:8000"

def test_basic_registration():
    """Test basic registration with minimal data"""
    register_data = {
        "email": "testbasic@example.com",
        "password": "simplepass123",
        "first_name": "Test",
        "last_name": "User"
    }

    try:
        print(f"Sending registration request to: {BASE_URL}/api/auth/register")
        print(f"Data: {json.dumps(register_data, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/auth/register", 
            json=register_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")

        return response
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Could not connect to the server")
        print("Make sure the backend server is running on http://127.0.0.1:8000")
        return None
    except Exception as e:
        print(f"❌ Error during registration test: {str(e)}")
        return None

def test_registration_with_validation_error():
    """Test registration with intentionally invalid data to see error format"""
    # Send incomplete data to trigger validation error
    register_data = {
        "email": "testinvalid@example.com",
        # Missing required password field
    }

    try:
        print(f"\nSending invalid registration request to: {BASE_URL}/api/auth/register")
        print(f"Data: {json.dumps(register_data, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/auth/register", 
            json=register_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        return response
        
    except Exception as e:
        print(f"❌ Error during invalid registration test: {str(e)}")
        return None

if __name__ == "__main__":
    print("🔍 Testing backend registration endpoint...")
    print("=" * 60)
    
    # Test basic registration
    response = test_basic_registration()
    
    if response:
        if response.status_code == 200:
            print("\n✅ Backend registration endpoint is working correctly!")
        else:
            print(f"\n❌ Backend registration endpoint returned error: {response.status_code}")
            
            # If it failed, try the validation error test to see what kind of error we get
            test_registration_with_validation_error()
    else:
        print("\n❌ Could not connect to backend server. Please make sure it's running.")