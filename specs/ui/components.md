# UI Components Specification: Advanced Professional Todo App

**Created**: 2026-01-07
**Status**: Draft
**Related**: `/specs/api/rest-endpoints.md`, `/specs/features/authentication.md`

## Purpose

Define an implementation-ready UI component and interaction specification for a professional, market-ready Todo web app that supports:

- A dashboard-style layout (sidebar + header + main content)
- Light/dark themes
- English + Urdu language support (including RTL layout)
- Voice-assisted task creation (microphone input on task title)
- Advanced task discovery (search, filters, sort)

This document specifies **what** the UI must look like and **how** it must behave from a user perspective.

---

## Design System

### Brand & Color Palette

- **Primary (Blue)**: `#1E40AF`
- **Success (Green)**: `#16A34A`
- **Danger (Red)**: `#DC2626`
- **Neutral Grays**: use a neutral gray scale for text, borders, backgrounds

### Visual Style Guidelines

- Modern, clean, productivity SaaS aesthetic
- Consistent spacing rhythm and alignment
- Card-based content with subtle shadows and rounded corners
- Clear visual hierarchy:
  - Page title and key actions visible above the fold
  - Filters/search secondary but discoverable
- Accessibility:
  - Sufficient contrast in both light and dark theme
  - Keyboard navigable controls
  - Focus indicators for interactive elements

### Typography

- Clear, readable sans-serif
- Use consistent text styles:
  - Page titles: prominent
  - Section headings: medium emphasis
  - Body text: neutral
  - Metadata (dates, tags): subdued

---

## Global Layout

### Layout Structure

Authenticated pages use a 3-region layout:

1. **Sidebar** (left in LTR, right in RTL)
2. **Header** (top, spans remaining width)
3. **Main Content** (task list, settings, etc.)

**Responsive behavior**:
- Desktop: persistent sidebar
- Tablet: collapsible sidebar (toggle button in header)
- Mobile: sidebar becomes an off-canvas drawer

### Theme Support

- The app MUST support **light** and **dark** themes
- Theme switch must be available globally (Header)
- Theme choice persists across sessions (user preference)

### Language + RTL Support (English / اردو)

- The UI MUST support switching between:
  - English (LTR)
  - Urdu (RTL)
- When Urdu is selected:
  - Layout direction becomes RTL (sidebar moves to right)
  - Text alignment defaults to right for most content
  - Icons that imply direction (arrows, chevrons, pagination) must flip direction

---

## Navigation Components

### Sidebar Navigation

**Purpose**: primary navigation between authenticated app sections.

**Elements**:
- Logo/Brand area at top
- Menu items (with icons):
  - **Tasks** (default)
  - **Settings**
  - **Logout**

**Behavior**:
- Current route is visibly highlighted
- Hover states for items
- Logout is a destructive/exit action:
  - Click triggers logout flow
  - After logout, user is redirected to Landing/Home

**RTL behavior**:
- Sidebar anchors to right
- Icons remain consistent; spacing mirrors LTR

### Header

**Purpose**: global controls and context.

**Elements**:
- Page title (e.g., “Tasks”, “Settings”)
- Theme toggle (light/dark)
- Language switcher:
  - Two-state toggle or segmented control: **EN** / **اردو**
- User avatar (circle)
  - Clicking opens a small menu (optional): profile summary + logout shortcut

**Behavior**:
- Header remains visible while scrolling task list (sticky)
- On mobile:
  - header contains hamburger icon to open sidebar

---

## Tasks Page Components

### TaskList (Grid/Card Layout)

**Purpose**: view and manage tasks.

**Sections**:
1. **Top bar**
   - Search input
   - Add Task primary button
2. **Filter bar**
   - Advanced filters (priority, tags, status, due date range)
   - Sort dropdown
   - “Clear filters” action (only visible when any filter is active)
3. **Results**
   - Card grid on desktop
   - Single-column cards on mobile

**Empty state**:
- If user has no tasks:
  - Show friendly empty state illustration/placeholder
  - Primary CTA: “Add your first task”
- If filters yield zero results:
  - Show “No tasks match your filters”
  - CTA: Clear filters

**Loading state**:
- Skeleton cards in grid
- Search/filter controls remain usable but indicate loading when query changes

**Many tasks behavior**:
- Scrolling performance must remain smooth
- Provide clear pagination/infinite-scroll approach (implementation choice) while maintaining usability

### Search Bar

**Placement**: top bar.

**Behavior**:
- Placeholder indicates it searches title and description
- Typing triggers search with short delay (debounce) OR on Enter (implementation choice)
- Clear (×) button appears when there is text
- Search applies in combination with filters and sort

### Advanced Filters

**Filter types**:
- **Status**: All / Pending / Completed
- **Priority**: Any / High / Medium / Low
- **Tags**: multi-select tag chips (filter by one tag at a time or multiple; see assumptions)
- **Due date range**: start + end date

