# Chatbot Architecture Specification

**Feature**: AI Todo Chatbot Integration
**Branch**: `001-ai-chatbot`
**Created**: 2026-02-09
**Status**: Draft

## Overview

This document defines the complete architecture for the Phase 3 AI Todo Chatbot, including the data flow from frontend to backend, integration with Cohere via OpenAI Agents SDK, MCP tool execution, and database persistence.

## Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                       │
├─────────────────────────────────────────────────────────────────┤
│  Dashboard Page                                                  │
│  ├─ Floating Chat Icon (bottom-right)                          │
│  └─ Chat Window Component                                       │
│     ├─ Message History Display                                 │
│     ├─ Text Input Field                                        │
│     └─ Voice Input Button (Web Speech API)                     │
│                                                                  │
│  HTTP POST /api/{user_id}/chat                                 │
│  Headers: Authorization: Bearer {JWT}                           │
│  Body: { message: "Add task to buy milk", conversation_id }    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
├─────────────────────────────────────────────────────────────────┤
│  POST /api/{user_id}/chat Endpoint                             │
│  ├─ JWT Token Validation                                       │
│  ├─ User ID Extraction from Token                              │
│  ├─ User ID Validation (URL vs Token)                          │
│  └─ Request Forwarding to Chat Service                         │
│                              ↓                                   │
│  Chat Service (Orchestrator)                                    │
│  ├─ Load Conversation History from DB                          │
│  ├─ Prepare Context for Agent                                  │
│  └─ Call OpenAI Agents SDK                                     │
│                              ↓                                   │
│  OpenAI Agents SDK (configured with Cohere)                    │
│  ├─ Natural Language Understanding                             │
│  ├─ Intent Detection (add_task, list_tasks, etc.)             │
│  ├─ Parameter Extraction                                       │
│  └─ MCP Tool Selection & Execution                            │
│                              ↓                                   │
│  MCP Tools (Model Context Protocol)                            │
│  ├─ add_task(title, description, priority, due_date)          │
│  ├─ list_tasks(status_filter)                                 │
│  ├─ complete_task(task_id)                                    │
│  ├─ delete_task(task_id)                                      │
│  ├─ update_task(task_id, updates)                            │
│  └─ get_user_info(query_type)                                │
│                              ↓                                   │
│  Task CRUD Operations (Existing Phase 2 API)                   │
│  └─ Database Operations on Tasks Table                         │
│                              ↓                                   │
│  Response Generation                                            │
│  ├─ Format Tool Results                                       │
│  ├─ Generate Natural Language Response                        │
│  └─ Persist Message to DB                                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (Neon PostgreSQL)                    │
├─────────────────────────────────────────────────────────────────┤
│  conversations                                                   │
│  ├─ id (UUID, PK)                                              │
│  ├─ user_id (FK → users.id)                                   │
│  ├─ created_at (timestamp)                                     │
│  └─ last_activity_at (timestamp)                               │
│                                                                  │
│  chat_messages                                                   │
│  ├─ id (UUID, PK)                                              │
│  ├─ conversation_id (FK → conversations.id)                   │
│  ├─ user_id (FK → users.id)                                   │
│  ├─ sender (enum: 'user', 'bot')                              │
│  ├─ message_text (text)                                       │
│  ├─ created_at (timestamp)                                     │
│  └─ metadata (jsonb, optional)                                │
│                                                                  │
│  tasks (Existing from Phase 2)                                  │
│  ├─ id (int, PK)                                               │
│  ├─ user_id (FK → users.id)                                   │
│  ├─ title (varchar)                                            │
│  ├─ description (text)                                         │
│  ├─ status (enum: pending, in_progress, completed)            │
│  ├─ priority (enum: low, medium, high)                        │
│  ├─ due_date (date, nullable)                                 │
│  ├─ created_at (timestamp)                                     │
│  └─ updated_at (timestamp)                                     │
│                                                                  │
│  users (Existing from Phase 2)                                  │
│  ├─ id (int, PK)                                               │
│  ├─ email (varchar, unique)                                    │
│  ├─ name (varchar)                                             │
│  └─ ... (other auth fields)                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Stateless Architecture Principles

### Request-Response Flow

1. **No In-Memory State**: Each chat request is completely independent
2. **JWT-Based Context**: All user context derived from JWT token claims
3. **Database-Backed History**: Conversation history loaded from database on each request
4. **Self-Contained Requests**: Each request includes all necessary information (message, conversation_id, JWT)

### Conversation Management

- **Conversation Creation**: First message from a user creates a new conversation record
- **Conversation Retrieval**: Subsequent messages reference existing conversation_id
- **History Loading**: Most recent 100 messages loaded for context
- **No Session State**: No server-side session storage or caching

## Database Models

