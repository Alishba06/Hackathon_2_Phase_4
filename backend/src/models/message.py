from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import text
from pydantic import field_validator

if TYPE_CHECKING:
    from src.models.conversation import Conversation


class MessageBase(SQLModel):
    role: str
    content: str = Field(min_length=1, max_length=10000)
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ('user', 'assistant'):
            raise ValueError('role must be "user" or "assistant"')
        return v


class Message(MessageBase, table=True):
    __tablename__ = "message"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, sa_column_kwargs={"server_default": text("gen_random_uuid()")})
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    content: str


class MessageRead(SQLModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    content: str
    created_at: datetime
