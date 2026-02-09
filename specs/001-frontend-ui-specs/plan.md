# Phase 2 Plan: Advanced Professional Todo App

## 1) Phase Goal

Build a **full-stack, multi-user** advanced Todo application with a **professional, market-ready UI**, while strictly following the project constitution (spec-driven workflow, zero manual coding, user isolation, and bonus-first integration).

**Core product features**:
- Task CRUD (create, view, edit, delete)
- Completion toggle
- Priorities (high/medium/low)
- Tags
- Search
- Filter
- Sort
- Due dates (including overdue highlighting)

**Professional design goals**:
- Sidebar dashboard layout (Tasks, Settings, Logout)
- Global header with:
  - Theme toggle (light/dark)
  - Language switcher (EN / اردو)
  - User avatar
- Modern card/grid task list, clean spacing, strong visual hierarchy
- Consistent color scheme:
  - Primary: `#1E40AF`
  - Success: `#16A34A`
  - Danger: `#DC2626`
  - Neutral grays for text/borders/backgrounds

**Bonus maximization goals**:
- **Reusable Intelligence (+200)**: Use the defined agents/skills in the intended workflow; document usage.
- **Urdu support (+100)**: Full i18n coverage + RTL layout.
- **Voice commands (+200)**: Web Speech API voice input and task-management commands integrated into task flows.

---

## 2) Current Status

- ✅ **CONSTITUTION.md** completed and governing the workflow.
- ✅ **Backend specs** completed.
- ✅ **Backend implementation** completed (API + user isolation + auth).
- ✅ **Frontend specs** completed:
  - `/specs/ui/components.md`
  - `/specs/features/frontend-todo.md`
- 🔄 **Frontend implementation** is in progress.

---

## 3) Implementation Steps (Sequential Order)

### Step 1: Complete frontend implementation (dashboard foundation)

**Outcome**: A professional, authenticated shell users can navigate.

- Implement dashboard layout:
  - Sidebar navigation: Tasks, Settings, Logout
  - Header: theme toggle, language switcher, user avatar
- Implement routing for:
  - Landing/Home (unauthenticated)
  - Login / Signup
  - Tasks dashboard
  - Settings
- Ensure authentication gating and redirect behavior:
  - Unauthenticated users see landing/auth
  - Authenticated users land on Tasks

**References**:
- `/specs/ui/components.md`
- `/specs/features/authentication.md`

---

### Step 2: Implement advanced UI features (search, filters, sort, visual semantics)

**Outcome**: A complete task management UI aligned with the backend API.

- Build Tasks page UI:
  - TaskList in grid/card layout
  - TaskCard with:
    - Priority badge
    - Tag chips
    - Due date + overdue highlighting
    - Complete toggle
    - Edit/Delete actions
  - Add/Edit Task modal with full fields
- Implement list discovery controls:
  - Search bar
  - Filters: priority, tags, status, due date range
  - Sort dropdown
  - Clear filters behavior
- Ensure all UI controls map to backend query parameters and endpoints.

**References**:
- `/specs/api/rest-endpoints.md`
- `/specs/ui/components.md`
- `/specs/features/frontend-todo.md`

---

### Step 3: Add voice command input on task forms with parsing

**Outcome**: Voice is a first-class interaction, not a demo-only add-on.

- Add microphone button in task title input (Add/Edit Task modal).
- Implement voice input feedback:
  - Clear listening state
  - Permission prompt handling
  - Friendly error + manual fallback
- Implement command parsing on recognized speech to populate fields when possible:
  - Priority (high/medium/low)
  - Tags (extract simple tag phrases)
  - Due date (basic supported phrases with graceful fallback)

**References**:
- `/specs/ui/components.md` (Voice Input section)
- `/specs/features/frontend-todo.md` (Voice-assisted story + edge cases)

---

### Step 4: Implement Urdu language support with full RTL layout toggle

**Outcome**: Full bilingual UI with correct RTL behavior.