**Behavior**:
- Filters are clearly visible and editable
- Active filters show a compact summary (chips) with per-filter clear action
- Clear filters resets to default view

**Backend integration constraint**:
- The filter UI MUST map to backend list endpoint query parameters described in `/specs/api/rest-endpoints.md`.

### Sort Dropdown

**Sort fields** (labels user-friendly):
- Created date (newest first / oldest first)
- Due date (soonest first / latest first)
- Priority (high to low / low to high)

**Behavior**:
- Changing sort updates the list immediately

---

## TaskCard Component

**Purpose**: represent one task and allow quick actions.

**Card Layout (at a glance)**:
- Left/top: completion checkbox
- Title (primary text)
- Priority badge (color-coded)
- Tags chips (wrap to new line when needed)
- Due date display
- Right/top actions:
  - Edit icon
  - Delete icon

### Priority Badge (Color)

- High: emphasize with danger-like accent (use red family)
- Medium: neutral accent (blue or gray)
- Low: subdued accent (green/gray)

### Due Date

- Display format: readable date + optional time
- If overdue:
  - Due date text turns **danger red**
  - Optional “Overdue” label

### Title & Long Text Handling

- Title should wrap up to 2 lines, then truncate
- Description is not shown fully on card (optional preview)

### Actions

- **Complete checkbox**:
  - Toggling immediately updates completion state
  - Completed tasks visually subdued (reduced contrast, optional strike-through)
- **Edit**:
  - Opens Add/Edit Task modal pre-filled
- **Delete**:
  - Shows confirmation dialog
  - Confirm deletes task

---

## AddTaskModal (Create / Edit Task)

**Purpose**: full-feature task form.

**Triggering**:
- “Add Task” button opens in create mode
- “Edit” icon opens in edit mode

### Modal Structure

- Title: “Add Task” (create) / “Edit Task” (edit)
- Form fields
- Primary CTA: Save / Create
- Secondary CTA: Cancel

### Form Fields

1. **Title**
   - Single-line input
   - Required
   - Maximum length aligned with backend constraints (see `/specs/api/rest-endpoints.md`)
   - Includes **microphone button** for voice input

2. **Description**
   - Multi-line textarea
   - Optional

3. **Priority**
   - Select with options:
     - High (red)
     - Medium
     - Low

4. **Tags**
   - Multi-select / chip input
   - User can type and press Enter to add a chip
   - Chips are removable

5. **Due Date**
   - Date picker
   - Optional
   - Must support clearing

6. **Recurring Option (Optional)**
   - Simple toggle: “Recurring”
   - If enabled, allow choosing frequency (daily/weekly/monthly)
   - If recurrence is not supported by backend yet, this field must be visually marked as “coming soon” or disabled (implementation choice)

### Voice Input (Microphone)

**User-visible behavior**:
- Clicking microphone:
  - Requests microphone permission if not already granted
  - Starts listening and shows clear visual indicator (e.g., pulsing mic)
- Recognized speech populates the **Title** field
- If recognition fails or times out:
  - Show a non-blocking error message
  - Allow retry
- User can always type manually

---

## Landing / Home Page (Unauthenticated)

**Purpose**: marketing-style entry point.

**Sections**:
- Hero:
  - Product name + short value statement
  - Primary CTA: Sign up
  - Secondary CTA: Sign in
- Feature highlights:
  - Multi-user secure tasks
  - Advanced filters and sorting
  - Urdu + RTL support
  - Voice-assisted task creation

**Behavior**:
- If already authenticated, visiting landing should redirect to dashboard/tasks

---

## Login / Signup Pages

### Auth Card Layout

**Purpose**: professional, centered authentication UI.

**Layout**:
- Centered card on neutral background
- Clear title: “Sign in” / “Create account”
- Email + password inputs
- Primary submit button
- Secondary links:
  - From login: “Create an account”
  - From signup: “Already have an account? Sign in”

### Validation Requirements

- Required field validation shown inline
- Friendly error text for invalid credentials
- Submit button shows loading state while authenticating

---

## Assumptions

- The UI supports both LTR and RTL layouts based on selected language.
- Tasks support: title, description, priority, tags, due date, completed status (as described in `/specs/api/rest-endpoints.md`).
- Recurring tasks may be treated as optional/preview capability depending on backend support.

---

## Acceptance Checklist (UI-level)

- User can navigate Tasks / Settings / Logout from sidebar
- User can switch theme (light/dark) and preference persists
- User can switch language (EN/اردو) and RTL is applied in Urdu
- User can search, filter, and sort tasks via the TaskList controls
- TaskCard displays priority, tags, due date (with overdue highlighting) and supports complete/edit/delete
- AddTaskModal supports voice title input and graceful error handling
- Unauthenticated users see Landing page with CTAs; authenticated users see dashboard
