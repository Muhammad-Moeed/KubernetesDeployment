---
description: "Task list for Frontend Professional UI implementation"
---

# Tasks: Frontend Professional UI Specificationsopt

**Input**: Design documents from `/specs/001-frontend-ui-specs/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`
- **Backend**: `backend/src/` (already implemented)

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETED

**Purpose**: Project initialization and basic structure

- [X] T001 Verify Next.js 16+ project structure exists in frontend/ directory
- [X] T002 Install required dependencies: next, react, typescript, tailwindcss, better-auth
- [X] T003 [P] Configure TypeScript with strict mode in frontend/tsconfig.json
- [X] T004 [P] Configure Tailwind CSS with design system colors in frontend/tailwind.config.ts
- [X] T005 [P] Create environment variables template in frontend/.env.example with NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET
- [X] T006 Configure Next.js App Router structure in frontend/src/app/

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETED

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Setup Better Auth configuration in frontend/src/lib/auth.ts with JWT token generation
- [X] T008 Create API client utility in frontend/src/lib/api-client.ts with JWT token injection and error handling
- [X] T009 [P] Setup i18n utilities in frontend/src/lib/i18n.ts with English and Urdu locales
- [X] T010 [P] Create English translations file in frontend/src/lib/locales/en.json
- [X] T011 [P] Create Urdu translations file in frontend/src/lib/locales/ur.json
- [X] T012 [P] Setup theme provider with light/dark mode in frontend/src/providers/theme-provider.tsx
- [X] T013 [P] Create authentication context in frontend/src/contexts/auth-context.tsx for user session management
- [X] T014 Create protected route wrapper component in frontend/src/components/auth/protected-route.tsx
- [X] T015 Create authentication middleware in frontend/src/middleware.ts to redirect unauthenticated users
- [X] T016 [P] Define TypeScript types for Task entity in frontend/src/types/task.ts
- [X] T017 [P] Define TypeScript types for User entity in frontend/src/types/user.ts

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Professional Dashboard Experience (Priority: P1) 🎯 MVP ✅ COMPLETED

**Goal**: Provide a professional dashboard layout with sidebar navigation and global header for authenticated users

**Independent Test**: Authenticate, land on Tasks page, navigate to Settings using sidebar, verify header controls are visible, logout and confirm redirect to landing page

### Implementation for User Story 1

- [X] T018 [P] [US1] Create Sidebar component in frontend/src/components/layout/sidebar.tsx with navigation items (Tasks, Settings, Logout)
- [X] T019 [P] [US1] Create Header component in frontend/src/components/layout/header.tsx with theme toggle, language switcher, and user avatar
- [X] T020 [US1] Create DashboardLayout component in frontend/src/components/layout/dashboard-layout.tsx integrating Sidebar and Header
- [X] T021 [P] [US1] Create Tasks page in frontend/src/app/(dashboard)/tasks/page.tsx with placeholder content
- [X] T022 [P] [US1] Create Settings page in frontend/src/app/(dashboard)/settings/page.tsx with placeholder content
- [X] T023 [US1] Implement logout functionality in Sidebar component calling Better Auth signOut
- [X] T024 [P] [US1] Create Landing page in frontend/src/app/page.tsx with hero section and CTAs
- [X] T025 [P] [US1] Create Login page in frontend/src/app/login/page.tsx with email/password form
- [X] T026 [P] [US1] Create Signup page in frontend/src/app/signup/page.tsx with email/password form
- [X] T027 [US1] Implement authentication redirect logic: unauthenticated users see landing, authenticated users see dashboard

**Checkpoint**: ✅ User Story 1 is fully functional - users can navigate the dashboard, access Tasks/Settings, and logout

---

## Phase 4: User Story 2 - Advanced Task Management UI (Priority: P1) ✅ COMPLETED

**Goal**: Enable users to create, view, edit, complete, and delete tasks through a professional card-based UI

**Independent Test**: Create a task via modal, see it in the grid, edit it, toggle completion, delete it with confirmation

### Implementation for User Story 2

