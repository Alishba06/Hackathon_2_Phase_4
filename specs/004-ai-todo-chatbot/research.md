# Research: AI-Powered Todo Chatbot (Spec-4)

**Feature**: 004-ai-todo-chatbot
**Date**: 2026-03-27
**Purpose**: Resolve all technical unknowns and document design decisions for Phase III implementation

---

## Technology Decisions

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK for agent orchestration with MCP tool integration

**Rationale**:
- Official OpenAI framework for building agent-based applications
- Native support for tool calling and function execution
- Integrates seamlessly with MCP protocol for stateless tool invocation
- Provides built-in intent recognition and natural language understanding

**Alternatives Considered**:
- **LangChain**: More complex, heavier dependency, overkill for simple todo operations
- **Custom NLP pipeline**: Would require significant development effort, less reliable than pre-trained models
- **Direct OpenAI API calls**: Lacks agent orchestration patterns, would need custom tool routing logic

**Implementation Notes**:
- Agent configured with system prompt for todo management domain
- Tools registered with MCP SDK and exposed to agent
- Agent responses include tool_calls array for frontend consumption

---

### 2. MCP SDK for Tool Definitions

**Decision**: Use official MCP SDK to define and expose stateless tools

**Rationale**:
- Standardized protocol for tool definitions and invocation
- Enforces stateless design pattern by construction
- Provides automatic input/output schema validation
- Enables tool discovery and introspection
- Aligns with constitution principle: Tool-Driven AI

**Alternatives Considered**:
- **Custom tool framework**: Would lack standardization, require more validation code
- **FastAPI dependency injection**: Tightly couples tools to HTTP layer, violates separation of concerns
- **Direct function calls**: No schema validation, harder to test and document

**Implementation Notes**:
- Each tool (add_task, list_tasks, update_task, complete_task, delete_task) defined as separate MCP tool
- Tools accept user_id as mandatory parameter for user isolation
- All tools persist changes via SQLModel, no in-memory state
- Tool responses include structured data for agent consumption

---

### 3. JWT Verification with Better Auth

**Decision**: Use Better Auth for JWT token issuance and verification with shared secret

**Rationale**:
- Already integrated in Phase II for authentication
- Issues JWT tokens that can be verified by backend without session lookup
- Shared secret (BETTER_AUTH_SECRET) enables stateless verification
- Aligns with existing frontend authentication flow

**Alternatives Considered**:
- **Auth0**: External dependency, adds latency, overkill for hackathon project
- **Custom JWT implementation**: Reinventing wheel, security risks
- **Session-based auth**: Violates stateless architecture principle

**Implementation Notes**:
- Frontend includes JWT in Authorization: Bearer header
- Backend verifies token signature using BETTER_AUTH_SECRET
- Token decoded to extract user_id and email
- User_id validated against URL parameter before agent execution

---

### 4. Conversation and Message Models

**Decision**: Create new Conversation and Message SQLModel models with foreign key relationships

**Rationale**:
- Persistent conversation history required by constitution
- Foreign key integrity ensures data consistency
- Separation from Task model maintains modularity
- Enables conversation reconstruction on each request

**Alternatives Considered**:
- **JSON storage in single table**: Harder to query, no referential integrity
- **In-memory conversation cache**: Violates stateless architecture principle
- **External vector database**: Unnecessary complexity for simple chat history

**Implementation Notes**:
- Conversation model: id, user_id, created_at, updated_at
- Message model: id, conversation_id, user_id, role (user/assistant), content, created_at
- All messages linked to conversation via foreign key
- Indexes on user_id and conversation_id for performance

---

### 5. Chat Endpoint Design (POST /api/{user_id}/chat)

**Decision**: RESTful endpoint accepting conversation_id and message, returning response + tool_calls

**Rationale**:
- Follows existing API pattern from Phase II task router
- URL parameter user_id provides clear ownership scope
- Optional conversation_id enables conversation continuity
- Response includes both assistant message and tool execution details

**Alternatives Considered**:
- **WebSocket streaming**: Adds complexity, not required for non-streaming responses
- **GraphQL**: Overkill for simple chat interaction, adds learning curve
- **Separate conversations and messages endpoints**: More round trips, less efficient

