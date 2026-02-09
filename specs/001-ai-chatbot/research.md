# Research: AI Todo Chatbot Integration

**Feature**: AI Todo Chatbot Integration
**Branch**: `001-ai-chatbot`
**Date**: 2026-02-09

## Overview

This document consolidates research findings for implementing the Phase 3 AI chatbot feature, including technology decisions, best practices, and architectural patterns.

## Technology Decisions

### 1. OpenAI Agents SDK with Cohere API

**Decision**: Use OpenAI Agents SDK configured with Cohere as the LLM provider

**Rationale**:
- OpenAI Agents SDK provides a standardized interface for agent orchestration
- Cohere offers competitive pricing and performance for conversational AI
- SDK supports custom LLM providers via base URL configuration
- Enables easy switching between LLM providers if needed
- Cohere's Command-R-Plus model excels at tool use and multilingual support

**Implementation Pattern**:
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("COHERE_API_KEY"),
    base_url="https://api.cohere.ai/v1"
)

# Agent with MCP tools
response = client.chat.completions.create(
    model="command-r-plus",
    messages=[{"role": "user", "content": "Add task to buy milk"}],
    tools=[add_task_tool, list_tasks_tool, ...]
)
```

**Alternatives Considered**:
- Direct Cohere SDK: Less standardized, harder to switch providers
- LangChain: More complex, unnecessary overhead for our use case
- Custom agent implementation: Reinventing the wheel, higher maintenance

### 2. Model Context Protocol (MCP) for Tool Execution

**Decision**: Implement MCP tools for all task operations

**Rationale**:
- MCP provides standardized tool definition format
- Clear separation between intent detection and tool execution
- Tools are reusable and testable independently
- Aligns with industry best practices for LLM tool use
- Official MCP SDK provides validation and error handling

**Tool Structure**:
```python
{
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new task in the user's account",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]}
            },
            "required": ["title"]
        }
    }
}
```

**Best Practices**:
- Keep tool descriptions clear and concise
- Use JSON Schema for parameter validation
- Return structured responses for consistent parsing
- Include error codes for different failure scenarios
- Validate user_id in every tool to enforce isolation

### 3. Stateless Chat Architecture

**Decision**: Implement stateless chat endpoint with database-backed conversation history

**Rationale**:
- Enables horizontal scaling of backend servers
- No server-side session management complexity
- Conversation history persists across server restarts
- Aligns with microservices best practices
- Simplifies deployment and load balancing

**Architecture Pattern**:
```
Request → JWT Validation → Load History from DB → Process with LLM →
Save to DB → Return Response
```

**Key Principles**:
- Each request is self-contained
- User context derived from JWT token
- No in-memory state between requests
- Conversation history loaded on-demand
- Limit history to recent messages for performance

**Alternatives Considered**:
- Stateful sessions: Doesn't scale horizontally, complex state management
- Redis caching: Adds dependency, still needs DB for persistence
- WebSocket connections: Overkill for request-response pattern

### 4. Web Speech API for Voice Input

**Decision**: Use browser-native Web Speech API for voice transcription

**Rationale**:
- No additional backend dependencies or costs
- Works offline (transcription happens in browser)
- Good accuracy for English and Urdu
- Simple JavaScript API
- Supported in major browsers (Chrome, Edge, Safari)

**Implementation Pattern**:
```javascript
const recognition = new webkitSpeechRecognition();
recognition.lang = 'en-US'; // or 'ur-PK' for Urdu
recognition.continuous = false;
recognition.interimResults = false;

recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;
  sendMessage(transcript);
};

recognition.start();
```

**Browser Compatibility**:
- Chrome 90+: Full support (English + Urdu)
- Edge 90+: Full support (English + Urdu)
- Safari 14.1+: Partial support (English only, limited Urdu)
- Firefox: Not supported (graceful degradation)

**Fallback Strategy**: Hide voice button in unsupported browsers

**Alternatives Considered**:
- Backend speech-to-text (Google Cloud, AWS): Adds cost and latency
- Third-party libraries: Unnecessary complexity
- Custom ML model: Too complex for this scope

### 5. Urdu Language Support with RTL Layout

**Decision**: Use CSS direction property and Unicode detection for RTL layout

**Rationale**:
- CSS `dir="rtl"` provides automatic RTL layout
- Unicode range detection (U+0600-U+06FF) identifies Urdu text
- Browser fonts handle Urdu rendering automatically
- next-intl provides i18n infrastructure (already in Phase 2)
- No additional dependencies required

**Implementation Pattern**:
```javascript
const isUrdu = (text) => /[\u0600-\u06FF]/.test(text);

