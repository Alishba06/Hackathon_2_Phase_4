"""
Security utilities for password hashing and verification.
"""

from passlib.context import CryptContext
import logging
from typing import Union

# Initialize CryptContext at module level
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
        
    Raises:
        ValueError: If password is None, empty, or hashing fails
    """
    # Validate input
    if not password:
        logger.error("Password is None or empty")
        raise ValueError("Password cannot be None or empty")
    
    try:
        # Ensure password is not longer than 72 bytes (bcrypt limitation)
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes and decode back to string
            password = password_bytes[:72].decode('utf-8', errors='ignore')
            logger.warning(f"Password was truncated to 72 bytes for bcrypt compatibility")
        
        # Hash the password
        hashed = pwd_context.hash(password)
        logger.debug(f"Password successfully hashed")
        return hashed
    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}", exc_info=True)
        raise ValueError("Password hashing failed") from e

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password to compare against
        
    Returns:
        True if passwords match, False otherwise
    """
    if not plain_password or not hashed_password:
        logger.warning("Either plain_password or hashed_password is None or empty")
        return False
    
    try:
        # Ensure plain password is not longer than 72 bytes (bcrypt limitation)
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes and decode back to string
            plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
        
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}", exc_info=True)
        return False