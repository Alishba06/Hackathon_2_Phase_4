---
id: 004
title: ai-todo-chatbot-architecture-plan
stage: plan
date: 2026-03-27
surface: agent
model: qwen-code
feature: 001-ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: City Computer
command: /sp.plan
labels: ["plan", "architecture", "ai-chatbot", "mcp", "design"]
links:
  spec: specs/001-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-ai-todo-chatbot/plan.md
  - specs/001-ai-todo-chatbot/research.md
  - specs/001-ai-todo-chatbot/data-model.md
  - specs/001-ai-todo-chatbot/quickstart.md
  - specs/001-ai-todo-chatbot/contracts/mcp-tools.md
  - specs/001-ai-todo-chatbot/contracts/chat-api.yaml
tests:
  - Constitution Check: All 7 gates passed (Stateless, Tool-Driven, User Isolation, etc.)
  - Validation: All NEEDS CLARIFICATION markers resolved in research.md
  - Validation: API contracts defined for chat endpoint and MCP tools
---

## Prompt

/sp.plan

Phase 1: Setup & Alignment
- Review Spec-4 constitution and specify
- Setup FastAPI, OpenAI Agents SDK, MCP SDK
- Configure database models (Task, Conversation, Message)

Phase 2: MCP Server (Tools)
- Implement tools:
  - add_task
  - list_tasks
  - update_task
  - complete_task
  - delete_task
- Ensure all tools are stateless and DB-driven

Phase 3: AI Agent
- Configure agent using OpenAI Agents SDK
- Connect agent with MCP tools
- Implement intent → tool mapping + confirmation responses

Phase 4: Chat Endpoint
- Build POST /api/{user_id}/chat
- Verify JWT token
- Fetch conversation history from DB
- Run agent with tools
- Store user + assistant messages
- Return response + tool_calls

Phase 5: Frontend Integration
- Connect ChatKit UI to chat endpoint
- Send message + JWT + conversation_id
- Render responses and maintain chat state

Phase 6: Testing & Validation
- Test all natural language commands
- Verify tool execution and user isolation
- Ensure stateless behavior
- Run Spec-Kit Plus validation

## Response snapshot

Completed Phase 0 and Phase 1 planning artifacts:

**Phase 0 - Research**: Created research.md documenting all technology decisions:
- OpenAI Agents SDK for agent orchestration
- MCP SDK for stateless tool definitions
- Better Auth with JWT for authentication
- Conversation and Message models for persistence
- OpenAI ChatKit for frontend UI
- RESTful POST /api/{user_id}/chat endpoint

**Phase 1 - Design**:
1. data-model.md: Defined Conversation and Message SQLModel models with foreign key relationships, validation rules, indexes, and query patterns
2. contracts/mcp-tools.md: Complete MCP tool specifications for add_task, list_tasks, update_task, complete_task, delete_task with input/output schemas
3. contracts/chat-api.yaml: OpenAPI 3.0 specification for chat endpoint with authentication, request/response schemas, error codes
4. quickstart.md: Step-by-step setup guide for backend and frontend with testing examples

**Constitution Check**: All 7 gates passed:
- Stateless Architecture ✅
- Tool-Driven AI ✅
- User Isolation ✅
- Deterministic Tool Invocation ✅
- Persistence ✅
- Separation of Concerns ✅
- Spec-Driven Development ✅

**Agent Context Updated**: Qwen.md updated with Python 3.11, TypeScript 5.3+, FastAPI, OpenAI Agents SDK, MCP SDK, Next.js 16+, Better Auth, Neon PostgreSQL.

## Outcome

- ✅ Impact: Complete architecture plan with all Phase 0 and Phase 1 artifacts ready for implementation
- 🧪 Tests: Constitution Check passed all 7 gates; No NEEDS CLARIFICATION markers remain
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/mcp-tools.md, contracts/chat-api.yaml
- 🔁 Next prompts: Run /sp.tasks to generate implementation tasks, or proceed to /sp.green for implementation
- 🧠 Reflection: Plan successfully extends Phase II architecture with Phase III AI capabilities while maintaining constitution compliance

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully on first iteration
- Graders run and results (PASS/FAIL): PASS - All constitution gates satisfied, all design artifacts complete
- Prompt variant (if applicable): N/A
- Next experiment: Proceed to task generation with /sp.tasks for implementation breakdown