const messageStyle = {
  direction: isUrdu(message.text) ? 'rtl' : 'ltr',
  textAlign: isUrdu(message.text) ? 'right' : 'left'
};
```

**Font Stack**:
```css
font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq',
             'Arabic Typesetting', sans-serif;
```

**Best Practices**:
- Detect language per message (not per conversation)
- Apply RTL to message bubbles, not entire chat window
- Use system fonts for better performance
- Test with mixed English/Urdu messages

### 6. Database Schema for Conversation History

**Decision**: Two-table design (conversations, chat_messages) with user_id foreign keys

**Rationale**:
- Separates conversation metadata from message content
- Enables efficient querying by conversation
- Supports future features (conversation titles, archiving)
- Enforces user isolation at database level
- Aligns with normalized database design

**Schema Design**:
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP,
    last_activity_at TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_last_activity (last_activity_at)
);

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    user_id INTEGER REFERENCES users(id),
    sender VARCHAR(10) CHECK (sender IN ('user', 'bot')),
    message_text TEXT,
    created_at TIMESTAMP,
    metadata JSONB,
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

**Performance Optimizations**:
- Indexes on user_id for fast user-scoped queries
- Index on conversation_id for message retrieval
- Index on created_at for chronological ordering
- Limit queries to 100 most recent messages

**Alternatives Considered**:
- Single table: Denormalized, harder to query conversations
- NoSQL (MongoDB): Overkill, adds complexity, violates constitution
- Message queue: Not needed for request-response pattern

## Integration Patterns

### JWT Token Validation and User Isolation

**Pattern**: Extract user_id from JWT token and validate against URL parameter

```python
def validate_user_access(token: str, url_user_id: int) -> dict:
    """Validate JWT and ensure user_id matches URL"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        token_user_id = payload.get("user_id")

        if token_user_id != url_user_id:
            raise HTTPException(status_code=403, detail="User ID mismatch")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Best Practices**:
- Always validate token signature and expiration
- Compare token user_id with URL user_id
- Return 401 for auth errors, 403 for authorization errors
- Never trust URL parameters alone

### Intent Detection and Parameter Extraction

**Pattern**: Use Cohere's tool use capability for intent detection

```python
def detect_intent(user_message: str, conversation_history: list) -> dict:
    """Detect intent and extract parameters from user message"""
    messages = conversation_history + [
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="command-r-plus",
        messages=messages,
        tools=MCP_TOOLS,
        tool_choice="auto"
    )

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        return {
            "intent": tool_call.function.name,
            "parameters": json.loads(tool_call.function.arguments)
        }
    else:
        return {"intent": "unknown", "parameters": {}}
```

**Error Handling**:
- Handle API rate limits with exponential backoff
- Catch JSON parsing errors in tool arguments
- Provide fallback responses for unknown intents
- Log all API errors for debugging

### Conversation History Management

**Pattern**: Load recent history, append new messages, limit size

```python
def get_conversation_history(conversation_id: str, user_id: int) -> list:
    """Load recent conversation history for context"""
    messages = db.query(ChatMessage)\
        .filter(ChatMessage.conversation_id == conversation_id)\
        .filter(ChatMessage.user_id == user_id)\
        .order_by(ChatMessage.created_at.desc())\
        .limit(100)\
        .all()

    return [
        {
            "role": "user" if msg.sender == "user" else "assistant",
            "content": msg.message_text
        }
        for msg in reversed(messages)
    ]
```

**Best Practices**:
- Limit to 100 most recent messages
- Order by created_at descending, then reverse
- Filter by user_id for security
- Cache within request scope (not across requests)

## Performance Considerations

### Response Time Optimization

**Target**: <3 seconds for 95th percentile

**Strategies**:
1. **Database Query Optimization**:
   - Use indexes on frequently queried columns
   - Limit conversation history to 100 messages
   - Use connection pooling (SQLAlchemy)

2. **API Call Optimization**:
   - Use async/await for I/O operations
   - Set reasonable timeouts (30 seconds)
   - Implement retry logic with exponential backoff

3. **Frontend Optimization**:
   - Show loading indicators immediately
   - Optimistic UI updates where possible
   - Lazy load chat component on first use

### Scalability Patterns

**Horizontal Scaling**: Stateless design enables multiple backend instances

**Load Balancing**: Round-robin or least-connections algorithm

**Database Connection Pooling**:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

**Rate Limiting**: Per-user limits to prevent abuse
```python
@limiter.limit("60/minute")
async def chat_endpoint(user_id: int, request: ChatRequest):
    ...
```

## Security Best Practices

### Input Sanitization

**SQL Injection Prevention**: Use SQLModel parameterized queries (automatic)

**XSS Prevention**: Sanitize message text before storing and displaying
```python
import bleach

def sanitize_message(text: str) -> str:
    """Remove potentially harmful HTML/JS"""
    return bleach.clean(text, tags=[], strip=True)
```

**Length Limits**: Enforce maximum message length (1000 characters)

### API Key Management

**Environment Variables**: Store Cohere API key in environment
```python
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set")
```

**Never Log Sensitive Data**: Exclude API keys and JWT tokens from logs

### Rate Limiting

**Per-User Limits**: 60 messages per minute per user

**Global Limits**: 1000 messages per minute across all users

**Cohere API Limits**: Respect Cohere's rate limits (varies by plan)

## Testing Strategy

### Unit Tests

**MCP Tools**: Test each tool independently with mock data
```python
def test_add_task_tool():
    result = add_task(
        title="Test task",
        priority="high",
        user_id=123
    )
    assert result["success"] == True
    assert result["task"]["title"] == "Test task"
```

**Intent Parser**: Test intent detection with various phrasings
```python
def test_intent_detection():
    intent = detect_intent("Add a task to buy milk", [])
    assert intent["intent"] == "add_task"
    assert "buy milk" in intent["parameters"]["title"]
```

### Integration Tests

**Chat Endpoint**: Test full request-response flow
```python
def test_chat_endpoint():
    response = client.post(
        "/api/123/chat",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"message": "Add task to buy milk"}
    )
    assert response.status_code == 200
    assert "created" in response.json()["response"].lower()
```

**User Isolation**: Verify users can't access other users' data
```python
def test_user_isolation():
    response = client.post(
        "/api/999/chat",  # Different user_id
        headers={"Authorization": f"Bearer {jwt_token_user_123}"},
        json={"message": "Show my tasks"}
    )
    assert response.status_code == 403
```

### Manual Testing

**Urdu Language**: Test with Urdu messages and verify RTL layout

**Voice Input**: Test with microphone in Chrome/Edge/Safari

**Error Scenarios**: Test with invalid tokens, network failures, API errors

## Deployment Considerations

### Environment Variables

**Backend**:
- `COHERE_API_KEY`: Cohere API key
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (existing)
- `CORS_ORIGINS`: Allowed frontend origins

**Frontend**:
- `NEXT_PUBLIC_API_URL`: Backend API base URL

### Database Migrations

**Alembic Migration**: Create conversations and chat_messages tables
```python
def upgrade():
    op.create_table(
        'conversations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_activity_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    # ... chat_messages table
```

### Monitoring and Logging

**Metrics to Track**:
- Chat endpoint response times (P50, P95, P99)
- Cohere API call success/failure rates
- Intent detection accuracy (manual review)
- User engagement (messages per user, conversations per day)

**Logging Strategy**:
- Log all API errors with stack traces
- Log slow requests (>3 seconds)
- Log intent detection results for analysis
- Never log JWT tokens or API keys

## Conclusion

All technology decisions are finalized and aligned with constitutional requirements. The research phase has resolved all technical unknowns and established clear implementation patterns. Ready to proceed to Phase 1 (Design & Contracts).
