"""
Authentication service for the Todo application.

This module provides functions for user authentication,
registration, and token management.
"""

from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
import logging

from ..models.user import User, UserCreate
from ..utils.jwt_utils import create_user_token
from ..config.database import engine
from ..utils.security import hash_password, verify_password


def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with the provided email and password.

    Args:
        email: User's email address
        password: User's plaintext password

    Returns:
        User object if authentication is successful, None otherwise
    """
    user = get_user_by_email(email)

    if not user:
        # To prevent timing attacks, we simulate the work that would be done
        # if the user existed by creating a dummy hash and verifying against it
        # but we do it in a way that avoids the error with empty strings
        try:
            # Create a dummy hash to simulate the same computational effort
            from ..utils.security import pwd_context
            dummy_hash = pwd_context.hash("dummy_password_for_timing_attack_prevention")
            # Verify the password against the dummy hash to simulate processing time
            verify_password(password, dummy_hash)
        except Exception:
            # If there's an error during verification, we still return None
            # but we don't propagate the error to prevent information leakage
            pass
        return None

    if not verify_password(password, user.password_hash):
        # Update failed login attempts
        update_failed_login_attempts(user.id, user.failed_login_attempts + 1)
        return None

    # Reset failed login attempts on successful login
    reset_failed_login_attempts(user.id)

    # Update last login time
    update_last_login(user.id)

    return user


def get_user_by_email(email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.

    Args:
        email: User's email address

    Returns:
        User object if found, None otherwise
    """
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user


def get_user_by_id(user_id: str) -> Optional[User]:
    """
    Retrieve a user by their ID.

    Args:
        user_id: User's ID

    Returns:
        User object if found, None otherwise
    """
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user


def create_user(user_create: UserCreate) -> User:
    """
    Create a new user with the provided information.

    Args:
        user_create: UserCreate object with user information

    Returns:
        Created User object
    """
    # Check if user already exists
    existing_user = get_user_by_email(user_create.email)
    if existing_user:
        raise ValueError(f"User with email '{user_create.email}' already exists")

    # Hash the password using the utility function
    hashed_password = hash_password(user_create.password)

    # Create the user object
    user = User(
        email=user_create.email,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        password_hash=hashed_password
    )

    # Save to database
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_last_login(user_id: str) -> None:
    """
    Update the last login time for a user.

    Args:
        user_id: ID of the user to update
    """
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user:
            user.last_login = datetime.utcnow()
            session.add(user)
            session.commit()


def update_failed_login_attempts(user_id: str, attempts: int) -> None:
    """
    Update the failed login attempts count for a user.

    Args:
        user_id: ID of the user to update
        attempts: New number of failed login attempts
    """
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user:
            user.failed_login_attempts = attempts
            # Lock account if too many failed attempts
            if attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            session.add(user)
            session.commit()


def reset_failed_login_attempts(user_id: str) -> None:
    """
    Reset the failed login attempts count for a user.

    Args:
        user_id: ID of the user to update
    """
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if user:
            user.failed_login_attempts = 0
            user.locked_until = None
            session.add(user)
            session.commit()


def is_account_locked(user: User) -> bool:
    """
    Check if a user's account is locked.

    Args:
        user: User object to check

    Returns:
        True if account is locked, False otherwise
    """
    if user.locked_until:
        return datetime.utcnow() < user.locked_until
    return False