- [X] T028 [P] [US2] Create TaskCard component in frontend/src/components/tasks/task-card.tsx displaying title, priority badge, tags, due date, completion checkbox, and edit/delete actions
- [X] T029 [P] [US2] Create TaskList component in frontend/src/components/tasks/task-list.tsx with grid layout for task cards
- [X] T030 [P] [US2] Create AddTaskModal component in frontend/src/components/tasks/add-task-modal.tsx with form fields (title, description, priority, tags, due date)
- [X] T031 [P] [US2] Create PriorityBadge component in frontend/src/components/tasks/priority-badge.tsx with color-coded styling
- [X] T032 [P] [US2] Create TagChip component in frontend/src/components/tasks/tag-chip.tsx for displaying task tags
- [X] T033 [P] [US2] Create DeleteConfirmDialog component in frontend/src/components/tasks/delete-confirm-dialog.tsx
- [X] T034 [US2] Implement create task API integration in AddTaskModal calling POST /api/{user_id}/tasks
- [X] T035 [US2] Implement list tasks API integration in TaskList calling GET /api/{user_id}/tasks
- [X] T036 [US2] Implement update task API integration in AddTaskModal calling PUT /api/{user_id}/tasks/{task_id}
- [X] T037 [US2] Implement toggle completion API integration in TaskCard calling PATCH /api/{user_id}/tasks/{task_id}/complete
- [X] T038 [US2] Implement delete task API integration in DeleteConfirmDialog calling DELETE /api/{user_id}/tasks/{task_id}
- [X] T039 [US2] Add due date highlighting logic in TaskCard to show overdue dates in danger red color
- [X] T040 [US2] Update Tasks page in frontend/src/app/(dashboard)/tasks/page.tsx to integrate TaskList and AddTaskModal

**Checkpoint**: ✅ User Stories 1 AND 2 both work independently - full CRUD operations on tasks are functional

---

## Phase 5: User Story 3 - Find Tasks with Search, Filters, and Sort (Priority: P2) ✅ COMPLETED

**Goal**: Enable users to search, filter, and sort tasks for efficient task discovery

**Independent Test**: Create multiple tasks with varying tags, priorities, due dates; apply search/filter/sort and verify displayed results match criteria

### Implementation for User Story 3

- [X] T041 [P] [US3] Create SearchBar component in frontend/src/components/tasks/search-bar.tsx with debounced input
- [X] T042 [P] [US3] Create FilterBar component in frontend/src/components/tasks/filter-bar.tsx with status, priority, tag, and due date filters
- [X] T043 [P] [US3] Create SortDropdown component in frontend/src/components/tasks/sort-dropdown.tsx with sort field and order options
- [X] T044 [P] [US3] Create ActiveFilters component in frontend/src/components/tasks/active-filters.tsx showing filter chips with clear actions
- [X] T045 [US3] Create task query state management hook in frontend/src/hooks/use-task-query.ts managing search, filters, and sort state
- [X] T046 [US3] Integrate SearchBar into Tasks page and connect to query state
- [X] T047 [US3] Integrate FilterBar into Tasks page and connect to query state
- [X] T048 [US3] Integrate SortDropdown into Tasks page and connect to query state
- [X] T049 [US3] Update TaskList to call GET /api/{user_id}/tasks with query parameters (status, priority, tag, search, sort, order, due_before)
- [X] T050 [US3] Implement "Clear filters" functionality resetting all filters to default state
- [X] T051 [US3] Add empty state for zero filter results in TaskList with "No tasks match your filters" message

**Checkpoint**: ✅ All user stories 1-3 are independently functional - advanced task discovery is working

---

## Phase 6: User Story 4 - Theme and Language Personalization (Priority: P2)

**Goal**: Enable users to switch between light/dark themes and English/Urdu languages with RTL support

**Independent Test**: Toggle theme and language; refresh page; verify preferences persist and layout direction changes for Urdu

### Implementation for User Story 4

- [ ] T052 [P] [US4] Implement theme toggle button in Header component with sun/moon icons
- [ ] T053 [P] [US4] Implement language switcher in Header component with EN/اردو toggle
- [ ] T054 [US4] Add theme persistence using localStorage in theme-provider.tsx
- [ ] T055 [US4] Add language persistence using cookies in i18n configuration
- [ ] T056 [US4] Complete all English translations in frontend/src/i18n/locales/en.json covering all UI strings (navigation, tasks, auth, settings)
- [ ] T057 [US4] Complete all Urdu translations in frontend/src/i18n/locales/ur.json covering all UI strings
- [ ] T058 [US4] Implement RTL layout support in frontend/src/app/layout.tsx applying dir="rtl" when Urdu is active
- [ ] T059 [US4] Update Sidebar component to anchor right in RTL mode
- [ ] T060 [US4] Update TaskCard component to support RTL text alignment and icon positioning
- [ ] T061 [US4] Update all form components to support RTL layout
- [ ] T062 [US4] Test and fix RTL layout issues across Tasks, Settings, Auth pages

**Checkpoint**: Theme and language switching should work seamlessly with full RTL support for Urdu

---

## Phase 7: User Story 5 - Voice-Assisted Task Creation (Priority: P3) ✅ COMPLETED

**Goal**: Enable users to create tasks using voice input for the task title field

**Independent Test**: Open Add Task modal, click microphone, speak a task title, verify the title input is populated; test denial/error flows

### Implementation for User Story 5

