"""
JWT utility functions for the Todo application.

This module provides utility functions for creating and verifying
JWT tokens used for authentication.
"""

from datetime import datetime, timedelta
from typing import Optional
import os
from jose import jwt, JWTError

from ..config.security import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_DELTA
from ..models.user import User


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token with the provided data.
    
    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration
    
    Returns:
        Encoded JWT token as a string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE_DELTA
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid.
    
    Args:
        token: JWT token to verify
    
    Returns:
        Payload dictionary if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def create_user_token(user: User) -> str:
    """
    Create an access token for a specific user.
    
    Args:
        user: User object for whom to create the token
    
    Returns:
        Encoded JWT token as a string
    """
    data = {
        "sub": user.email,
        "user_id": user.id,
        "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE_DELTA
    }
    return create_access_token(data)


def get_current_user_email(token: str) -> Optional[str]:
    """
    Extract the user's email from a JWT token.
    
    Args:
        token: JWT token to extract email from
    
    Returns:
        User's email if token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        email: str = payload.get("sub")
        if email:
            return email
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired.

    Args:
        token: JWT token to check

    Returns:
        True if token is expired, False otherwise
    """
    payload = verify_token(token)
    if payload:
        exp = payload.get("exp")
        if exp:
            return datetime.fromtimestamp(exp) < datetime.utcnow()
    return True  # If we can't decode the token, treat it as expired


def validate_token_signature(token: str) -> bool:
    """
    Validate the signature of a JWT token.

    Args:
        token: JWT token to validate

    Returns:
        True if signature is valid, False otherwise
    """
    try:
        # This will raise an exception if the signature is invalid
        jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return True
    except JWTError:
        return False


def validate_token_claims(token: str) -> Optional[dict]:
    """
    Validate the claims in a JWT token.

    Args:
        token: JWT token to validate

    Returns:
        Claims dictionary if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        # Check that required claims are present
        if "sub" not in payload:
            return None

        # Check that the subject (email) is not empty
        if not payload["sub"]:
            return None

        # Check that the token hasn't expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            return None

        return payload
    except JWTError:
        return None