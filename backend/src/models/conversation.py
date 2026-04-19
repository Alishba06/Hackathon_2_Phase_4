from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy import text

if TYPE_CHECKING:
    from src.models.message import Message


class ConversationBase(SQLModel):
    pass


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversation"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, sa_column_kwargs={"server_default": text("gen_random_uuid()")})
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to messages
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class ConversationCreate(SQLModel):
    user_id: uuid.UUID


class ConversationRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
