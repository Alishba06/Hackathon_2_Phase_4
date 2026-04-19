---
id: 002
title: phase-iii-constitution-update
stage: constitution
date: 2026-03-27
surface: agent
model: qwen-code
feature: ai-powered-todo-chatbot
branch: main
user: City Computer
command: /sp.constitution
labels: ["constitution", "phase-iii", "governance", "mcp", "stateless"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Validation: No unresolved placeholder tokens
  - Validation: Version format matches semantic versioning
  - Validation: Dates in ISO format YYYY-MM-DD
  - Validation: Principles are declarative and testable
---

## Prompt

/sp.constitution

Project: Spec-4 – AI-Powered Todo Chatbot (Phase III)

Core principles:
- Stateless Architecture: Server must not hold in-memory state between requests
- Tool-Driven AI: All task operations must occur via MCP tools (no direct DB manipulation by agent)
- User Isolation: All operations strictly scoped to authenticated user_id
- Deterministic Tool Invocation: Agent must call MCP tools based on defined behavior rules
- Persistence: Conversations and messages stored in database
- Separation of Concerns: Chat endpoint, Agent logic, MCP tools, and DB models must remain modular
- Spec-Driven Development: All agent behaviors and tool contracts must be explicitly defined

Key standards:
- Chat endpoint must follow REST format: POST /api/{user_id}/chat
- Conversation history must be reconstructed from database on each request
- All MCP tools must be stateless and persist changes via database
- Agent must not perform task logic internally — only via MCP tools
- Tool input/output schemas must be strictly validated
- Every assistant action must include confirmation message
- All errors must be handled gracefully and stored in logs
- JWT authentication required for chat endpoint

Database standards:
- Task model reused from Phase-2
- Conversation model: user_id, id, created_at, updated_at
- Message model: user_id, id, conversation_id, role, content, created_at
- All models must enforce foreign key integrity
- No conversation state stored in memory

Constraints:
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Frontend: OpenAI ChatKit
- Authentication: Better Auth with JWT
- Shared secret via environment variable BETTER_AUTH_SECRET
- Stateless request cycle required

Security constraints:
- Chat endpoint must reject unauthorized requests (401)
- Agent must only operate on tasks belonging to authenticated user
- MCP tools must validate user_id before DB operation
- No tool may expose another user's data
- JWT verification required before any agent execution

Success criteria:
- Chatbot manages todos entirely via natural language
- Agent correctly selects MCP tools based on user intent
- Conversations persist across server restarts
- Server remains stateless between requests
- Tool calls are returned in API response
- Errors handled without crashing system
- Architecture passes Spec-Kit Plus validation

Non-goals:
- Long-term memory beyond database storage
- Multi-agent orchestration
- Real-time streaming responses (optional enhancement)
- Voice input/output
- External third-party integrations

## Response snapshot

Updated constitution from version 1.0.0 to 2.0.0 (MAJOR bump) with 7 core principles for Phase III:
Stateless Architecture, Tool-Driven AI, User Isolation, Deterministic Tool Invocation, Persistence, Separation of Concerns, and Spec-Driven Development. Included technology stack (FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL, Better Auth), API standards, database models, security requirements, development workflow with JWT request flow, and governance policies with versioning and amendment procedures.

## Outcome

- ✅ Impact: Constitution updated to Phase III with MAJOR version bump (1.0.0 → 2.0.0), redefined 6 principles, added 1 new principle
- 🧪 Tests: All validation checks passed - no placeholder tokens, semantic versioning correct, ISO dates, declarative principles
- 📁 Files: .specify/memory/constitution.md overwritten with complete Phase III constitution
- 🔁 Next prompts: Build specification with /sp.specify, Create architecture plan with /sp.plan
- 🧠 Reflection: Constitution successfully transformed from Phase II (web app focus) to Phase III (AI chatbot with MCP tools)

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully
- Graders run and results (PASS/FAIL): PASS - All validation criteria met
- Prompt variant (if applicable): N/A
- Next experiment: Proceed to feature specification phase
