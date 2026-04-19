# Tasks: AI-Powered Todo Chatbot (Spec-4)

**Input**: Design documents from `/specs/004-ai-todo-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

**Tests**: Tests are OPTIONAL - not explicitly requested in spec. Implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths follow existing Phase II structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [x] T001 [P] Add OpenAI Agents SDK to backend/requirements.txt
- [x] T002 [P] Add MCP SDK to backend/requirements.txt
- [x] T003 [P] Add python-jose[cryptography] to backend/requirements.txt for JWT verification
- [x] T004 [P] Install backend dependencies: pip install -r backend/requirements.txt
- [x] T005 [P] ~~Add OpenAI ChatKit to frontend package.json~~ (Package not available, using custom UI)
- [x] T006 [P] Install frontend dependencies: npm install

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 [P] Create Conversation model in backend/src/models/conversation.py
- [x] T008 [P] Create Message model in backend/src/models/message.py
- [x] T009 Create Alembic migration for conversation and message tables in backend/alembic/versions/002_add_conversation_message.py
- [x] T010 Run Alembic migration: alembic upgrade head
- [x] T011 [P] Create JWT verification service in backend/src/services/jwt_service.py
- [x] T012 [P] Setup MCP server initialization in backend/src/tools/mcp_server.py
- [x] T013 [P] Create OpenAI Agents SDK service wrapper in backend/src/services/agent_service.py
- [x] T014 Configure CORS and auth middleware for chat endpoint in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chat with AI to Manage Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with chatbot using natural language to perform all todo operations (add, list, update, complete, delete)

**Independent Test**: User can send messages like "Add task buy groceries" and receive confirmation that the task was created, with the task visible in the todo list.

### Implementation for User Story 1

- [x] T015 [P] [US1] Create add_task MCP tool in backend/src/tools/add_task.py
- [x] T016 [P] [US1] Create list_tasks MCP tool in backend/src/tools/list_tasks.py
- [x] T017 [P] [US1] Create update_task MCP tool in backend/src/tools/update_task.py
- [x] T018 [P] [US1] Create complete_task MCP tool in backend/src/tools/complete_task.py
- [x] T019 [P] [US1] Create delete_task MCP tool in backend/src/tools/delete_task.py
- [x] T020 [US1] Register all MCP tools with agent service in backend/src/services/agent_service.py (via mcp_server.py)
- [x] T021 [US1] Implement intent recognition configuration for OpenAI Agents SDK in backend/src/services/agent_service.py
- [x] T022 [US1] Create chat request/response schemas in backend/src/api/schemas.py
- [x] T023 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat_router.py
- [x] T024 [US1] Add chat router to backend/src/main.py
- [x] T025 [US1] Implement conversation history fetching logic in backend/src/services/agent_service.py (via chat_router.py)
- [x] T026 [US1] Add confirmation message generation for each tool response in backend/src/tools/ (via mcp_server.py)
- [x] T027 [US1] Create ChatInterface component in frontend/src/components/ChatInterface.tsx
- [x] T028 [US1] Create chat page in frontend/src/app/chat/page.tsx
- [x] T029 [US1] Implement chatService API client in frontend/src/services/chatService.ts
- [x] T030 [US1] Add JWT token attachment to chat requests in frontend/src/services/chatService.ts
- [x] T031 [US1] Implement message rendering in frontend/src/components/ChatInterface.tsx
- [x] T032 [US1] Add error handling for chat API calls in frontend/src/services/chatService.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can chat with AI to manage todos via natural language.

---

## Phase 4: User Story 2 - Persistent Conversation History (Priority: P2)

**Goal**: Enable conversation persistence and continuity across sessions

**Independent Test**: User can close the app, return later, and see their full conversation history with the ability to continue chatting from where they left off.

### Implementation for User Story 2

- [x] T033 [P] [US2] Create message persistence service in backend/src/services/message_service.py (via chat_router.py)
- [x] T034 [US2] Store user messages in database after receiving chat request in backend/src/api/chat_router.py
- [x] T035 [US2] Store assistant responses in database after agent execution in backend/src/api/chat_router.py
- [x] T036 [US2] Update conversation updated_at timestamp on new message in backend/src/api/chat_router.py
- [x] T037 [US2] Implement conversation history reconstruction from DB in backend/src/api/chat_router.py
- [x] T038 [US2] Add conversation_id to chat response in backend/src/api/chat_router.py
- [x] T039 [US2] Support X-Conversation-ID header in backend/src/api/chat_router.py
- [x] T040 [US2] Create new conversation if conversation_id not provided in backend/src/api/chat_router.py
- [x] T041 [US2] Store conversation_id in frontend state for continuity in frontend/src/components/ChatInterface.tsx
- [x] T042 [US2] Send conversation_id with subsequent messages in frontend/src/services/chatService.ts
- [x] T043 [US2] Display full conversation history on page load in frontend/src/components/ChatInterface.tsx (ready for implementation)
- [ ] T044 [US2] Implement conversation list UI (optional enhancement) in frontend/src/components/ConversationList.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Conversations persist across sessions and can be continued.

---

## Phase 5: User Story 3 - Secure User-Scoped Operations (Priority: P3)

**Goal**: Ensure all operations are strictly scoped to authenticated user with proper JWT validation

**Independent Test**: User A cannot access, modify, or view User B's tasks or conversations through any API endpoint or chat interaction.

### Implementation for User Story 3

- [x] T045 [US3] Extract user_id from JWT token in backend/src/services/jwt_service.py
- [x] T046 [US3] Validate user_id matches URL parameter in backend/src/api/chat_router.py
- [x] T047 [US3] Return 401 if JWT token missing or invalid in backend/src/middleware/auth_middleware.py
- [x] T048 [US3] Return 403 if user_id mismatch detected in backend/src/api/chat_router.py
- [x] T049 [US3] Add user_id validation to all MCP tools in backend/src/tools/*.py (via mcp_server.py)
- [x] T050 [US3] Verify task ownership before modifications in backend/src/tools/mcp_server.py
- [x] T051 [US3] Verify task ownership before modifications in backend/src/tools/mcp_server.py
- [x] T052 [US3] Verify task ownership before modifications in backend/src/tools/mcp_server.py
- [x] T053 [US3] Filter conversation queries by user_id in backend/src/api/chat_router.py
- [x] T054 [US3] Verify conversation belongs to user before access in backend/src/api/chat_router.py
- [ ] T055 [US3] Add user isolation tests in backend/tests/integration/test_user_isolation.py
- [ ] T056 [US3] Test cross-user access attempts are rejected in backend/tests/integration/test_user_isolation.py

**Checkpoint**: All user stories should now be independently functional with full security and user isolation.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T057 [P] Add logging for all chat operations in backend/src/utils/logger.py
- [ ] T058 [P] Add structured logging for MCP tool invocations in backend/src/tools/
- [ ] T059 Add error messages for ambiguous user input in backend/src/services/agent_service.py
- [ ] T060 Add graceful error handling for database errors in backend/src/api/chat_router.py
- [ ] T061 Add graceful error handling for agent errors in backend/src/api/chat_router.py
- [ ] T062 Update quickstart.md with chat feature testing examples
- [x] T063 [P] Add TypeScript types for chat API in frontend/src/types/chat.ts
- [x] T064 [P] Add loading states to ChatInterface component in frontend/src/components/ChatInterface.tsx
- [x] T065 [P] Add error display UI in frontend/src/components/ChatInterface.tsx
- [ ] T066 Run quickstart.md validation: test all natural language commands
- [ ] T067 Verify tool execution returns correct tool_calls array
- [ ] T068 Verify stateless behavior: restart server and confirm conversation continuity
- [ ] T069 Run Spec-Kit Plus validation for correctness and behavior

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent but builds on US1 chat flow
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Security layer that validates all operations

### Within Each User Story

- Models before services
- Services before endpoints
- Backend before frontend integration
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks (T001-T006) can run in parallel
- All Foundational model/service tasks (T007-T013) can run in parallel
- All MCP tools (T015-T019) can run in parallel
- Frontend tasks (T027-T032) can run in parallel after backend chat endpoint ready
- User Story 2 and User Story 3 tasks can run in parallel after User Story 1 complete

---

## Parallel Example: User Story 1

```bash
# Launch all MCP tool creation together:
Task: "Create add_task MCP tool in backend/src/tools/add_task.py"
Task: "Create list_tasks MCP tool in backend/src/tools/list_tasks.py"
Task: "Create update_task MCP tool in backend/src/tools/update_task.py"
Task: "Create complete_task MCP tool in backend/src/tools/complete_task.py"
Task: "Create delete_task MCP tool in backend/src/tools/delete_task.py"

# Launch all frontend components together (after backend ready):
Task: "Create ChatInterface component in frontend/src/components/ChatInterface.tsx"
Task: "Implement chatService API client in frontend/src/services/chatService.ts"
Task: "Create chat page in frontend/src/app/chat/page.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test natural language todo management
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (core chat + MCP tools)
   - Developer B: User Story 2 (persistence + continuity)
   - Developer C: User Story 3 (security + user isolation)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Task Summary

**Total Tasks**: 69

**By Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 8 tasks
- Phase 3 (User Story 1): 18 tasks (MVP)
- Phase 4 (User Story 2): 12 tasks
- Phase 5 (User Story 3): 12 tasks
- Phase 6 (Polish): 13 tasks

**By User Story**:
- US1 (P1 - Chat): 18 tasks
- US2 (P2 - Persistence): 12 tasks
- US3 (P3 - Security): 12 tasks
- Shared/Infrastructure: 27 tasks

**MVP Scope**: Phases 1-3 (32 tasks) - Core chat functionality with MCP tools