### Conversation Model

**Purpose**: Track chat sessions between users and the chatbot

**Attributes**:
- `id`: Unique identifier (UUID)
- `user_id`: Foreign key to users table
- `created_at`: Timestamp when conversation started
- `last_activity_at`: Timestamp of most recent message

**Relationships**:
- One-to-Many with ChatMessage (one conversation has many messages)
- Many-to-One with User (many conversations belong to one user)

**Indexes**:
- Primary key on `id`
- Index on `user_id` for efficient user conversation lookup
- Index on `last_activity_at` for sorting by recency

### ChatMessage Model

**Purpose**: Store individual messages in conversations

**Attributes**:
- `id`: Unique identifier (UUID)
- `conversation_id`: Foreign key to conversations table
- `user_id`: Foreign key to users table (for user isolation)
- `sender`: Enum ('user', 'bot') indicating message source
- `message_text`: The actual message content
- `created_at`: Timestamp when message was sent
- `metadata`: Optional JSON field for additional data (intent, tool results, etc.)

**Relationships**:
- Many-to-One with Conversation (many messages belong to one conversation)
- Many-to-One with User (many messages belong to one user)

**Indexes**:
- Primary key on `id`
- Index on `conversation_id` for efficient message retrieval
- Index on `user_id` for user isolation enforcement
- Index on `created_at` for chronological ordering

### Task Model (Existing from Phase 2)

**Purpose**: Store user tasks (reused from Phase 2)

**Attributes**:
- `id`: Unique identifier (integer)
- `user_id`: Foreign key to users table
- `title`: Task title
- `description`: Task description
- `status`: Enum (pending, in_progress, completed)
- `priority`: Enum (low, medium, high)
- `due_date`: Optional due date
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

**Note**: This model is not modified in Phase 3, only accessed via MCP tools

### User Model (Existing from Phase 2)

**Purpose**: Store user accounts and authentication data

**Note**: This model is not modified in Phase 3. User information is retrieved from JWT tokens, not database queries.

## JWT User Isolation

### Token Structure

The JWT token contains user claims that are used for all operations:

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Isolation Enforcement

1. **URL Parameter Validation**: The `user_id` in the URL path must match the `user_id` in the JWT token
2. **Database Queries**: All database queries filter by `user_id` from JWT token
3. **MCP Tool Context**: User ID is passed to all MCP tools for scoped operations
4. **No Cross-User Access**: Any attempt to access another user's data returns 403 Forbidden

### Token Validation Flow

```
1. Extract JWT from Authorization header
2. Verify JWT signature and expiration
3. Extract user_id from JWT claims
4. Compare JWT user_id with URL user_id
5. If mismatch: return 403 Forbidden
6. If match: proceed with request using JWT user_id for all operations
```

## Cohere API Integration

### OpenAI Agents SDK Configuration

The OpenAI Agents SDK is configured to use Cohere as the LLM provider:

```python
# Conceptual configuration (not actual implementation code)
agent = Agent(
    model="command-r-plus",  # Cohere model
    api_key=os.getenv("COHERE_API_KEY"),
    base_url="https://api.cohere.ai/v1",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task, get_user_info]
)
```

### API Key Management

- **Environment Variable**: `COHERE_API_KEY` stored in backend environment
- **Security**: Never exposed to frontend or logs
- **Validation**: Checked at application startup
- **Error Handling**: Graceful degradation if API key is invalid or quota exceeded

### Request Flow to Cohere

1. User message received at backend
2. Conversation history loaded from database
3. Context prepared with user message + history
4. Request sent to Cohere via OpenAI SDK
5. Cohere analyzes message and determines intent
6. Cohere selects appropriate MCP tool(s) to execute
7. Tool results returned to Cohere
8. Cohere generates natural language response
9. Response returned to backend
10. Response persisted to database and sent to frontend

## Agent Orchestration

### Specialized Agents (Reusable Intelligence)

The Phase 3 implementation uses five specialized agents:

1. **chatbot-orchestrator**: Main control flow, coordinates all other agents
2. **intent-parser**: Parses natural language to detect intent and extract parameters
3. **mcp-tool-executor**: Executes MCP tools and handles tool results
4. **chatbot-frontend-integrator**: Generates frontend chat UI components
5. **chatbot-api-tester**: Tests chat API endpoints and validates functionality

### Agent Coordination

- **Sequential Execution**: Agents are invoked in order based on task requirements
- **Context Passing**: Each agent receives context from previous agents
- **Error Propagation**: Errors from any agent halt the pipeline and return to user
- **Logging**: All agent actions logged for debugging and monitoring

## Error Handling

### Error Categories

