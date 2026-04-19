"""OpenAI Agents SDK Service for AI Todo Chatbot.

This service wraps the OpenAI/Groq API to provide natural language
understanding and tool orchestration for todo management.
"""
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import json


@dataclass
class AgentResponse:
    """Response from agent execution."""
    response: str
    tool_calls: List[Dict[str, Any]]
    conversation_id: str


class AgentService:
    """Service for OpenAI/Groq API integration."""
    
    def __init__(self):
        """Initialize agent service with Groq or OpenAI API key."""
        # Check if using Groq
        self.use_groq = os.getenv("USE_GROQ") == "true"
        
        # System prompt for the AI assistant
        self.system_prompt = """You are an AI assistant helping users manage their todo list.
You have access to the following tools:
- add_task: Create a new task
- list_tasks: List user's tasks with optional filters
- update_task: Update an existing task
- complete_task: Mark a task as completed
- delete_task: Delete a task

Guidelines:
1. Always be friendly and helpful
2. Confirm actions clearly after completing them
3. If user intent is unclear, ask clarifying questions
4. Never make up task IDs - only use IDs from list_tasks results
5. When listing tasks, summarize them in a readable format
6. Handle errors gracefully and explain what went wrong

Example responses:
- "I've added 'Buy groceries' to your tasks for tomorrow."
- "You have 3 pending tasks: 1) Buy groceries (due tomorrow), 2) Call dentist, 3) Finish report"
- "I've marked 'Buy groceries' as completed. Great job!"
"""
        
        if self.use_groq:
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("GROQ_API_KEY environment variable is required")
            # Use OpenAI client with Groq endpoint
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = "llama-3.3-70b-versatile"  # Groq's latest free model (updated from 3.1)
            print(f"✅ Using Groq API with model: {self.model}")
        else:
            # Fallback to OpenAI
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4o-mini"
            print(f"✅ Using OpenAI API with model: {self.model}")
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        tools_context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process user message and return agent response with tool calls.
        
        Args:
            user_id: Authenticated user ID
            message: User's natural language message
            conversation_history: Optional list of previous messages
            tools_context: Context about available tools
            
        Returns:
            AgentResponse with response text and tool calls
        """
        # Build messages array
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 messages for context
        
        # Add user message
        messages.append({"role": "user", "content": message})
        
        # Define tools for OpenAI function calling
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title or name"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional detailed description"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Optional due date in ISO 8601 format"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Task priority level"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for the user with optional filters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Filter by completion status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Filter by priority level"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "New due date"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]
        
        # Call Groq/OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,  # Uses Groq or OpenAI model based on config
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )
        
        # Extract response
        assistant_message = response.choices[0].message
        tool_calls = []
        
        # Process tool calls if any
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_calls.append({
                    "tool": tool_call.function.name,
                    "input": json.loads(tool_call.function.arguments),
                    "output": None  # Will be filled after tool execution
                })
        
        # Generate response text
        response_text = assistant_message.content or ""
        
        # If there are tool calls, add a confirmation message
        if tool_calls and not response_text:
            tool_name = tool_calls[0]["tool"]
            response_text = self._generate_confirmation_message(tool_name, tool_calls[0]["input"])
        
        return AgentResponse(
            response=response_text,
            tool_calls=tool_calls,
            conversation_id=""  # Will be set by caller
        )
    
    def _generate_confirmation_message(
        self,
        tool_name: str,
        tool_input: Dict[str, Any]
    ) -> str:
        """Generate a friendly confirmation message based on tool call."""
        messages = {
            "add_task": f"I've added '{tool_input.get('title', 'the task')}' to your todo list.",
            "list_tasks": "Here are your tasks:",
            "update_task": f"I've updated the task.",
            "complete_task": "Great job! I've marked the task as completed.",
            "delete_task": "I've deleted the task from your list."
        }
        return messages.get(tool_name, "I've completed your request.")
    
    def parse_tool_intent(self, message: str) -> Optional[str]:
        """
        Parse user message to determine intended tool.
        
        Args:
            message: User's natural language message
            
        Returns:
            Tool name or None if no clear intent
        """
        message_lower = message.lower()
        
        # Add task patterns
        if any(word in message_lower for word in ["add", "create", "new task", "remind me"]):
            return "add_task"
        
        # List tasks patterns
        if any(word in message_lower for word in ["list", "show", "my tasks", "pending", "what do i have"]):
            return "list_tasks"
        
        # Update task patterns
        if any(word in message_lower for word in ["update", "change", "edit", "modify"]):
            return "update_task"
        
        # Complete task patterns
        if any(word in message_lower for word in ["complete", "done", "finish", "mark as"]):
            return "complete_task"
        
        # Delete task patterns
        if any(word in message_lower for word in ["delete", "remove", "cancel", "drop"]):
            return "delete_task"
        
        return None


# Singleton instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """Get or create agent service singleton."""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
