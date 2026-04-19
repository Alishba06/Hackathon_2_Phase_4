"""MCP Server initialization for AI Todo Chatbot.

This module sets up the MCP (Model Context Protocol) server that exposes
tools to the OpenAI Agents SDK for todo management operations.
"""
import os
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select
from src.config.database import engine
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
import uuid


# Initialize MCP server
mcp_server = FastMCP("AI Todo Chatbot Tools")


# ============================================================================
# MCP Tool: add_task
# ============================================================================

@mcp_server.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: str = "medium"
) -> Dict[str, Any]:
    """
    Add a new task to the user's todo list.
    
    Args:
        user_id: Authenticated user ID (UUID)
        title: Task title (required)
        description: Optional task description
        due_date: Optional due date in ISO 8601 format
        priority: Task priority (low, medium, high)
        
    Returns:
        Created task details or error message
    """
    try:
        # Validate user exists
        with Session(engine) as session:
            user = session.get(User, uuid.UUID(user_id))
            if not user:
                return {
                    "success": False,
                    "error": "User not found"
                }
            
            # Create task
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority
            )
            
            if due_date:
                from datetime import datetime
                task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "success": True,
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat()
                },
                "message": f"Task '{title}' created successfully"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# MCP Tool: list_tasks
# ============================================================================

@mcp_server.tool()
async def list_tasks(
    user_id: str,
    status: str = "all",
    priority: Optional[str] = None
) -> Dict[str, Any]:
    """
    List tasks for the authenticated user.
    
    Args:
        user_id: Authenticated user ID (UUID)
        status: Filter by status (all, pending, completed)
        priority: Filter by priority (low, medium, high)
        
    Returns:
        List of tasks matching criteria
    """
    try:
        with Session(engine) as session:
            # Build query
            query = select(Task).where(Task.user_id == user_id)
            
            # Apply status filter
            if status == "pending":
                query = query.where(Task.is_completed == False)
            elif status == "completed":
                query = query.where(Task.is_completed == True)
            
            # Apply priority filter
            if priority:
                query = query.where(Task.priority == priority)
            
            # Order by created_at descending
            query = query.order_by(Task.created_at.desc())
            
            tasks = session.exec(query).all()
            
            return {
                "success": True,
                "tasks": [
                    {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "priority": task.priority,
                        "created_at": task.created_at.isoformat()
                    }
                    for task in tasks
                ],
                "count": len(tasks)
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# MCP Tool: update_task
# ============================================================================

@mcp_server.tool()
async def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing task.
    
    Args:
        user_id: Authenticated user ID (UUID)
        task_id: Task ID to update (UUID)
        title: New title (optional)
        description: New description (optional)
        due_date: New due date (optional)
        priority: New priority (optional)
        
    Returns:
        Updated task details or error message
    """
    try:
        with Session(engine) as session:
            # Get task
            task = session.get(Task, uuid.UUID(task_id))
            
            if not task:
                return {
                    "success": False,
                    "error": "Task not found"
                }
            
            # Verify ownership
            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Task not found"
                }
            
            # Update fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if due_date is not None:
                from datetime import datetime
                task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            if priority is not None:
                task.priority = priority
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "success": True,
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "priority": task.priority,
                    "updated_at": task.updated_at.isoformat()
                },
                "message": f"Task '{task.title}' updated successfully"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# MCP Tool: complete_task
# ============================================================================

@mcp_server.tool()
async def complete_task(
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Mark a task as completed.
    
    Args:
        user_id: Authenticated user ID (UUID)
        task_id: Task ID to complete (UUID)
        
    Returns:
        Updated task details or error message
    """
    try:
        with Session(engine) as session:
            # Get task
            task = session.get(Task, uuid.UUID(task_id))
            
            if not task:
                return {
                    "success": False,
                    "error": "Task not found"
                }
            
            # Verify ownership
            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Task not found"
                }
            
            # Mark as completed
            task.is_completed = True
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "success": True,
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "is_completed": True
                },
                "message": f"Task '{task.title}' marked as completed"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# MCP Tool: delete_task
# ============================================================================

@mcp_server.tool()
async def delete_task(
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Delete a task.
    
    Args:
        user_id: Authenticated user ID (UUID)
        task_id: Task ID to delete (UUID)
        
    Returns:
        Success confirmation or error message
    """
    try:
        with Session(engine) as session:
            # Get task
            task = session.get(Task, uuid.UUID(task_id))
            
            if not task:
                return {
                    "success": False,
                    "error": "Task not found"
                }
            
            # Verify ownership
            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Task not found"
                }
            
            # Delete task
            session.delete(task)
            session.commit()
            
            return {
                "success": True,
                "deleted_task_id": task_id,
                "message": f"Task '{task.title}' deleted successfully"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# Tool Registration Helper
# ============================================================================

def get_mcp_tools() -> List[str]:
    """Get list of registered MCP tool names."""
    return [
        "add_task",
        "list_tasks",
        "update_task",
        "complete_task",
        "delete_task"
    ]
