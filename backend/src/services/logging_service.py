"""
Security logging service for the Todo application.

This module provides functions for logging security-related events
such as authentication attempts, access violations, etc.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
import logging
from enum import Enum

from ..models.user import User
from ..models.security_log import SecurityLog, SecurityEventType
from ..config.database import engine


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_security_event(
    event_type: SecurityEventType,
    user_id: Optional[str] = None,
    endpoint: Optional[str] = None,
    method: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status_code: Optional[int] = None,
    details: Optional[str] = None
) -> SecurityLog:
    """
    Log a security event to the database and application logs.
    
    Args:
        event_type: Type of security event
        user_id: ID of the user associated with the event (if any)
        endpoint: The API endpoint that was accessed
        method: HTTP method used (GET, POST, PUT, DELETE, etc.)
        ip_address: IP address of the requesting client
        user_agent: User agent string of the requesting client
        status_code: HTTP status code returned
        details: Additional details about the event
    
    Returns:
        SecurityLog object that was created
    """
    # Create security log entry
    security_log = SecurityLog(
        user_id=user_id,
        endpoint=endpoint,
        method=method,
        ip_address=ip_address,
        user_agent=user_agent,
        status_code=status_code,
        timestamp=datetime.utcnow(),
        event_type=event_type,
        details=details
    )
    
    # Save to database
    with Session(engine) as session:
        session.add(security_log)
        session.commit()
        session.refresh(security_log)
    
    # Also log to application logs
    log_msg = f"Security Event: {event_type.value} - "
    if user_id:
        log_msg += f"User: {user_id} - "
    if endpoint:
        log_msg += f"Endpoint: {endpoint} - "
    if ip_address:
        log_msg += f"IP: {ip_address} - "
    if details:
        log_msg += f"Details: {details}"
    
    if event_type in [SecurityEventType.AUTH_FAILURE, SecurityEventType.UNAUTHORIZED_ACCESS, SecurityEventType.USER_ISOLATION_VIOLATION]:
        logger.warning(log_msg)
    else:
        logger.info(log_msg)
    
    return security_log


def log_authentication_success(user: User, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> SecurityLog:
    """
    Log a successful authentication event.
    
    Args:
        user: User object that authenticated successfully
        ip_address: IP address of the requesting client
        user_agent: User agent string of the requesting client
    
    Returns:
        SecurityLog object that was created
    """
    return log_security_event(
        event_type=SecurityEventType.AUTH_SUCCESS,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=f"Successful login for user {user.email}"
    )


def log_authentication_failure(email: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None, reason: Optional[str] = None) -> SecurityLog:
    """
    Log a failed authentication event.
    
    Args:
        email: Email address that failed authentication
        ip_address: IP address of the requesting client
        user_agent: User agent string of the requesting client
        reason: Reason for authentication failure
    
    Returns:
        SecurityLog object that was created
    """
    details = f"Failed login attempt for email: {email}"
    if reason:
        details += f" - Reason: {reason}"
    
    return log_security_event(
        event_type=SecurityEventType.AUTH_FAILURE,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )


def log_unauthorized_access(user_id: Optional[str], endpoint: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> SecurityLog:
    """
    Log an unauthorized access attempt.
    
    Args:
        user_id: ID of the user attempting access (if known)
        endpoint: Endpoint that was accessed without authorization
        ip_address: IP address of the requesting client
        user_agent: User agent string of the requesting client
    
    Returns:
        SecurityLog object that was created
    """
    return log_security_event(
        event_type=SecurityEventType.UNAUTHORIZED_ACCESS,
        user_id=user_id,
        endpoint=endpoint,
        ip_address=ip_address,
        user_agent=user_agent,
        details=f"Unauthorized access attempt to {endpoint}"
    )


def log_user_isolation_violation(accessing_user_id: str, target_user_id: str, endpoint: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> SecurityLog:
    """
    Log a user isolation violation.
    
    Args:
        accessing_user_id: ID of the user attempting unauthorized access
        target_user_id: ID of the user whose resources were accessed
        endpoint: Endpoint that was accessed in violation
        ip_address: IP address of the requesting client
        user_agent: User agent string of the requesting client
    
    Returns:
        SecurityLog object that was created
    """
    return log_security_event(
        event_type=SecurityEventType.USER_ISOLATION_VIOLATION,
        user_id=accessing_user_id,
        endpoint=endpoint,
        ip_address=ip_address,
        user_agent=user_agent,
        details=f"User {accessing_user_id} attempted to access resources of user {target_user_id}"
    )


def log_token_validation_failure(token: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None, reason: Optional[str] = None) -> SecurityLog:
    """
    Log a JWT token validation failure.
    
    Args:
        token: The token that failed validation
        ip_address: IP address of the requesting client
        user_agent: User agent string of the requesting client
        reason: Reason for token validation failure
    
    Returns:
        SecurityLog object that was created
    """
    details = f"JWT token validation failed"
    if reason:
        details += f" - Reason: {reason}"
    
    return log_security_event(
        event_type=SecurityEventType.TOKEN_VALIDATION_FAILURE,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )


def get_security_logs_by_user(user_id: str, limit: int = 100) -> list[SecurityLog]:
    """
    Retrieve security logs for a specific user.
    
    Args:
        user_id: ID of the user to retrieve logs for
        limit: Maximum number of logs to return
    
    Returns:
        List of SecurityLog objects
    """
    with Session(engine) as session:
        statement = select(SecurityLog).where(SecurityLog.user_id == user_id).order_by(SecurityLog.timestamp.desc()).limit(limit)
        logs = session.exec(statement).all()
        return logs


def get_security_logs_by_event_type(event_type: SecurityEventType, limit: int = 100) -> list[SecurityLog]:
    """
    Retrieve security logs of a specific event type.
    
    Args:
        event_type: Type of security event to retrieve
        limit: Maximum number of logs to return
    
    Returns:
        List of SecurityLog objects
    """
    with Session(engine) as session:
        statement = select(SecurityLog).where(SecurityLog.event_type == event_type).order_by(SecurityLog.timestamp.desc()).limit(limit)
        logs = session.exec(statement).all()
        return logs