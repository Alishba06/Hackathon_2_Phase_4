"""
Pydantic models for user authentication.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class UserCreate(BaseModel):
    """
    Model for user registration data.
    """
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """
        Validate password meets security requirements.
        """
        if not v:
            raise ValueError('Password cannot be empty')
        
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for password complexity
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        
        # Ensure password is not longer than 72 bytes for bcrypt compatibility
        if len(v.encode('utf-8')) > 72:
            # Truncate to 72 bytes
            v = v.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v):
        """
        Validate name fields.
        """
        if v is not None and len(v.strip()) == 0:
            return None
        return v


class UserLogin(BaseModel):
    """
    Model for user login data.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Model for user response data.
    """
    id: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True