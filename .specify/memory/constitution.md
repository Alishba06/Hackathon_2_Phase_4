<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0 (MAJOR)
Modified principles: 
  - Functionality First → Stateless Architecture (redefined for Phase III)
  - Security by Default → User Isolation (enhanced with strict scoping)
  - Test-First → Deterministic Tool Invocation (specialized for MCP)
  - Responsive Design → Persistence (database-focused)
  - Spec-Driven Development → Separation of Concerns (modular architecture)
  - Reliability and Error Handling → Tool-Driven AI (MCP-specific)
Added sections:
  - MCP Server standards
  - OpenAI Agents SDK integration
  - Conversation and Message models
  - JWT verification workflow
  - Tool input/output schema validation
Removed sections:
  - Frontend-specific responsive design requirements (moved to frontend spec)
  - Generic test-first requirements (specialized for tool-driven approach)
Templates requiring updates:
  - plan-template.md: ✅ Constitution Check section aligns with new principles
  - spec-template.md: ✅ Requirements format compatible with new principles
  - tasks-template.md: ✅ Task organization supports tool-driven development
Follow-up TODOs: None
-->
# AI-Powered Todo Chatbot (Phase III) Constitution

**Project Code**: SPEC-4 | **Type**: Stateless AI Chatbot with MCP Tools

## Core Principles

### Stateless Architecture
Server must not hold in-memory state between requests; Every request must be self-contained with all context retrieved from database; No session data stored in application memory; All conversational state persisted to database before response completion; Request context reconstructed fresh on each API call

**Rationale**: Enables horizontal scaling, eliminates race conditions, ensures reliability across server restarts

### Tool-Driven AI
All task operations must occur via MCP tools; Agent must not perform direct database manipulation; No task logic implemented inside agent code; Agent acts solely as orchestrator calling stateless MCP tools; All CRUD operations on tasks executed through defined tool interfaces

**Rationale**: Enforces separation of concerns, enables tool testing, maintains clear boundaries between AI logic and data operations

### User Isolation
All operations strictly scoped to authenticated user_id; Agent must only access tasks belonging to authenticated user; MCP tools must validate user_id before any database operation; No tool may expose another user's data; JWT authentication required for all chat endpoint requests

**Rationale**: Multi-tenant security, data privacy, prevents unauthorized access across user boundaries

### Deterministic Tool Invocation
Agent must call MCP tools based on defined behavior rules; Tool selection must be predictable and testable; Agent responses must follow consistent patterns for identical inputs; Tool input/output schemas must be strictly validated; Every assistant action must include confirmation message

**Rationale**: Ensures reliability, enables testing, provides predictable user experience

### Persistence
Conversations and messages stored in database; Conversation history reconstructed from database on each request; No conversation state stored in memory; All tool outputs persisted before agent response; Database serves as single source of truth for all state

**Rationale**: Enables conversation continuity, supports server restarts, provides audit trail

### Separation of Concerns
Chat endpoint, Agent logic, MCP tools, and DB models must remain modular; Each component has single responsibility; No circular dependencies between modules; Clear interfaces between layers; API endpoints do not contain business logic

**Rationale**: Maintainability, testability, enables independent component evolution

### Spec-Driven Development
All agent behaviors and tool contracts must be explicitly defined; Implementation must match specifications precisely; All development follows Qwen Code + Spec-Kit Plus methodology; Tool schemas documented before implementation; API contracts defined in specification phase

**Rationale**: Ensures correctness, enables validation, reduces ambiguity

## Technology Stack and Constraints

**Backend**: Python FastAPI with REST format
**AI Framework**: OpenAI Agents SDK
**MCP Server**: Official MCP SDK for tool definitions
**ORM**: SQLModel with foreign key integrity enforcement
**Database**: Neon Serverless PostgreSQL
**Frontend**: OpenAI ChatKit
**Authentication**: Better Auth with JWT tokens
**Shared Secret**: Environment variable BETTER_AUTH_SECRET required

**API Standards**:
- Chat endpoint: POST /api/{user_id}/chat
- All endpoints return proper HTTP status codes
- JWT tokens verified using BETTER_AUTH_SECRET
- Unauthorized requests rejected with 401

**Database Models**:
- Task model (reused from Phase II)
- Conversation model: user_id, id, created_at, updated_at
- Message model: user_id, id, conversation_id, role, content, created_at
- All models enforce foreign key integrity

**Security Requirements**:
- Chat endpoint rejects unauthorized requests (401)
- Agent operates only on tasks belonging to authenticated user
- MCP tools validate user_id before database operation
- No tool exposes another user's data
- JWT verification required before agent execution

## Development Workflow

All setup steps documented with database migrations and environment variables; Frontend API client attaches JWT tokens in Authorization: Bearer header; Backend validates JWT token for every request using shared secret; Code follows project-specific style guides; Clear separation between chat endpoint, agent logic, MCP tools, and database models

**Request Flow**:
1. User logs in → Better Auth issues JWT token
2. Frontend includes JWT in Authorization header
3. Backend extracts and verifies token signature
4. Backend decodes token to get user ID and email
5. Backend validates user_id matches URL parameter
6. Agent executes with authenticated context
7. All operations scoped to verified user_id

## Governance

All PRs and reviews must verify compliance with stateless architecture requirements; All API endpoints must validate JWT tokens before processing; All MCP tools must enforce user_id validation; Spec-Driven Development methodology enforced via Qwen Code + Spec-Kit Plus; All components must pass automated spec-driven checks

**Versioning Policy**:
- MAJOR: Backward incompatible changes to tool schemas or API contracts
- MINOR: New tools added or existing tools enhanced
- PATCH: Bug fixes, clarifications, non-breaking improvements

**Amendment Procedure**:
Constitution changes require documentation of rationale, impact analysis on existing tools, and migration strategy if breaking changes introduced

**Compliance Review**:
Every pull request must verify: stateless design, user isolation, tool-driven operations, proper JWT validation, and database persistence

**Version**: 2.0.0 | **Ratified**: 2026-01-22 | **Last Amended**: 2026-03-27
