# Tasks: AI Todo Chatbot Integration

**Input**: Design documents from `/specs/001-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are omitted per template guidelines.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- This project uses the web application structure with separate backend and frontend directories

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [X] T001 Install backend dependencies (openai, cohere, mcp-sdk) in backend/requirements.txt
- [X] T002 [P] Install frontend dependencies (lucide-react) in frontend/package.json
- [X] T003 [P] Add COHERE_API_KEY to backend/.env file
- [X] T004 [P] Verify existing Phase 2 authentication and task API are functional

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Alembic migration script in backend/alembic/versions/xxx_add_chat_tables.py for conversations and chat_messages tables
- [X] T006 Run database migration to create conversations and chat_messages tables
- [X] T007 [P] Create Conversation model in backend/src/models/conversation.py with SQLModel definition
- [X] T008 [P] Create ChatMessage model in backend/src/models/chat_message.py with SQLModel definition and MessageSender enum
- [X] T009 [P] Create Cohere API configuration in backend/src/config/cohere.py with OpenAI client initialization
- [X] T010 Verify database tables created and models importable

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks via natural language chat with floating chat icon and basic UI

**Independent Test**: Authenticate a user, open chat interface, send "Add a task to buy groceries", verify task appears in task list with correct details

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement add_task MCP tool in backend/services/mcp_tools.py with parameter validation and task creation
- [X] T012 [P] [US1] Create intent parser service in backend/services/intent_parser.py using Cohere via OpenAI SDK
- [X] T013 [US1] Create chat service in backend/services/chat_service.py with process_chat_message function (depends on T011, T012)
- [X] T014 [US1] Create chat API endpoint in backend/routes/chat.py with POST /api/{user_id}/chat route and JWT validation
- [X] T015 [US1] Register chat router in backend/main.py
- [X] T016 [P] [US1] Create ChatWidget root component in frontend/src/components/chat/ChatWidget.tsx with state management
- [X] T017 [P] [US1] Create ChatIcon floating button component in frontend/src/components/chat/ChatIcon.tsx
- [X] T018 [P] [US1] Create ChatWindow main window component in frontend/src/components/chat/ChatWindow.tsx
- [X] T019 [P] [US1] Create ChatHeader component in frontend/src/components/chat/ChatHeader.tsx with close button
- [X] T020 [P] [US1] Create MessageList scrollable component in frontend/src/components/chat/MessageList.tsx with auto-scroll
- [X] T021 [P] [US1] Create Message bubble component in frontend/src/components/chat/Message.tsx with user/bot styling
- [X] T022 [P] [US1] Create ChatInput component in frontend/src/components/chat/ChatInput.tsx with text input and send button
- [X] T023 [P] [US1] Create useChat hook in frontend/src/hooks/useChat.ts for chat state management
- [X] T024 [P] [US1] Create useChatAPI hook in frontend/src/hooks/useChatAPI.ts for API integration
- [X] T025 [P] [US1] Create chat service in frontend/src/services/chatService.ts for HTTP requests
- [X] T026 [US1] Add ChatWidget to dashboard page in frontend/src/app/dashboard/page.tsx
- [X] T027 [US1] Create chat-specific styles in frontend/src/styles/chat.css for message bubbles and layout
- [ ] T028 [US1] Test end-to-end: Open chat, send "Add task to buy milk", verify task created and response received

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - MVP complete!

---

## Phase 4: User Story 2 - Task Management via Chat (Priority: P2)

**Goal**: Enable full CRUD operations (list, complete, delete, update) through chat interface

**Independent Test**: Create several tasks, use chat commands to list, complete, update, and delete them, verify operations succeed

### Implementation for User Story 2

- [X] T029 [P] [US2] Implement list_tasks MCP tool in backend/src/services/mcp_tools.py with status and priority filters
- [X] T030 [P] [US2] Implement complete_task MCP tool in backend/src/services/mcp_tools.py with task_id validation
- [X] T031 [P] [US2] Implement delete_task MCP tool in backend/src/services/mcp_tools.py with user isolation check
- [X] T032 [P] [US2] Implement update_task MCP tool in backend/src/services/mcp_tools.py with partial update support
- [X] T033 [US2] Update intent parser in backend/src/services/intent_parser.py to handle list, complete, delete, update intents
- [X] T034 [US2] Update chat service in backend/src/services/chat_service.py to execute new MCP tools
- [ ] T035 [US2] Test end-to-end: Send "Show my tasks", "Mark task X as done", "Delete task Y", "Update task Z to high priority"

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full CRUD via chat complete!

---

## Phase 5: User Story 3 - User Information and Conversation History (Priority: P3)

**Goal**: Enable user info queries and persist conversation history across sessions

**Independent Test**: Ask "What's my email?", verify correct response, close and reopen chat, verify history persists

### Implementation for User Story 3

- [X] T036 [P] [US3] Implement get_user_info MCP tool in backend/src/services/mcp_tools.py extracting data from JWT token
- [X] T037 [US3] Update intent parser in backend/src/services/intent_parser.py to handle get_user_info intent
- [X] T038 [US3] Implement conversation history loading in backend/src/services/chat_service.py with 100 message limit
- [X] T039 [US3] Implement message persistence in backend/src/services/chat_service.py saving user and bot messages
- [X] T040 [US3] Update chat service to load history on conversation start
- [X] T041 [US3] Update useChat hook in frontend/src/hooks/useChat.ts to persist conversation_id in localStorage
- [X] T042 [US3] Update MessageList component in frontend/src/components/chat/MessageList.tsx to display history on load
- [ ] T043 [US3] Test end-to-end: Ask "What's my email?", close chat, reopen, verify history shows previous messages

**Checkpoint**: All core chat functionality complete - user info queries and conversation persistence working!

---

## Phase 6: User Story 4 - Urdu Language Support (Priority: P4) 🎁 BONUS +100

**Goal**: Enable Urdu language input/output with RTL layout in chat interface

**Independent Test**: Send Urdu messages for all operations, verify chatbot understands and responds in Urdu with RTL layout

### Implementation for User Story 4

- [X] T044 [P] [US4] Create English chat translations in frontend/public/locales/en/chat.json
- [X] T045 [P] [US4] Create Urdu chat translations in frontend/public/locales/ur/chat.json
- [X] T046 [US4] Update intent parser in backend/src/services/intent_parser.py to handle Urdu language detection
- [X] T047 [US4] Update chat service in backend/src/services/chat_service.py to respond in detected language
- [X] T048 [US4] Add RTL detection function in frontend/src/components/chat/Message.tsx using Unicode range check
- [X] T049 [US4] Update Message component styling to apply dir="rtl" for Urdu messages
- [X] T050 [US4] Update ChatInput placeholder to switch based on detected language
- [X] T051 [US4] Add Urdu font support in frontend/src/styles/chat.css
- [ ] T052 [US4] Test end-to-end: Send "ٹاسک شامل کریں: دودھ خریدنا", verify task created and Urdu response with RTL layout

**Checkpoint**: Urdu language support complete - bonus feature +100 points earned!

---

## Phase 7: User Story 5 - Voice Input for Hands-Free Task Management (Priority: P5) 🎁 BONUS +200

**Goal**: Enable voice input using Web Speech API for hands-free task creation and management

**Independent Test**: Click microphone, speak "Add task to call dentist", verify transcription and task creation

### Implementation for User Story 5

- [X] T053 [P] [US5] Create VoiceButton component in frontend/src/components/chat/VoiceButton.tsx with microphone icon
- [X] T054 [P] [US5] Create useVoiceInput hook in frontend/src/hooks/useVoiceInput.ts with Web Speech API integration
- [X] T055 [US5] Implement voice recognition start/stop logic in useVoiceInput hook
- [X] T056 [US5] Add microphone permission handling in useVoiceInput hook with error messages
- [X] T057 [US5] Implement auto-stop after 2 seconds of silence in useVoiceInput hook
- [X] T058 [US5] Add VoiceButton to ChatInput component in frontend/src/components/chat/ChatInput.tsx
- [X] T059 [US5] Connect voice transcript to message sending in ChatInput component
- [X] T060 [US5] Add visual feedback (pulsing animation) during recording in VoiceButton component
- [X] T061 [US5] Add language support (en-US, ur-PK) in useVoiceInput hook
- [ ] T062 [US5] Test end-to-end: Click microphone, speak "Add task to buy groceries", verify transcription and task creation

**Checkpoint**: Voice input complete - bonus feature +200 points earned! All user stories implemented!

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final deployment preparation

- [X] T063 [P] Add error handling for Cohere API failures in backend/src/services/intent_parser.py
- [ ] T064 [P] Add rate limiting (60 messages/minute) to chat endpoint in backend/src/api/chat.py
- [X] T065 [P] Add loading indicators during API calls in frontend/src/components/chat/ChatWindow.tsx
- [X] T066 [P] Add error message display in frontend/src/components/chat/ChatWindow.tsx
- [X] T067 [P] Optimize conversation history query with proper indexes in database
- [X] T068 [P] Add welcome message on first chat open in frontend/src/components/chat/MessageList.tsx
- [X] T069 [P] Add timestamp display to messages in frontend/src/components/chat/Message.tsx
- [X] T070 [P] Implement responsive design for mobile in frontend/src/styles/chat.css
- [X] T071 Update README.md with Phase 3 documentation, setup instructions, and bonus features
- [ ] T072 Create demo video (<90 seconds) showing all features: CRUD, user info, Urdu, voice input
- [ ] T073 Deploy backend to Render/Railway with environment variables
- [ ] T074 Deploy frontend to Vercel with API URL configuration
- [ ] T075 Run smoke tests on deployed application
- [ ] T076 Prepare submission: repo link, deployed URLs, demo video, WhatsApp number

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Adds to US1/US2 but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Bonus feature, independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Bonus feature, independently testable

### Within Each User Story

- Backend MCP tools can be implemented in parallel (marked [P])
- Frontend components can be implemented in parallel (marked [P])
- Services depend on tools being complete
- API endpoints depend on services being complete
- Frontend integration depends on API being functional
- End-to-end testing is the final step for each story

### Parallel Opportunities

- All Setup tasks (T001-T004) can run in parallel
- All Foundational model tasks (T007-T009) can run in parallel after migration
- Within US1: All MCP tools, components, and hooks marked [P] can run in parallel
- Within US2: All 4 MCP tools (T029-T032) can run in parallel
- Within US4: Translation files (T044-T045) can run in parallel
- Within US5: VoiceButton and useVoiceInput (T053-T054) can run in parallel
- All Polish tasks (T063-T070) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all backend MCP tools together:
Task: "Implement add_task MCP tool in backend/src/services/mcp_tools.py"
Task: "Create intent parser service in backend/src/services/intent_parser.py"

# Launch all frontend components together:
Task: "Create ChatWidget root component in frontend/src/components/chat/ChatWidget.tsx"
Task: "Create ChatIcon floating button component in frontend/src/components/chat/ChatIcon.tsx"
Task: "Create ChatWindow main window component in frontend/src/components/chat/ChatWindow.tsx"
Task: "Create ChatHeader component in frontend/src/components/chat/ChatHeader.tsx"
Task: "Create MessageList scrollable component in frontend/src/components/chat/MessageList.tsx"
Task: "Create Message bubble component in frontend/src/components/chat/Message.tsx"
Task: "Create ChatInput component in frontend/src/components/chat/ChatInput.tsx"

# Launch all hooks together:
Task: "Create useChat hook in frontend/src/hooks/useChat.ts"
Task: "Create useChatAPI hook in frontend/src/hooks/useChatAPI.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T010) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T011-T028)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready - you now have a working AI chatbot for task creation!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - task creation via chat!)
3. Add User Story 2 → Test independently → Deploy/Demo (full CRUD via chat!)
4. Add User Story 3 → Test independently → Deploy/Demo (user info + history!)
5. Add User Story 4 → Test independently → Deploy/Demo (Urdu support +100 bonus!)
6. Add User Story 5 → Test independently → Deploy/Demo (voice input +200 bonus!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T011-T028)
   - Developer B: User Story 2 (T029-T035)
   - Developer C: User Story 3 (T036-T043)
   - Developer D: User Story 4 (T044-T052)
   - Developer E: User Story 5 (T053-T062)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are NOT included as they were not explicitly requested in the specification
- All 5 user stories are independently testable and can be deployed incrementally
- Bonus features (US4, US5) are optional but earn +300 total bonus points
