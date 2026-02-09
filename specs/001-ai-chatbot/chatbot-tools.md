# Chatbot MCP Tools Specification

**Feature**: AI Todo Chatbot Integration
**Branch**: `001-ai-chatbot`
**Created**: 2026-02-09
**Status**: Draft

## Overview

This document defines all Model Context Protocol (MCP) tools that the AI chatbot can invoke to perform task management operations and retrieve user information. Each tool includes parameter definitions, return values, error handling, and natural language examples in both English and Urdu.

## MCP Tool Architecture

### Tool Execution Flow

```
1. User sends natural language message
2. Cohere (via OpenAI SDK) analyzes message and detects intent
3. Cohere selects appropriate MCP tool(s) to invoke
4. Backend executes tool with extracted parameters
5. Tool performs operation (database query/update)
6. Tool returns structured result
7. Cohere formats result into natural language response
8. Response sent back to user
```

### Tool Design Principles

- **User-Scoped**: All tools operate within authenticated user's scope
- **Idempotent**: Tools can be safely retried without side effects (where applicable)
- **Validated**: All parameters validated before execution
- **Structured Results**: Return consistent JSON structures
- **Error Handling**: Clear error messages for all failure scenarios

## Tool Definitions

### 1. add_task

**Purpose**: Create a new task in the user's account

**Intent Patterns** (English):
- "Add a task to [task title]"
- "Create a task: [task title]"
- "New task: [task title]"
- "I need to [task title]"
- "Remind me to [task title]"
- "Create a [priority] priority task to [task title]"
- "Add task [task title] due [date]"

**Intent Patterns** (Urdu):
- "ٹاسک شامل کریں: [task title]"
- "نیا کام: [task title]"
- "مجھے یاد دلائیں: [task title]"
- "[تاریخ] تک [task title] کا کام شامل کریں"

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| title | string | Yes | - | Task title (max 200 chars) |
| description | string | No | "" | Task description (max 1000 chars) |
| priority | enum | No | "medium" | Priority level: "low", "medium", "high" |
| due_date | string | No | null | Due date in ISO format (YYYY-MM-DD) |
| user_id | integer | Yes | from JWT | User ID from JWT token |

**Return Value**:

```json
{
  "success": true,
  "task": {
    "id": 123,
    "title": "Buy groceries",
    "description": "",
    "status": "pending",
    "priority": "medium",
    "due_date": null,
    "created_at": "2026-02-09T10:30:00Z"
  },
  "message": "Task created successfully"
}
```

**Error Responses**:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_TITLE",
    "message": "Task title cannot be empty",
    "details": "Please provide a task title"
  }
}
```

**Error Codes**:
- `INVALID_TITLE`: Title is empty or exceeds max length
- `INVALID_PRIORITY`: Priority is not one of: low, medium, high
- `INVALID_DATE`: Due date format is invalid
- `DATABASE_ERROR`: Database operation failed

**Natural Language Examples**:

English:
- Input: "Add a task to buy milk"
  - Extracted: title="buy milk", priority="medium"
  - Response: "I've created a task 'buy milk' with ID 45. It's set to medium priority."

- Input: "Create a high priority task to finish the report by Friday"
  - Extracted: title="finish the report", priority="high", due_date="2026-02-14"
  - Response: "I've created a high priority task 'finish the report' (ID 46) due on Friday, February 14th."

Urdu:
- Input: "ٹاسک شامل کریں: دودھ خریدنا"
  - Extracted: title="دودھ خریدنا", priority="medium"
  - Response: "میں نے 'دودھ خریدنا' کا کام بنا دیا ہے (ID 45)۔"

---

### 2. list_tasks

**Purpose**: Retrieve all tasks or filtered tasks for the user

**Intent Patterns** (English):
- "Show me all my tasks"
- "List my tasks"
- "What are my tasks?"
- "Show incomplete tasks"
- "List high priority tasks"
- "What tasks do I have?"

**Intent Patterns** (Urdu):
- "میرے تمام کام دکھاؤ"
- "میری ٹاسک لسٹ"
- "نامکمل کام دکھاؤ"
- "اہم کام کون سے ہیں؟"

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| status_filter | enum | No | null | Filter by status: "pending", "in_progress", "completed", or null for all |
| priority_filter | enum | No | null | Filter by priority: "low", "medium", "high", or null for all |
| user_id | integer | Yes | from JWT | User ID from JWT token |

**Return Value**:

```json
{
  "success": true,
  "tasks": [
    {
      "id": 123,
      "title": "Buy groceries",
      "description": "",
      "status": "pending",
      "priority": "medium",
      "due_date": null,
      "created_at": "2026-02-09T10:30:00Z"
    },
    {
      "id": 124,
      "title": "Finish report",
      "description": "Q4 financial report",
      "status": "in_progress",
      "priority": "high",
      "due_date": "2026-02-14",
      "created_at": "2026-02-09T11:00:00Z"
    }
  ],
  "count": 2,
  "message": "Retrieved 2 tasks"
}
```

**Error Responses**:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILTER",
    "message": "Invalid status filter",
    "details": "Status must be one of: pending, in_progress, completed"
  }
}
```

