# Quickstart: AI-Powered Todo Chatbot

**Feature**: 004-ai-todo-chatbot
**Date**: 2026-03-27
**Purpose**: Get the AI chatbot feature running quickly

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Neon Serverless PostgreSQL database
- OpenAI API key
- Better Auth configured

---

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Additional Dependencies Needed**:
Add to `requirements.txt`:
```
openai-agents
mcp
python-jose[cryptography]
```

### 2. Configure Environment Variables

Create or update `.env` file:

```bash
# Database
DATABASE_URL=postgresql+psycopg://user:password@host.neon.tech/dbname

# Authentication (must match Better Auth secret)
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-chars

# OpenAI
OPENAI_API_KEY=sk-...

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### 3. Run Database Migrations

Create Conversation and Message tables:

```bash
# Using Alembic
alembic revision --autogenerate -m "Add conversation and message tables"
alembic upgrade head

# Or manually create tables
python create_tables.py
```

### 4. Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server should start at: `http://localhost:8000`

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

**Additional Dependencies Needed**:
```bash
npm install @openai/chatkit
```

### 2. Configure Environment Variables

Create or update `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

### 3. Start Frontend Development Server

```bash
npm run dev
```

Frontend should start at: `http://localhost:3000`

---

## Testing the Chat Feature

### 1. Authenticate

First, log in to get a JWT token:

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Save the JWT token from the response.

### 2. Send a Chat Message

```bash
curl -X POST http://localhost:8000/api/YOUR_USER_ID/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add task buy groceries tomorrow"
  }'
```

Expected response:
```json
{
  "conversation_id": "uuid-here",
  "response": "I've added 'buy groceries' to your tasks for tomorrow.",
  "tool_calls": [
    {
      "tool": "add_task",
      "input": { "title": "buy groceries", ... },
      "output": { "success": true, ... }
    }
  ]
}
```

### 3. Continue the Conversation

Use the returned `conversation_id` for continuity:

```bash
curl -X POST http://localhost:8000/api/YOUR_USER_ID/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-Conversation-ID: CONVERSATION_ID_FROM_PREVIOUS" \
  -d '{
    "message": "Show me all my tasks"
  }'
```

---

## Common Commands

### View All Tasks via Chat

```
Message: "List all my tasks"
```

### Create Task with Priority

```
Message: "Add high priority task finish report by Friday"
```

### Complete a Task

```
Message: "Mark buy groceries as done"
```

### Update Task

```
Message: "Change the dentist appointment to next week"
```

### Delete Task

```
Message: "Remove the grocery shopping task"
```

---

## Troubleshooting

### 401 Unauthorized

**Problem**: JWT token invalid or expired

**Solution**:
- Verify token is included in Authorization header
- Check token format: `Bearer <token>`
- Re-login to get fresh token
- Ensure BETTER_AUTH_SECRET matches on both frontend and backend

### 403 Forbidden

**Problem**: User ID mismatch

**Solution**:
- Verify user_id in URL matches user_id in JWT token
- Don't use another user's ID

### Database Connection Error

**Problem**: Cannot connect to PostgreSQL

**Solution**:
- Check DATABASE_URL format
- Verify network access to Neon database
- Ensure SSL is enabled if required

### MCP Tool Not Found

**Problem**: Agent cannot find registered tools

**Solution**:
- Verify MCP server initialization in main.py
- Check tool registration code
- Ensure all tool files exist in `backend/src/tools/`

---

## Architecture Overview

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Frontend   │ ───► │   Backend    │ ───► │  Database   │
│  ChatKit    │      │   FastAPI    │      │  PostgreSQL │
│             │ ◄─── │              │ ◄─── │             │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  MCP Tools   │
                     │  add_task    │
                     │  list_tasks  │
                     │  update_task │
                     │  complete    │
                     │  delete      │
                     └──────────────┘
```

---

## Next Steps

1. **Customize Agent Behavior**: Edit system prompt in `agent_service.py`
2. **Add More Tools**: Create new MCP tools in `backend/src/tools/`
3. **Enhance UI**: Customize ChatKit components in `frontend/src/components/`
4. **Add Analytics**: Track tool usage and conversation metrics
5. **Deploy**: Follow deployment guide for production setup

---

## Additional Resources

- [MCP Tools Specification](contracts/mcp-tools.md)
- [Chat API Specification](contracts/chat-api.yaml)
- [Data Model](data-model.md)
- [Implementation Plan](plan.md)
