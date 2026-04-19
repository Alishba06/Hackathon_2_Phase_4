# MCP Tools Specification: AI-Powered Todo Chatbot

**Feature**: 004-ai-todo-chatbot
**Date**: 2026-03-27
**Purpose**: Define MCP tool schemas for AI agent tool invocation

---

## Tool Overview

All task operations are exposed via MCP (Model Context Protocol) tools. The AI agent calls these tools based on user intent detected from natural language input.

**Tools**:
1. `add_task` - Create a new todo task
2. `list_tasks` - List tasks with optional filters
3. `update_task` - Update task details
4. `complete_task` - Mark a task as completed
5. `delete_task` - Remove a task

---

## Common Parameters

All tools accept the following common parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | Authenticated user ID for isolation |

---

## Tool Definitions

### add_task

Creates a new todo task for the authenticated user.

**Description**: Add a new task to the user's todo list with optional description, due date, and priority.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user ID"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "Task title or name"
    },
    "description": {
      "type": "string",
      "maxLength": 10000,
      "description": "Optional detailed description"
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "Optional due date in ISO 8601 format"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "default": "medium",
      "description": "Task priority level"
    }
  },
  "required": ["user_id", "title"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "title": { "type": "string" },
        "description": { "type": "string" },
        "is_completed": { "type": "boolean" },
        "due_date": { "type": "string", "format": "date-time" },
        "priority": { "type": "string" },
        "created_at": { "type": "string", "format": "date-time" }
      }
    },
    "message": { "type": "string" }
  }
}
```

**Example Usage**:
```
User: "Add task buy groceries tomorrow"
Agent calls: add_task(user_id="...", title="buy groceries", due_date="2026-03-28T00:00:00Z")
Response: { success: true, task: {...}, message: "Task created successfully" }
```

**Error Handling**:
- 400: Invalid input (missing title, invalid date format)
- 401: Invalid or missing user_id
- 500: Database error

---

### list_tasks

Retrieves tasks for the authenticated user with optional filtering.

**Description**: List all tasks belonging to the user, optionally filtered by completion status or priority.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user ID"
    },
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "default": "all",
      "description": "Filter by completion status"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Filter by priority level"
    }
  },
  "required": ["user_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "format": "uuid" },
          "title": { "type": "string" },
          "description": { "type": "string" },
          "is_completed": { "type": "boolean" },
          "due_date": { "type": "string", "format": "date-time" },
          "priority": { "type": "string" },
          "created_at": { "type": "string", "format": "date-time" }
        }
      }
    },
    "count": { "type": "integer" }
  }
}
```

**Example Usage**:
```
User: "Show me my pending tasks"
Agent calls: list_tasks(user_id="...", status="pending")
Response: { success: true, tasks: [...], count: 5 }
```

**Error Handling**:
- 400: Invalid status or priority filter
- 401: Invalid or missing user_id
- 500: Database error

---

### update_task

Updates an existing task's details.

**Description**: Modify the title, description, due date, or priority of an existing task.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user ID"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to update"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "New title (optional)"
    },
    "description": {
      "type": "string",
      "maxLength": 10000,
      "description": "New description (optional)"
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "New due date (optional)"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "New priority level (optional)"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "title": { "type": "string" },
        "description": { "type": "string" },
        "is_completed": { "type": "boolean" },
        "due_date": { "type": "string", "format": "date-time" },
        "priority": { "type": "string" },
        "updated_at": { "type": "string", "format": "date-time" }
      }
    },
    "message": { "type": "string" }
  }
}
```

**Example Usage**:
```
User: "Change the grocery shopping task to high priority"
Agent calls: update_task(user_id="...", task_id="...", priority="high")
Response: { success: true, task: {...}, message: "Task updated successfully" }
```

**Error Handling**:
- 400: Invalid input data
- 401: Invalid or missing user_id
- 404: Task not found or doesn't belong to user
- 500: Database error

---

### complete_task

Marks a task as completed.

**Description**: Change the completion status of a task to true.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user ID"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to complete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "title": { "type": "string" },
        "is_completed": { "type": "boolean", "const": true },
        "completed_at": { "type": "string", "format": "date-time" }
      }
    },
    "message": { "type": "string" }
  }
}
```

**Example Usage**:
```
User: "Mark buy groceries as done"
Agent calls: complete_task(user_id="...", task_id="...")
Response: { success: true, task: {...}, message: "Task completed successfully" }
```

**Error Handling**:
- 401: Invalid or missing user_id
- 404: Task not found or doesn't belong to user
- 409: Task already completed
- 500: Database error

---

### delete_task

Permanently removes a task.

**Description**: Delete a task from the user's todo list.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user ID"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to delete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "deleted_task_id": { "type": "string", "format": "uuid" },
    "message": { "type": "string" }
  }
}
```

**Example Usage**:
```
User: "Delete the dentist appointment task"
Agent calls: delete_task(user_id="...", task_id="...")
Response: { success: true, deleted_task_id: "...", message: "Task deleted successfully" }
```

**Error Handling**:
- 401: Invalid or missing user_id
- 404: Task not found or doesn't belong to user
- 500: Database error

---

## Tool Invocation Rules

1. **User Validation**: Every tool MUST validate user_id before any database operation
2. **Task Ownership**: Tools MUST verify that the task belongs to the authenticated user
3. **Input Validation**: All inputs MUST be validated against schema before execution
4. **Stateless Execution**: Tools MUST NOT store any state between invocations
5. **Error Messages**: Errors MUST be user-friendly and actionable
6. **Confirmation**: Each successful operation MUST return a confirmation message

---

## Intent Mapping

The AI agent maps natural language to tools as follows:

| User Intent | Example Phrases | Tool |
|-------------|-----------------|------|
| Create task | "Add task...", "Create...", "Remind me to..." | `add_task` |
| List tasks | "Show my tasks", "What do I have...", "List..." | `list_tasks` |
| Update task | "Change...", "Update...", "Edit..." | `update_task` |
| Complete task | "Mark as done", "Complete...", "Finish..." | `complete_task` |
| Delete task | "Delete...", "Remove...", "Cancel..." | `delete_task` |

---

## Testing Requirements

Each tool MUST have:
1. **Contract Test**: Validates input/output schema compliance
2. **User Isolation Test**: Verifies user cannot access another user's tasks
3. **Error Handling Test**: Confirms graceful error responses
4. **Integration Test**: End-to-end test with database persistence
