# Implementation Plan: AI-Powered Todo Chatbot (Spec-4)

**Branch**: `004-ai-todo-chatbot` | **Date**: 2026-03-27 | **Spec**: [specs/004-ai-todo-chatbot/spec.md](../spec.md)
**Input**: Feature specification from `/specs/004-ai-todo-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an AI-powered chatbot that enables users to manage todos using natural language. The system integrates OpenAI ChatKit frontend with a FastAPI backend using OpenAI Agents SDK and MCP tools. All task operations occur through stateless MCP tools with strict user isolation via JWT authentication. Conversation history persists in PostgreSQL database, reconstructed fresh on each request to maintain stateless architecture.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.3+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, MCP SDK, Next.js 16+, Better Auth
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web application (browser-based)
**Project Type**: Web application with separate frontend and backend
**Performance Goals**: p95 latency <3 seconds for chat responses, support 100 concurrent users
**Constraints**: Stateless request cycle, JWT required for all chat operations, no in-memory session storage
**Scale/Scope**: Single-user todo management with multi-tenant architecture, conversation history up to 100 messages per conversation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Stateless Architecture ✅
- **Requirement**: Server must not hold in-memory state between requests
- **Compliance**: Chat endpoint reconstructs conversation from DB on each request; No session data in memory
- **Status**: PASS

### Gate 2: Tool-Driven AI ✅
- **Requirement**: All task operations must occur via MCP tools
- **Compliance**: Agent orchestrates MCP tools (add_task, list_tasks, update_task, complete_task, delete_task); No direct DB access
- **Status**: PASS

### Gate 3: User Isolation ✅
- **Requirement**: All operations strictly scoped to authenticated user_id
- **Compliance**: JWT validation before agent execution; All MCP tools validate user_id; Task ownership enforced
- **Status**: PASS

### Gate 4: Deterministic Tool Invocation ✅
- **Requirement**: Agent must call MCP tools based on defined behavior rules
- **Compliance**: Tool schemas strictly validated; Confirmation messages for all actions; Predictable intent mapping
- **Status**: PASS

### Gate 5: Persistence ✅
- **Requirement**: Conversations and messages stored in database
- **Compliance**: Conversation and Message models with foreign key integrity; All messages persisted before response
- **Status**: PASS

### Gate 6: Separation of Concerns ✅
- **Requirement**: Chat endpoint, Agent logic, MCP tools, and DB models must remain modular
- **Compliance**: Separate directories for api/, tools/, models/, services/; No circular dependencies
- **Status**: PASS

### Gate 7: Spec-Driven Development ✅
- **Requirement**: All agent behaviors and tool contracts must be explicitly defined
- **Compliance**: Tool schemas documented in contracts/; API contracts defined before implementation
- **Status**: PASS

**Overall Gate Status**: PASS - All constitution principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/004-ai-todo-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── mcp-tools.yaml   # MCP tool schemas
│   └── chat-api.yaml    # Chat endpoint OpenAPI spec
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py           # Existing User model
│   │   ├── task.py           # Existing Task model
│   │   ├── conversation.py   # NEW: Conversation model
│   │   └── message.py        # NEW: Message model
│   ├── tools/
│   │   ├── mcp_server.py     # NEW: MCP server setup
│   │   ├── add_task.py       # NEW: add_task tool
│   │   ├── list_tasks.py     # NEW: list_tasks tool
│   │   ├── update_task.py    # NEW: update_task tool
│   │   ├── complete_task.py  # NEW: complete_task tool
│   │   └── delete_task.py    # NEW: delete_task tool
│   ├── services/
│   │   ├── agent_service.py  # NEW: OpenAI Agents SDK integration
│   │   └── jwt_service.py    # NEW: JWT verification service
│   ├── api/
│   │   ├── chat_router.py    # NEW: POST /api/{user_id}/chat
│   │   └── deps.py           # Existing: Dependencies
│   ├── middleware/
│   │   └── auth_middleware.py # Existing: JWT middleware
│   └── main.py               # Updated: Include chat router
└── tests/
    ├── contract/
    │   └── test_mcp_tools.py  # NEW: MCP tool contract tests
    └── integration/
        └── test_chat_flow.py  # NEW: Chat integration tests

frontend/
├── src/
│   ├── app/
│   │   └── chat/
│   │       └── page.tsx      # NEW: Chat page using ChatKit
│   ├── components/
│   │   └── ChatInterface.tsx # NEW: ChatKit UI component
│   ├── services/
│   │   └── chatService.ts    # NEW: Chat API client
│   └── lib/
│       └── auth.ts           # NEW: JWT token management
└── tests/
    └── components/
        └── ChatInterface.test.tsx # NEW: Component tests
```

**Structure Decision**: Web application structure (Option 2) selected. Existing `backend/` and `frontend/` directories reused. New models, tools, services, and API routes added for chatbot functionality. This matches the existing Phase II architecture and extends it with Phase III AI capabilities.

## Complexity Tracking

No constitution violations. All gates passed with existing architecture patterns.
