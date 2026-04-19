# Tasks: Todo Full-Stack Web Application – Phase II (Hackathon)

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure in backend/
- [X] T002 Create frontend project structure in frontend/
- [X] T003 [P] Initialize backend with FastAPI dependencies in backend/requirements.txt
- [X] T004 [P] Initialize frontend with Next.js dependencies in frontend/package.json
- [X] T005 Create shared environment configuration in .env
- [X] T006 Create docker-compose.yml for local development
- [X] T007 Create README.md with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T008 Setup database schema and migrations framework in backend/alembic/
- [X] T009 [P] Configure Better Auth for JWT authentication in backend/src/config/
- [X] T010 [P] Setup JWT middleware for token validation in backend/src/middleware/jwt_middleware.py
- [X] T011 Create base User and Task models in backend/src/models/
- [X] T012 Configure database connection in backend/src/config/database.py
- [X] T013 Setup CORS and security headers in backend/src/main.py
- [X] T014 Create frontend authentication service in frontend/src/services/auth.ts
- [X] T015 Setup frontend API service in frontend/src/services/api.ts
- [X] T016 Create frontend types for User and Task in frontend/src/types/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Manage Personal Todo Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to create, view, update, and delete their personal todo tasks through a web interface

**Independent Test**: Can be fully tested by creating a user account, logging in, creating tasks, viewing them, updating them, and deleting them. Delivers the core value of task management.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US1] Contract test for GET /api/{user_id}/tasks in backend/tests/test_tasks.py
- [ ] T018 [P] [US1] Contract test for POST /api/{user_id}/tasks in backend/tests/test_tasks.py
- [ ] T019 [P] [US1] Contract test for PUT /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py
- [ ] T020 [P] [US1] Contract test for DELETE /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py
- [ ] T021 [P] [US1] Integration test for task CRUD operations in backend/tests/test_tasks.py

### Implementation for User Story 1

- [X] T022 [P] [US1] Create Task model in backend/src/models/task.py
- [X] T023 [P] [US1] Create TaskService in backend/src/services/task_service.py
- [X] T024 [US1] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/task_router.py
- [X] T025 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/task_router.py
- [X] T026 [US1] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/task_router.py
- [X] T027 [US1] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/task_router.py
- [X] T028 [US1] Create TaskList component in frontend/src/components/TaskList.tsx
- [X] T029 [US1] Create TaskForm component in frontend/src/components/TaskForm.tsx
- [X] T030 [US1] Create TaskItem component in frontend/src/components/TaskItem.tsx
- [X] T031 [US1] Create tasks page in frontend/src/app/dashboard/tasks/page.tsx
- [X] T032 [US1] Create task creation page in frontend/src/app/dashboard/tasks/create/page.tsx
- [X] T033 [US1] Add frontend API calls for task operations in frontend/src/services/api.ts
- [X] T034 [US1] Add frontend navigation for task management in frontend/src/components/Navbar.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure Authentication and User Isolation (Priority: P2)

**Goal**: Implement secure authentication and ensure users can only access their own tasks

**Independent Test**: Can be tested by registering multiple users, logging in as each user, and verifying that they can only see their own tasks. Ensures data isolation between users.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T035 [P] [US2] Contract test for JWT validation middleware in backend/tests/test_auth.py
- [ ] T036 [P] [US2] Integration test for user isolation in backend/tests/test_tasks.py
- [ ] T037 [P] [US2] Unit test for JWT token decoding in backend/tests/test_auth.py

### Implementation for User Story 2

- [X] T038 [P] [US2] Implement JWT validation in backend/src/middleware/jwt_middleware.py
- [X] T039 [US2] Add user_id validation to all task endpoints in backend/src/api/task_router.py
- [X] T040 [US2] Implement user isolation in TaskService methods in backend/src/services/task_service.py
- [X] T041 [US2] Create login page in frontend/src/app/login/page.tsx
- [X] T042 [US2] Create signup page in frontend/src/app/signup/page.tsx
- [ ] T043 [US2] Implement login form component in frontend/src/components/LoginForm.tsx
- [X] T044 [US2] Integrate authentication with Better Auth in frontend
- [X] T045 [US2] Add protected routes in frontend to ensure authentication
- [X] T046 [US2] Add error handling for unauthorized access in frontend/src/services/api.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - View Detailed Task Information (Priority: P3)

**Goal**: Allow users to view detailed information about each task and toggle completion status

**Independent Test**: Can be tested by creating tasks with detailed information and verifying that users can view these details. Enhances the core task management experience.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T047 [P] [US3] Contract test for GET /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py
- [ ] T048 [P] [US3] Contract test for PATCH /api/{user_id}/tasks/{id}/complete in backend/tests/test_tasks.py
- [ ] T049 [P] [US3] Integration test for task detail view in backend/tests/test_tasks.py

### Implementation for User Story 3

- [X] T050 [P] [US3] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/task_router.py
- [X] T051 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/task_router.py
- [X] T052 [US3] Add task detail view in frontend/src/app/dashboard/tasks/[id]/page.tsx
- [X] T053 [US3] Add task detail component in frontend/src/components/TaskDetail.tsx
- [X] T054 [US3] Add toggle completion functionality in frontend/src/components/TaskItem.tsx
- [X] T055 [US3] Update TaskService to handle task completion toggle in backend/src/services/task_service.py
- [X] T056 [US3] Add frontend API calls for task detail and completion toggle in frontend/src/services/api.ts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T057 [P] Update documentation in README.md with API endpoints and usage
- [ ] T058 Add responsive design to all frontend components using Tailwind CSS
- [ ] T059 Add loading states and error handling to all frontend components
- [ ] T060 [P] Add unit tests for backend services in backend/tests/
- [ ] T061 Add end-to-end tests for critical user flows in frontend/tests/
- [ ] T062 Security hardening: input validation, SQL injection protection
- [ ] T063 Run quickstart.md validation to ensure all setup instructions work
- [ ] T064 Performance optimization: database query optimization, API response caching
- [ ] T065 Final integration testing of all user stories together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for GET /api/{user_id}/tasks in backend/tests/test_tasks.py"
Task: "Contract test for POST /api/{user_id}/tasks in backend/tests/test_tasks.py"
Task: "Contract test for PUT /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py"
Task: "Contract test for DELETE /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py"
Task: "Integration test for task CRUD operations in backend/tests/test_tasks.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task.py"
Task: "Create TaskService in backend/src/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
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
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence