import requests
import json

# Test the registration endpoint with various scenarios
BASE_URL = "http://127.0.0.1:8000"

def test_registration_with_long_password():
    """Test registering a new user with a long password (>72 bytes)"""
    # Create a password longer than 72 bytes
    long_password = "a" * 80  # 80 characters, which is definitely longer than 72 bytes
    
    register_data = {
        "email": "testlongpassword@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": long_password
    }

    try:
        print(f"Attempting to register user with password of length: {len(long_password)} characters")
        print(f"Password byte length: {len(long_password.encode('utf-8'))} bytes")
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Registration - Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful! Long password was handled correctly.")
            return True
        else:
            print("❌ Registration failed")
            return False

    except Exception as e:
        print(f"❌ Error during registration test: {str(e)}")
        return False

def test_registration_with_normal_password():
    """Test registering a new user with a normal password"""
    register_data = {
        "email": "testnormalpassword@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "simple123"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Normal Registration - Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✅ Normal registration successful!")
            return True
        else:
            print("❌ Normal registration failed")
            return False

    except Exception as e:
        print(f"❌ Error during normal registration test: {str(e)}")
        return False

def test_registration_with_duplicate_email():
    """Test registering a user with an email that already exists"""
    register_data = {
        "email": "testnormalpassword@example.com",  # Same email as previous test
        "first_name": "Duplicate",
        "last_name": "User",
        "password": "anotherpassword"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Duplicate Email Registration - Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 400:
            print("✅ Duplicate email properly rejected with 400 error!")
            return True
        else:
            print("❌ Duplicate email should have been rejected")
            return False

    except Exception as e:
        print(f"❌ Error during duplicate email test: {str(e)}")
        return False

def test_registration_with_special_characters():
    """Test registering a user with special characters and emojis in password"""
    # Create a password with multi-byte characters (emojis)
    password_with_emojis = "mypasswordwithemoji😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀"

    register_data = {
        "email": "testemojipassword@example.com",
        "first_name": "Emoji",
        "last_name": "User",
        "password": password_with_emojis
    }

    try:
        print(f"Attempting to register user with emoji password of length: {len(password_with_emojis)} characters")
        print(f"Password byte length: {len(password_with_emojis.encode('utf-8'))} bytes")
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Emoji Password Registration - Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✅ Emoji password registration successful! Special characters were handled correctly.")
            return True
        else:
            print("❌ Emoji password registration failed")
            return False

    except Exception as e:
        print(f"❌ Error during emoji password test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing registration with various scenarios...")
    print("=" * 60)
    
    # Note: Start the backend server first before running these tests
    print("Running tests...")
    
    print("\n1. Testing with long password (>72 bytes):")
    long_result = test_registration_with_long_password()
    
    print("\n2. Testing with normal password:")
    normal_result = test_registration_with_normal_password()
    
    print("\n3. Testing with duplicate email:")
    duplicate_result = test_registration_with_duplicate_email()
    
    print("\n4. Testing with special characters/emojis in password:")
    emoji_result = test_registration_with_special_characters()
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    print(f"- Long password test: {'✅ PASS' if long_result else '❌ FAIL'}")
    print(f"- Normal password test: {'✅ PASS' if normal_result else '❌ FAIL'}")
    print(f"- Duplicate email test: {'✅ PASS' if duplicate_result else '❌ FAIL'}")
    print(f"- Emoji password test: {'✅ PASS' if emoji_result else '❌ FAIL'}")
    
    all_passed = long_result and normal_result and duplicate_result and emoji_result
    if all_passed:
        print("\n🎉 All tests passed! The fix is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
        
    print("\nTest completed.")