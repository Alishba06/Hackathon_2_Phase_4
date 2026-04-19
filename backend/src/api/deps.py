"""
Dependency injection functions for the Todo application.

This module provides dependency functions for FastAPI to inject
commonly used objects like the current user.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..models.user import User
from ..utils.jwt_utils import verify_token, get_current_user_email
from ..services.auth_service import get_user_by_email


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Dependency function to get the current authenticated user.
    
    This function extracts the JWT token from the Authorization header,
    verifies it, and returns the corresponding User object.
    
    Args:
        credentials: HTTP authorization credentials from the request header
    
    Returns:
        User object for the authenticated user
    
    Raises:
        HTTPException: If the token is invalid or the user doesn't exist
    """
    token = credentials.credentials
    
    # Verify the token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract email from token
    email = get_current_user_email(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Retrieve user from database
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency function to get the current active user.
    
    This function ensures the user is active in addition to being authenticated.
    
    Args:
        current_user: The authenticated user (from get_current_user dependency)
    
    Returns:
        User object for the authenticated and active user
    
    Raises:
        HTTPException: If the user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user