**Error Codes**:
- `INVALID_FILTER`: Invalid status or priority filter value
- `DATABASE_ERROR`: Database query failed

**Natural Language Examples**:

English:
- Input: "Show me all my tasks"
  - Extracted: status_filter=null, priority_filter=null
  - Response: "You have 5 tasks: 1) Buy groceries (pending, medium), 2) Finish report (in_progress, high), ..."

- Input: "List my incomplete tasks"
  - Extracted: status_filter="pending"
  - Response: "You have 3 incomplete tasks: 1) Buy groceries (ID 123), 2) Call dentist (ID 125), ..."

Urdu:
- Input: "میرے تمام کام دکھاؤ"
  - Extracted: status_filter=null
  - Response: "آپ کے 5 کام ہیں: 1) دودھ خریدنا (زیر التواء، درمیانی)، 2) رپورٹ مکمل کریں (جاری، اہم)، ..."

---

### 3. complete_task

**Purpose**: Mark a task as completed

**Intent Patterns** (English):
- "Mark task [id] as done"
- "Complete task [id]"
- "Finish task [id]"
- "Task [id] is done"
- "I completed task [id]"

**Intent Patterns** (Urdu):
- "ٹاسک [id] مکمل کریں"
- "کام [id] ہو گیا"
- "ٹاسک [id] ختم کریں"

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| task_id | integer | Yes | - | ID of the task to complete |
| user_id | integer | Yes | from JWT | User ID from JWT token |

**Return Value**:

```json
{
  "success": true,
  "task": {
    "id": 123,
    "title": "Buy groceries",
    "status": "completed",
    "completed_at": "2026-02-09T15:30:00Z"
  },
  "message": "Task marked as completed"
}
```

**Error Responses**:

```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 999 not found",
    "details": "Please check the task ID and try again"
  }
}
```

**Error Codes**:
- `TASK_NOT_FOUND`: Task ID does not exist or belongs to another user
- `ALREADY_COMPLETED`: Task is already marked as completed
- `INVALID_TASK_ID`: Task ID is not a valid integer
- `DATABASE_ERROR`: Database update failed

**Natural Language Examples**:

English:
- Input: "Mark task 123 as done"
  - Extracted: task_id=123
  - Response: "Great! I've marked task 123 'Buy groceries' as completed."

- Input: "Complete task 999"
  - Extracted: task_id=999
  - Response: "I couldn't find task 999 in your account. Please check the task ID."

Urdu:
- Input: "ٹاسک 123 مکمل کریں"
  - Extracted: task_id=123
  - Response: "بہترین! میں نے ٹاسک 123 'دودھ خریدنا' مکمل کر دیا ہے۔"

---

### 4. delete_task

**Purpose**: Delete a task from the user's account

**Intent Patterns** (English):
- "Delete task [id]"
- "Remove task [id]"
- "Delete the [task title] task"
- "Get rid of task [id]"
- "Cancel task [id]"

**Intent Patterns** (Urdu):
- "ٹاسک [id] حذف کریں"
- "کام [id] ہٹائیں"
- "[task title] کا کام حذف کریں"

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| task_id | integer | Yes | - | ID of the task to delete |
| user_id | integer | Yes | from JWT | User ID from JWT token |

**Return Value**:

```json
{
  "success": true,
  "task_id": 123,
  "message": "Task deleted successfully"
}
```

**Error Responses**:

```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 999 not found",
    "details": "The task may have already been deleted"
  }
}
```

**Error Codes**:
- `TASK_NOT_FOUND`: Task ID does not exist or belongs to another user
- `INVALID_TASK_ID`: Task ID is not a valid integer
- `DATABASE_ERROR`: Database deletion failed

**Natural Language Examples**:

English:
- Input: "Delete task 123"
  - Extracted: task_id=123
  - Response: "I've deleted task 123 'Buy groceries' from your account."

- Input: "Remove the grocery task"
  - Extracted: task_id=123 (resolved from title)
  - Response: "I've deleted the task 'Buy groceries' (ID 123)."

