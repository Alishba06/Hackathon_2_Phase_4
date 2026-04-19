"""Chat API Schemas for AI Todo Chatbot."""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any, Dict
from datetime import datetime
import uuid


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=10000, description="User's natural language message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for continuity")


class ToolCallInput(BaseModel):
    """Input for a tool call."""
    tool: str = Field(..., description="Name of the MCP tool called")
    input: Dict[str, Any] = Field(..., description="Input parameters passed to the tool")
    output: Optional[Dict[str, Any]] = Field(None, description="Output returned by the tool")


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    conversation_id: str = Field(..., description="Conversation ID for continuity")
    response: str = Field(..., description="AI-generated natural language response")
    tool_calls: List[ToolCallInput] = Field(default_factory=list, description="List of MCP tools invoked")


class MessageCreate(BaseModel):
    """Schema for creating a message."""
    conversation_id: str
    user_id: str
    role: str
    content: str = Field(..., min_length=1, max_length=10000)
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ('user', 'assistant'):
            raise ValueError('role must be "user" or "assistant"')
        return v


class MessageRead(BaseModel):
    """Schema for reading a message."""
    id: str
    conversation_id: str
    user_id: str
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationRead(BaseModel):
    """Schema for reading a conversation."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    message: str
    detail: Optional[str] = None