1. **Authentication Errors**: Invalid or expired JWT token → 401 Unauthorized
2. **Authorization Errors**: User ID mismatch → 403 Forbidden
3. **Validation Errors**: Invalid message format or parameters → 400 Bad Request
4. **Not Found Errors**: Task or conversation not found → 404 Not Found
5. **API Errors**: Cohere API failure → 503 Service Unavailable
6. **Database Errors**: Database connection or query failure → 500 Internal Server Error

### Error Response Format

```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "The task with ID 999 was not found in your account.",
    "details": "Please check the task ID and try again."
  }
}
```

### User-Friendly Error Messages

- **Task Not Found**: "I couldn't find that task. Please check the task ID and try again."
- **Invalid Priority**: "I didn't recognize that priority level. Please use 'low', 'medium', or 'high'."
- **Token Expired**: "Your session has expired. Please log in again."
- **API Quota Exceeded**: "I'm experiencing high demand right now. Please try again in a moment."

## Performance Considerations

### Response Time Targets

- **Chat Message Processing**: < 3 seconds (95th percentile)
- **Conversation History Loading**: < 500ms
- **Database Queries**: < 100ms per query
- **Cohere API Calls**: < 2 seconds (depends on Cohere SLA)

### Optimization Strategies

1. **History Limiting**: Load only 100 most recent messages
2. **Database Indexing**: Proper indexes on user_id, conversation_id, created_at
3. **Connection Pooling**: Reuse database connections
4. **Async Processing**: Use async/await for I/O operations
5. **Caching**: Cache user JWT claims for request duration (not across requests)

### Scalability

- **Stateless Design**: Enables horizontal scaling of backend servers
- **Database Connection Pooling**: Efficient database resource usage
- **Rate Limiting**: Prevent abuse and ensure fair usage
- **Load Balancing**: Distribute requests across multiple backend instances

## Security Considerations

### Input Sanitization

- **SQL Injection Prevention**: Use parameterized queries (SQLModel handles this)
- **XSS Prevention**: Sanitize message text before storing and displaying
- **Command Injection**: Validate all user input before processing
- **Length Limits**: Enforce maximum message length (1000 characters)

### Data Privacy

- **User Isolation**: Strict enforcement of user-scoped data access
- **JWT Validation**: Every request validates token signature and expiration
- **No Logging of Sensitive Data**: Never log JWT tokens or user messages in plain text
- **HTTPS Only**: All API communication over encrypted connections

### Rate Limiting

- **Per-User Limits**: Maximum 60 messages per minute per user
- **Global Limits**: Maximum 1000 messages per minute across all users
- **Cohere API Limits**: Respect Cohere's rate limits and quotas
- **Backoff Strategy**: Exponential backoff on rate limit errors

## Monitoring and Logging

### Metrics to Track

- **Request Volume**: Messages per minute/hour/day
- **Response Times**: P50, P95, P99 latencies
- **Error Rates**: Percentage of failed requests by error type
- **Cohere API Usage**: API calls, tokens consumed, quota remaining
- **Database Performance**: Query times, connection pool usage

### Logging Strategy

- **Request Logging**: Log all incoming requests with user_id, timestamp, message length
- **Error Logging**: Log all errors with stack traces and context
- **Tool Execution Logging**: Log which MCP tools are invoked and their results
- **Performance Logging**: Log slow requests (>3 seconds)

### Alerting

- **High Error Rate**: Alert if error rate exceeds 5%
- **Slow Responses**: Alert if P95 latency exceeds 5 seconds
- **API Quota**: Alert when Cohere quota reaches 80%
- **Database Issues**: Alert on connection failures or slow queries

## Deployment Architecture

### Backend Deployment

- **Platform**: Render, Railway, or similar PaaS
- **Environment Variables**: COHERE_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET
- **Health Checks**: /health endpoint for load balancer monitoring
- **Auto-Scaling**: Scale based on CPU and memory usage

### Frontend Deployment

- **Platform**: Vercel (existing Phase 2 deployment)
- **Environment Variables**: NEXT_PUBLIC_API_URL
- **CDN**: Static assets served via Vercel CDN
- **Edge Functions**: Not required for Phase 3

### Database Deployment

- **Platform**: Neon.tech (existing Phase 2 database)
- **Migrations**: Run database migrations to add conversations and chat_messages tables
- **Backups**: Automated daily backups
- **Connection Pooling**: Use Neon's connection pooling feature

## Cross-References

- **@specs/001-ai-chatbot/chatbot-tools.md**: MCP tool definitions and contracts
- **@specs/001-ai-chatbot/chatbot-frontend.md**: Frontend chat UI components
- **@specs/api/rest-endpoints.md**: Existing Phase 2 API endpoints
- **@specs/database/schema.md**: Database schema including new tables
- **@specs/features/authentication.md**: JWT token structure and validation
