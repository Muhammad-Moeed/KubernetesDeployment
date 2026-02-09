# Quick Start Guide - Phase 3 AI Chatbot Backend

## Backend Components Implemented (T011-T015)

### Files Created

```
backend/
├── services/
│   ├── __init__.py              # Services package
│   ├── mcp_tools.py             # MCP tools (add_task, list_tasks, get_user_info)
│   ├── intent_parser.py         # Cohere-based intent detection
│   └── chat_service.py          # Chat orchestration service
├── routes/
│   └── chat.py                  # Chat API endpoints
└── main.py                      # Updated with chat router

Total: ~1,270 lines of new code
```

### API Endpoints

#### 1. Send Chat Message
```bash
POST /api/{user_id}/chat
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-uuid"
}

Response:
{
  "response": "I've created a task 'buy groceries' with ID 45.",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "add_task",
  "success": true,
  "language": "en"
}
```

#### 2. Get Conversation History
```bash
GET /api/{user_id}/chat/history/{conversation_id}
Authorization: Bearer {jwt_token}

Response:
{
  "success": true,
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "id": "msg-uuid",
      "sender": "user",
      "message": "Add a task to buy milk",
      "timestamp": "2026-02-09T10:30:00Z"
    },
    {
      "id": "msg-uuid",
      "sender": "bot",
      "message": "I've created a task 'buy milk' with ID 45.",
      "timestamp": "2026-02-09T10:30:02Z"
    }
  ],
  "count": 2
}
```

## Testing the Backend

### 1. Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Test with curl

```bash
# Get a JWT token first (use existing Phase 2 auth)
export JWT_TOKEN="your_jwt_token_here"
export USER_ID="your_user_id_here"

# Test chat endpoint
curl -X POST http://localhost:8000/api/$USER_ID/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'

# Test with Urdu
curl -X POST http://localhost:8000/api/$USER_ID/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "ٹاسک شامل کریں: دودھ خریدنا"}'

# List tasks
curl -X POST http://localhost:8000/api/$USER_ID/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all my tasks"}'

# Get user info
curl -X POST http://localhost:8000/api/$USER_ID/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my email?"}'
```

### 3. Test with API Documentation

Visit: http://localhost:8000/docs

Look for the "chat" section with two endpoints:
- POST /api/{user_id}/chat
- GET /api/{user_id}/chat/history/{conversation_id}

## Environment Variables Required

```env
# Existing from Phase 2
DATABASE_URL=postgresql://user:pass@host:port/dbname
BETTER_AUTH_SECRET=your_secret_key

# New for Phase 3
COHERE_API_KEY=your_cohere_api_key_here
```

Get your Cohere API key from: https://dashboard.cohere.com/api-keys

## Supported Intents

1. **add_task**: Create new tasks
   - "Add a task to buy groceries"
   - "Create a high priority task to finish report"
   - "ٹاسک شامل کریں: دودھ خریدنا"

2. **list_tasks**: List user tasks
   - "Show me all my tasks"
   - "List my incomplete tasks"
   - "میرے تمام کام دکھاؤ"

3. **get_user_info**: Get user information
   - "What's my email?"
   - "What's my name?"
   - "میری ای میل کیا ہے؟"

4. **complete_task**: Mark task as done (Coming in User Story 2)
5. **delete_task**: Delete task (Coming in User Story 2)
6. **update_task**: Update task (Coming in User Story 2)

## Architecture

```
User Message → JWT Auth → Intent Parser (Cohere) → MCP Tool → Database → Response
```

### Key Components

1. **Intent Parser** (`services/intent_parser.py`)
   - Uses Cohere command-r-plus model
   - Detects intent and extracts parameters
   - Supports English and Urdu

2. **MCP Tools** (`services/mcp_tools.py`)
   - add_task: Creates tasks with validation
   - list_tasks: Retrieves filtered tasks
   - get_user_info: Extracts info from JWT

3. **Chat Service** (`services/chat_service.py`)
   - Orchestrates the entire flow
   - Manages conversations
   - Persists messages to database

4. **Chat Routes** (`routes/chat.py`)
   - REST API endpoints
   - JWT authentication
   - User isolation enforcement

## Database Tables Used

### Existing (Phase 2)
- `tasks`: Task storage
- `users`: User accounts

### New (Phase 3)
- `conversations`: Chat sessions
- `chat_messages`: Message history

## Security Features

- JWT token validation on every request
- User ID verification (path vs token)
- User isolation on all database queries
- Input validation and sanitization
- Secure error messages

## Next Steps (Frontend)

The backend is ready. Next tasks (T016-T028):
1. Create React chat UI components
2. Implement hooks for state management
3. Integrate with backend API
4. Add styling and animations
5. End-to-end testing

## Troubleshooting

### Cohere API Key Issues
```
[WARNING] COHERE_API_KEY not set or using placeholder
```
Solution: Set COHERE_API_KEY in .env file

### Import Errors
```
ModuleNotFoundError: No module named 'services'
```
Solution: Run from backend directory or add to PYTHONPATH

### Database Connection Issues
```
[ERROR] Database initialization failed
```
Solution: Check DATABASE_URL and ensure migrations are run

## API Documentation

Full API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Support

For issues or questions:
1. Check the implementation summary: `backend/IMPLEMENTATION_SUMMARY.md`
2. Review the spec: `specs/001-ai-chatbot/spec.md`
3. Check tasks: `specs/001-ai-chatbot/tasks.md`
