from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
from pydantic import field_validator

def generate_uuid():
    return str(uuid.uuid4())

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True

class User(UserBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True, max_length=36)  # UUID is 36 chars
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Additional authentication-related fields
    last_login: Optional[datetime] = Field(default=None)
    failed_login_attempts: int = Field(default=0)
    locked_until: Optional[datetime] = Field(default=None)

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        # Ensure password is not longer than 72 bytes for bcrypt
        if len(v.encode('utf-8')) > 72:
            # Truncate the password to 72 bytes
            v = v.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return v

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    failed_login_attempts: int
    locked_until: Optional[datetime]

class UserUpdate(SQLModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    last_login: Optional[datetime] = None
    failed_login_attempts: Optional[int] = None
    locked_until: Optional[datetime] = None