Urdu:
- Input: "ٹاسک 123 حذف کریں"
  - Extracted: task_id=123
  - Response: "میں نے ٹاسک 123 'دودھ خریدنا' حذف کر دیا ہے۔"

---

### 5. update_task

**Purpose**: Update properties of an existing task

**Intent Patterns** (English):
- "Update task [id] to [priority] priority"
- "Change task [id] priority to [priority]"
- "Set task [id] due date to [date]"
- "Update task [id] title to [new title]"
- "Change task [id] description to [new description]"

**Intent Patterns** (Urdu):
- "ٹاسک [id] کی ترجیح [priority] میں تبدیل کریں"
- "کام [id] کی تاریخ [date] پر سیٹ کریں"
- "ٹاسک [id] کا عنوان تبدیل کریں"

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| task_id | integer | Yes | - | ID of the task to update |
| title | string | No | - | New task title (max 200 chars) |
| description | string | No | - | New task description (max 1000 chars) |
| priority | enum | No | - | New priority: "low", "medium", "high" |
| due_date | string | No | - | New due date in ISO format (YYYY-MM-DD) |
| status | enum | No | - | New status: "pending", "in_progress", "completed" |
| user_id | integer | Yes | from JWT | User ID from JWT token |

**Return Value**:

```json
{
  "success": true,
  "task": {
    "id": 123,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "priority": "high",
    "due_date": "2026-02-10",
    "updated_at": "2026-02-09T16:00:00Z"
  },
  "message": "Task updated successfully"
}
```

**Error Responses**:

```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 999 not found",
    "details": "Please check the task ID and try again"
  }
}
```

**Error Codes**:
- `TASK_NOT_FOUND`: Task ID does not exist or belongs to another user
- `INVALID_TASK_ID`: Task ID is not a valid integer
- `INVALID_PRIORITY`: Priority is not one of: low, medium, high
- `INVALID_STATUS`: Status is not one of: pending, in_progress, completed
- `INVALID_DATE`: Due date format is invalid
- `NO_UPDATES`: No update parameters provided
- `DATABASE_ERROR`: Database update failed

**Natural Language Examples**:

English:
- Input: "Update task 123 to high priority"
  - Extracted: task_id=123, priority="high"
  - Response: "I've updated task 123 'Buy groceries' to high priority."

- Input: "Change task 123 due date to tomorrow"
  - Extracted: task_id=123, due_date="2026-02-10"
  - Response: "I've set the due date for task 123 'Buy groceries' to tomorrow (February 10th)."

Urdu:
- Input: "ٹاسک 123 کی ترجیح اہم میں تبدیل کریں"
  - Extracted: task_id=123, priority="high"
  - Response: "میں نے ٹاسک 123 'دودھ خریدنا' کی ترجیح اہم میں تبدیل کر دی ہے۔"

---

### 6. get_user_info

**Purpose**: Retrieve user information from JWT token

**Intent Patterns** (English):
- "What's my email?"
- "What is my email address?"
- "What's my name?"
- "Who am I?"
- "Show my account info"
- "What's my user ID?"

**Intent Patterns** (Urdu):
- "میری ای میل کیا ہے؟"
- "میرا نام کیا ہے؟"
- "میں کون ہوں؟"
- "میری معلومات دکھائیں"

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query_type | enum | Yes | - | Type of info: "email", "name", "user_id", "all" |
| user_id | integer | Yes | from JWT | User ID from JWT token |

**Return Value**:

```json
{
  "success": true,
  "user_info": {
    "user_id": 123,
    "email": "user@example.com",
    "name": "John Doe"
  },
  "message": "User information retrieved"
}
```

