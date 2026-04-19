#!/usr/bin/env python3
"""
Debug script to test the password validation in the UserCreate model
"""

from src.models.user import UserCreate
from src.services.auth_service import get_password_hash

def test_password_validation():
    print("Testing password validation in UserCreate model...")
    
    # Test with a long password
    long_password = "a" * 80  # 80 characters, which is definitely longer than 72 bytes
    print(f"Original password length: {len(long_password)} characters")
    print(f"Original password byte length: {len(long_password.encode('utf-8'))} bytes")
    
    try:
        # Create a UserCreate object - this should trigger the validation
        user_create = UserCreate(
            email="test@example.com",
            password=long_password,
            first_name="Test",
            last_name="User"
        )
        
        print(f"After validation - password length: {len(user_create.password)} characters")
        print(f"After validation - password byte length: {len(user_create.password.encode('utf-8'))} bytes")
        print(f"Password after validation: {repr(user_create.password)}")
        
        # Now test the hashing function
        print("\nTesting password hashing...")
        hashed = get_password_hash(user_create.password)
        print("Password hashing succeeded!")
        
    except Exception as e:
        print(f"Error during validation/hashing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_validation()