"""Chat Router for AI Todo Chatbot.

This module implements the POST /api/{user_id}/chat endpoint that:
1. Validates JWT token
2. Fetches conversation history from DB
3. Runs agent with MCP tools
4. Stores messages in DB
5. Returns response with tool calls
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select
import uuid
from datetime import datetime

from src.config.database import engine
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message
from src.api.schemas import ChatRequest, ChatResponse, ToolCallInput
from src.services.jwt_service import get_jwt_service, JWTService
from src.services.agent_service import get_agent_service, AgentService
from src.tools.mcp_server import (
    add_task,
    list_tasks,
    update_task,
    complete_task,
    delete_task
)

router = APIRouter()


async def execute_mcp_tool(tool_name: str, user_id: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute an MCP tool with the given input.
    
    Args:
        tool_name: Name of the tool to execute
        user_id: Authenticated user ID
        tool_input: Tool input parameters
        
    Returns:
        Tool execution result
    """
    # Add user_id to tool input if not present
    if "user_id" not in tool_input:
        tool_input["user_id"] = user_id
    
    # Execute appropriate tool
    if tool_name == "add_task":
        return await add_task(**tool_input)
    elif tool_name == "list_tasks":
        return await list_tasks(**tool_input)
    elif tool_name == "update_task":
        return await update_task(**tool_input)
    elif tool_name == "complete_task":
        return await complete_task(**tool_input)
    elif tool_name == "delete_task":
        return await delete_task(**tool_input)
    else:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    summary="Chat with AI todo assistant",
    description="Send a natural language message to the AI agent for todo management"
)
async def chat(
    user_id: str,
    request: ChatRequest,
    x_conversation_id: Optional[str] = Header(None, alias="X-Conversation-ID"),
    authorization: Optional[str] = Header(None),
    jwt_service: JWTService = Depends(get_jwt_service),
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Chat with AI todo assistant.
    
    - **user_id**: User ID from URL path
    - **message**: User's natural language message
    - **conversation_id**: Optional conversation ID for continuity
    - **authorization**: JWT token in Authorization header
    """
    # Step 1: Verify JWT token
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = jwt_service.extract_token_from_header(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    verification_result = jwt_service.verify_token(token)
    if not verification_result.valid:
        raise HTTPException(status_code=401, detail=verification_result.error)
    
    # Step 2: Validate user_id matches token
    if verification_result.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match URL parameter"
        )
    
    # Step 3: Verify user exists
    with Session(engine) as db_session:
        user = db_session.get(User, uuid.UUID(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
    # Step 4: Get or create conversation
    conversation_id = request.conversation_id or x_conversation_id
    with Session(engine) as db_session:
        if conversation_id:
            # Try to load existing conversation
            conversation = db_session.get(Conversation, uuid.UUID(conversation_id))
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            # Verify ownership
            if str(conversation.user_id) != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            db_session.add(conversation)
            db_session.commit()
            db_session.refresh(conversation)
            conversation_id = str(conversation.id)
    
    # Step 5: Fetch conversation history
    conversation_history: List[Dict[str, str]] = []
    with Session(engine) as db_session:
        query = (
            select(Message)
            .where(Message.conversation_id == uuid.UUID(conversation_id))
            .order_by(Message.created_at.asc())
        )
        messages = db_session.exec(query).all()
        
        for msg in messages:
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })
    
    # Step 6: Run agent to get response and tool calls
    agent_response = await agent_service.process_message(
        user_id=user_id,
        message=request.message,
        conversation_history=conversation_history
    )
    
    # Step 7: Execute MCP tools if any
    tool_calls_output: List[ToolCallInput] = []
    for tool_call in agent_response.tool_calls:
        # Execute the tool
        tool_result = await execute_mcp_tool(
            tool_name=tool_call["tool"],
            user_id=user_id,
            tool_input=tool_call["input"]
        )
        
        # Store tool call with output
        tool_calls_output.append(ToolCallInput(
            tool=tool_call["tool"],
            input=tool_call["input"],
            output=tool_result
        ))
        
        # Update response text based on tool result
        if tool_result.get("success"):
            # Use tool's message if available
            if "message" in tool_result:
                agent_response.response = tool_result["message"]
        else:
            # Handle error
            agent_response.response = f"Sorry, I encountered an error: {tool_result.get('error', 'Unknown error')}"
    
    # Step 8: Store messages in database
    with Session(engine) as db_session:
        # Store user message
        user_message = Message(
            conversation_id=uuid.UUID(conversation_id),
            user_id=user_id,
            role="user",
            content=request.message
        )
        db_session.add(user_message)
        
        # Store assistant response
        assistant_message = Message(
            conversation_id=uuid.UUID(conversation_id),
            user_id=user_id,
            role="assistant",
            content=agent_response.response
        )
        db_session.add(assistant_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        db_session.add(conversation)
        
        db_session.commit()
    
    # Step 9: Return response
    return ChatResponse(
        conversation_id=conversation_id,
        response=agent_response.response,
        tool_calls=tool_calls_output
    )