**Error Responses**:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_QUERY_TYPE",
    "message": "Invalid query type",
    "details": "Query type must be one of: email, name, user_id, all"
  }
}
```

**Error Codes**:
- `INVALID_QUERY_TYPE`: Query type is not recognized
- `TOKEN_INVALID`: JWT token is invalid or expired

**Natural Language Examples**:

English:
- Input: "What's my email?"
  - Extracted: query_type="email"
  - Response: "Your email address is: user@example.com"

- Input: "What's my name?"
  - Extracted: query_type="name"
  - Response: "Your name is: John Doe"

Urdu:
- Input: "میری ای میل کیا ہے؟"
  - Extracted: query_type="email"
  - Response: "آپ کا ای میل: user@example.com"

---

## Intent Mapping and Chaining

### Intent Detection Logic

The Cohere agent analyzes user messages to detect one of the following intents:

1. **add_task**: User wants to create a new task
2. **list_tasks**: User wants to see their tasks
3. **complete_task**: User wants to mark a task as done
4. **delete_task**: User wants to remove a task
5. **update_task**: User wants to modify a task
6. **get_user_info**: User wants to know their account information
7. **unknown**: User message doesn't match any known intent

### Parameter Extraction

For each detected intent, the agent extracts relevant parameters:

- **Task Title**: Extracted from phrases like "to [title]", "task: [title]", "[title] task"
- **Priority**: Extracted from keywords: "high", "urgent", "important" → high; "low" → low; default → medium
- **Due Date**: Extracted from phrases like "by [date]", "due [date]", "on [date]", "tomorrow", "next week"
- **Task ID**: Extracted from numbers following "task" keyword: "task 123" → 123

### Tool Chaining

Some user requests may require multiple tool invocations:

**Example 1: Create and List**
- Input: "Add a task to buy milk and show me all my tasks"
- Chain: add_task(title="buy milk") → list_tasks()
- Response: "I've created task 'buy milk' (ID 45). You now have 6 tasks: ..."

**Example 2: Update and Confirm**
- Input: "Change task 123 to high priority and mark it as in progress"
- Chain: update_task(task_id=123, priority="high", status="in_progress")
- Response: "I've updated task 123 'Buy groceries' to high priority and marked it as in progress."

**Example 3: Delete and List**
- Input: "Delete task 123 and show my remaining tasks"
- Chain: delete_task(task_id=123) → list_tasks()
- Response: "I've deleted task 123. You now have 5 remaining tasks: ..."

### Ambiguity Resolution

When user input is ambiguous, the agent should:

1. **Ask for Clarification**: "I found multiple tasks with 'grocery' in the title. Which one did you mean? Task 123 or Task 125?"
2. **Suggest Options**: "Did you want to mark task 123 as completed or delete it?"
3. **Use Context**: If previous message mentioned a task ID, use that ID for follow-up commands

## Agent Behavior Guidelines

### Response Tone

- **Friendly**: Use conversational language, not robotic
- **Concise**: Keep responses brief but informative
- **Helpful**: Provide actionable information
- **Consistent**: Maintain consistent tone across languages

### Error Handling

- **User-Friendly**: Translate technical errors into plain language
- **Actionable**: Tell users what they can do to fix the issue
- **Polite**: Never blame the user for errors

### Language Detection

- **Automatic**: Detect language from user input
- **Consistent**: Respond in the same language as the input
- **Mixed Language**: Handle code-switching gracefully

### Confirmation Messages

- **Task Created**: Include task ID and key details
- **Task Updated**: Confirm what changed
- **Task Deleted**: Confirm deletion with task title
- **Task Completed**: Celebrate completion

## Testing Scenarios

### English Test Cases

1. "Add a task to buy groceries" → add_task(title="buy groceries")
2. "Create a high priority task to finish report by Friday" → add_task(title="finish report", priority="high", due_date="2026-02-14")
3. "Show me all my tasks" → list_tasks()
4. "List my incomplete tasks" → list_tasks(status_filter="pending")
5. "Mark task 123 as done" → complete_task(task_id=123)
6. "Delete task 456" → delete_task(task_id=456)
7. "Update task 789 to high priority" → update_task(task_id=789, priority="high")
8. "What's my email?" → get_user_info(query_type="email")

### Urdu Test Cases

1. "ٹاسک شامل کریں: دودھ خریدنا" → add_task(title="دودھ خریدنا")
2. "میرے تمام کام دکھاؤ" → list_tasks()
3. "ٹاسک 123 مکمل کریں" → complete_task(task_id=123)
4. "کام 456 حذف کریں" → delete_task(task_id=456)
5. "ٹاسک 789 کی ترجیح اہم میں تبدیل کریں" → update_task(task_id=789, priority="high")
6. "میری ای میل کیا ہے؟" → get_user_info(query_type="email")

### Edge Case Test Cases

1. "Delete the task" (ambiguous - no task ID) → Ask for clarification
2. "Mark task 999 as done" (non-existent task) → Error: TASK_NOT_FOUND
3. "Add a task" (no title) → Error: INVALID_TITLE
4. "Update task 123 to super priority" (invalid priority) → Error: INVALID_PRIORITY
5. "What's the weather?" (out of scope) → Polite message explaining capabilities

## Cross-References

- **@specs/001-ai-chatbot/chatbot-architecture.md**: Overall system architecture
- **@specs/001-ai-chatbot/chatbot-frontend.md**: Frontend chat UI
- **@specs/api/rest-endpoints.md**: Existing Phase 2 task API endpoints
- **@specs/features/task-crud.md**: Task management functionality
