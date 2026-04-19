import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print raw environment variable
raw_db_url = os.environ.get("DATABASE_URL", "")
print(f"Raw DATABASE_URL: {repr(raw_db_url)}")

# Check if it contains any unexpected characters
if "psql" in raw_db_url and "postgresql://" in raw_db_url:
    print("Detected the issue: psql command is mixed with postgresql URL")
    # Fix the URL by removing the psql part
    if raw_db_url.startswith("psql '") and raw_db_url.endswith("'"):
        fixed_url = raw_db_url[6:-1]  # Remove "psql '" from start and "'" from end
        print(f"Fixed URL: {repr(fixed_url)}")
        raw_db_url = fixed_url

print(f"Final DATABASE_URL: {repr(raw_db_url)}")