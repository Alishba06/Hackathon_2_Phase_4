"""
Security log model for the Todo application.

This module defines the data model for security-related logs.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

def generate_uuid():
    return str(uuid.uuid4())


class SecurityEventType(str, Enum):
    """Enumeration of possible security event types."""
    ACCESS_ATTEMPT = "access_attempt"
    AUTH_FAILURE = "auth_failure"
    AUTH_SUCCESS = "auth_success"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    TOKEN_VALIDATION_FAILURE = "token_validation_failure"
    USER_ISOLATION_VIOLATION = "user_isolation_violation"


class SecurityLog(SQLModel, table=True):
    """Model for storing security-related events."""

    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key="user.id", nullable=True, max_length=36)  # UUID is 36 chars
    endpoint: Optional[str] = Field(default=None, max_length=255)
    method: Optional[str] = Field(default=None, max_length=10)  # GET, POST, PUT, DELETE, etc.
    ip_address: Optional[str] = Field(default=None, max_length=45)  # Support for IPv6
    user_agent: Optional[str] = Field(default=None)
    status_code: Optional[int] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: SecurityEventType
    details: Optional[str] = Field(default=None)