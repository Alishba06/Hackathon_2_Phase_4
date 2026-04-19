from src.utils.security import hash_password

try:
    print("Testing password hashing...")
    result = hash_password("shortpass")
    print(f"Success: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()