- Add English + Urdu translations for all UI strings.
- Ensure no hardcoded UI strings remain.
- Implement RTL layout behavior in Urdu:
  - Direction flips (layout + alignment)
  - Sidebar moves to right
  - Directional icons flip where relevant
- Validate Tasks, Auth, Landing, Settings for both languages.

**References**:
- Constitution: Internationalization Standards
- `/specs/ui/components.md`

---

### Step 5: Full end-to-end integration testing

**Outcome**: Demonstrable, reliable system behavior across the full stack.

Test the complete flow:
- Signup → login
- Add task (including voice-assisted title)
- Edit, complete, delete task
- Apply search/filter/sort
- Switch to Urdu (RTL) and verify layout
- Toggle theme and verify persistence

**References**:
- `/specs/api/rest-endpoints.md`
- `/specs/features/authentication.md`

---

### Step 6: Polish pro design (visual + UX quality)

**Outcome**: Market-like UI quality suitable for demo and judging.

- Visual polish:
  - Spacing consistency
  - Typography hierarchy
  - Card shadows/borders
  - Consistent iconography
- UX polish:
  - Loading states (skeletons/spinners)
  - Empty states (no tasks / no filter results)
  - Error messaging (network/auth/validation)
  - Responsive layout checks (mobile/tablet/desktop)

---

### Step 7: Prepare deployment (Vercel frontend, backend hosting)

**Outcome**: Deployed URLs ready for submission.

- Prepare frontend deployment (Vercel):
  - Environment variables set correctly
  - Auth configuration points to production
- Prepare backend hosting:
  - Environment variables configured
  - CORS restricted to frontend origin
- Validate deployed end-to-end functionality.

---

### Step 8: Update documentation (README with bonus showcase, .env.example)

**Outcome**: Clear setup instructions and explicit bonus documentation.

- Update README with:
  - Setup steps
  - Local run instructions
  - Deployed URLs
  - Bonus showcase instructions (Urdu + voice + reusable intelligence)
- Add/verify `.env.example` files for frontend and backend.

---

### Step 9: Record <90 second professional demo video

**Outcome**: A concise demo showcasing value + bonuses.

Include:
- Professional dashboard UI
- CRUD flow
- Search/filter/sort
- Theme toggle
- Urdu RTL switch
- Voice task creation

---

### Step 10: Final review and submission via Google Form

**Outcome**: Complete and correct hackathon submission.

- Final repo check:
  - Public GitHub repo
  - Constitution and specs present
  - App runs without console errors
- Submit via Google Form:
  - Repo link
  - Deployed app link(s)
  - Demo video link
  - WhatsApp number

---

## 4) Agent Usage Guide

- **@nextjs-frontend-builder**: Core frontend components and pages.
- **@fullstack-todo-agent**: End-to-end integration and cross-stack fixes.
- **@deployment-prep**: Documentation, tests, deployment readiness, demo prep.
- **@spec-refiner**: Spec updates/refinement if requirements change or gaps are found.

---

## 5) Bonus Achievement Strategy

### Reusable Intelligence (+200)

- Use the defined agents and skills consistently throughout implementation.
- Keep `/specs/` as the source of truth (update specs when behavior changes).
- Highlight agent/skill usage explicitly in README.

### Urdu Support (+100)

- Complete i18n coverage of all UI text.
- Enforce RTL layout as a core mode (not partial styling).
- Demonstrate Urdu + RTL in the demo video.

### Voice Commands (+200)

- Reliable Web Speech API integration with clear UI feedback.
- Include command parsing for task creation fields when possible.
- Demonstrate voice input and error fallback in the demo video.

---

## 6) Submission Checklist

- [ ] Public GitHub repo with **CONSTITUTION.md** and full **/specs/**
- [ ] Working deployed app (Vercel + backend URL)
- [ ] <90 second demo video showing pro design + all bonuses
- [ ] Google Form submission with:
  - Repo link
  - App link
  - Video link
  - WhatsApp number

---

Following this plan step by step will deliver a professional, bonus-maximized Phase 2 submission that stands out.