**Implementation Notes**:
- Request body: { conversation_id?: string, message: string }
- Response: { conversation_id: string, response: string, tool_calls: ToolCall[] }
- JWT middleware validates authentication before handler execution
- Conversation history fetched from DB and passed to agent context

---

### 6. OpenAI ChatKit for Frontend

**Decision**: Use OpenAI ChatKit UI components for chat interface

**Rationale**:
- Official OpenAI library for chat interfaces
- Pre-built components reduce development time
- Integrates naturally with OpenAI Agents SDK backend
- Provides accessible, responsive UI out of the box

**Alternatives Considered**:
- **Custom React components**: More development time, reinventing wheel
- **Other chat UI libraries**: May not integrate as smoothly with OpenAI ecosystem
- **Plain HTML/CSS**: More work, less polished UX

**Implementation Notes**:
- ChatKit component configured with custom API endpoint
- JWT token attached to requests via Authorization header
- conversation_id managed in frontend state for continuity
- Messages rendered with user/assistant differentiation

---

## Best Practices

### MCP Tool Design

1. **Stateless Operations**: Tools must not store state between invocations
2. **User Validation**: Every tool must validate user_id before database operations
3. **Structured Responses**: Return consistent, typed responses for agent consumption
4. **Error Handling**: Graceful error messages that agent can communicate to users
5. **Input Validation**: Strict schema validation using Pydantic models

### JWT Security

1. **Token Verification**: Verify signature on every request using shared secret
2. **User ID Matching**: Validate token user_id matches URL parameter
3. **Expiration Checking**: Reject expired tokens with 401 response
4. **No Token Logging**: Never log full JWT tokens in application logs
5. **HTTPS Only**: Tokens only transmitted over secure connections in production

### Database Design

1. **Foreign Key Constraints**: All relationships enforced at database level
2. **Indexes**: Add indexes on user_id and conversation_id for query performance
3. **Soft Deletes**: Consider soft deletes for conversations (optional enhancement)
4. **Timestamps**: All models include created_at and updated_at fields
5. **UUID Primary Keys**: Use UUIDs instead of integers for security

---

## Integration Patterns

### Agent → Tool Invocation Flow

```
1. User sends message → Chat endpoint
2. Fetch conversation history from DB
3. Build agent context with history + user_id
4. Agent processes message, identifies intent
5. Agent selects appropriate MCP tool(s)
6. Tool executes with validated parameters
7. Tool persists changes to DB
8. Agent generates confirmation response
9. Store user + assistant messages in DB
10. Return response + tool_calls to frontend
```

### Conversation Continuity Pattern

```
1. Frontend stores conversation_id in state
2. On new message, include conversation_id in request
3. Backend fetches full conversation from DB
4. Agent receives conversation history as context
5. New messages appended to same conversation
6. Frontend re-renders with updated history
```

### User Isolation Pattern

```
1. JWT token extracted from Authorization header
2. Token verified using BETTER_AUTH_SECRET
3. user_id decoded from token payload
4. user_id validated against URL parameter
5. All MCP tools receive user_id as parameter
6. Database queries filtered by user_id WHERE clause
7. Task ownership validated before modifications
```

---

## Resolved Clarifications

All technical unknowns from initial spec have been resolved:

| Unknown | Resolution |
|---------|------------|
| AI Framework | OpenAI Agents SDK |
| Tool Protocol | MCP SDK |
| Authentication | Better Auth with JWT |
| Conversation Storage | PostgreSQL with Conversation and Message models |
| Frontend Chat UI | OpenAI ChatKit |
| API Pattern | RESTful POST /api/{user_id}/chat |
| State Management | Database-only, no in-memory state |

---

## Next Steps

Proceed to Phase 1: Design & Contracts
- Create data-model.md with Conversation and Message entity definitions
- Generate MCP tool schemas in contracts/mcp-tools.yaml
- Generate chat API spec in contracts/chat-api.yaml
- Create quickstart.md with setup and usage instructions