- [X] T063 [P] [US5] Create voice recognition hook in frontend/src/hooks/use-voice-recognition.ts using Web Speech API
- [X] T064 [P] [US5] Create MicrophoneButton component in frontend/src/components/ui/microphone-button.tsx with listening state indicator
- [X] T065 [US5] Integrate MicrophoneButton into AddTaskModal title input field
- [X] T066 [US5] Implement voice recognition permission request flow with user-friendly prompts
- [X] T067 [US5] Implement listening state UI feedback (pulsing microphone icon) in MicrophoneButton
- [X] T068 [US5] Implement speech-to-text result handling populating title input field
- [X] T069 [US5] Implement voice recognition error handling for permission denied, timeout, and unsupported browser
- [X] T070 [US5] Add non-blocking error toast notifications for voice recognition failures
- [X] T071 [US5] Ensure manual typing fallback always works when voice recognition fails

**Checkpoint**: ✅ Voice-assisted task creation works reliably with graceful error handling and toast notifications

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall UX quality

- [ ] T072 [P] Create EmptyState component in frontend/src/components/ui/empty-state.tsx for "no tasks" scenario
- [ ] T073 [P] Create LoadingSpinner component in frontend/src/components/ui/loading-spinner.tsx
- [ ] T074 [P] Create SkeletonCard component in frontend/src/components/ui/skeleton-card.tsx for loading states
- [ ] T075 Add loading states to TaskList showing skeleton cards while fetching
- [ ] T076 Add loading states to AddTaskModal submit button preventing duplicate submissions
- [ ] T077 Add error toast notifications for API failures across all CRUD operations
- [ ] T078 Implement responsive design for mobile/tablet in DashboardLayout (collapsible sidebar)
- [ ] T079 Implement responsive design for TaskList (single column on mobile, grid on desktop)
- [ ] T080 Add keyboard navigation support for modal dialogs and interactive elements
- [ ] T081 Add focus indicators for accessibility compliance
- [ ] T082 Optimize task card layout for long titles (truncation with ellipsis)
- [ ] T083 Optimize tag display for many tags (wrapping with max visible count)
- [ ] T084 Add visual polish: consistent spacing, shadows, rounded corners per design system
- [ ] T085 Add visual polish: typography hierarchy across all pages
- [ ] T086 Test and fix any remaining visual inconsistencies in light/dark themes
- [ ] T087 Verify all API error responses (401, 403, 404, 500) are handled gracefully with user-friendly messages
- [ ] T088 Add network latency handling with optimistic UI updates for task completion toggle
- [ ] T089 [P] Update README.md with setup instructions, environment variables, and bonus feature showcase
- [ ] T090 [P] Create .env.example file in frontend/ with all required environment variables

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Requires US1 dashboard layout to display tasks
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Requires US2 TaskList component to apply filters
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent but enhances all pages
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Requires US2 AddTaskModal to add voice input

### Within Each User Story

- Components marked [P] can be built in parallel (different files)
- API integration tasks depend on component completion
- Page integration tasks depend on all components being ready

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, US1 and US4 can start in parallel
- Within each user story, all components marked [P] can be built in parallel
- Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 2

```bash
# Launch all components for User Story 2 together:
Task: "Create TaskCard component in frontend/src/components/tasks/task-card.tsx"
Task: "Create TaskList component in frontend/src/components/tasks/task-list.tsx"
Task: "Create AddTaskModal component in frontend/src/components/tasks/add-task-modal.tsx"
Task: "Create PriorityBadge component in frontend/src/components/tasks/priority-badge.tsx"
Task: "Create TagChip component in frontend/src/components/tasks/tag-chip.tsx"
Task: "Create DeleteConfirmDialog component in frontend/src/components/tasks/delete-confirm-dialog.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Dashboard)
4. Complete Phase 4: User Story 2 (Task CRUD)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Navigation MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (Full CRUD MVP!)
4. Add User Story 3 → Test independently → Deploy/Demo (Power user features!)
5. Add User Story 4 → Test independently → Deploy/Demo (i18n + themes!)
6. Add User Story 5 → Test independently → Deploy/Demo (Voice bonus!)
7. Add Polish → Final quality pass → Deploy/Demo (Production ready!)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Dashboard)
   - Developer B: User Story 4 (Theme/i18n setup)
3. After US1 completes:
   - Developer A: User Story 2 (Task CRUD)
   - Developer B: User Story 3 (Search/Filter)
   - Developer C: User Story 5 (Voice)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Backend API is already implemented per plan.md
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths use forward slashes for cross-platform compatibility
- TypeScript strict mode enforced for type safety
- Tailwind CSS used for all styling (no custom CSS files)
- Better Auth handles JWT token management automatically
- API client automatically injects JWT tokens from Better Auth session
