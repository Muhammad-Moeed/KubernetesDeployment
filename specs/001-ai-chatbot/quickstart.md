# Quickstart Guide: AI Todo Chatbot Integration

**Feature**: AI Todo Chatbot Integration
**Branch**: `001-ai-chatbot`
**Date**: 2026-02-09

## Overview

This quickstart guide provides step-by-step instructions for implementing and testing the Phase 3 AI chatbot feature. Follow these steps in order to integrate natural language task management into the existing Phase 2 Todo application.

## Prerequisites

Before starting implementation, ensure:

- ✅ Phase 2 fullstack Todo app is complete and functional
- ✅ Backend: FastAPI with SQLModel, Neon PostgreSQL, Better Auth JWT
- ✅ Frontend: Next.js 16+ with TypeScript, Tailwind CSS
- ✅ All Phase 2 tests passing
- ✅ Cohere API account created with API key
- ✅ Branch `001-ai-chatbot` checked out

## Implementation Phases

### Phase 1: Backend Setup (Database & Models)

**Estimated Effort**: 2-3 hours

#### Step 1.1: Install Dependencies

```bash
cd backend
pip install openai cohere mcp-sdk
pip freeze > requirements.txt
```

**Required packages**:
- `openai` (latest): OpenAI Agents SDK
- `cohere` (latest): Cohere Python SDK
- `mcp-sdk` (latest): Model Context Protocol SDK

#### Step 1.2: Create Database Migration

```bash
cd backend
alembic revision -m "add_chat_tables"
```

Edit the migration file to create `conversations` and `chat_messages` tables (see `data-model.md` for schema).

Run migration:
```bash
alembic upgrade head
```

Verify tables created:
```bash
psql $DATABASE_URL -c "\dt"
```

#### Step 1.3: Create SQLModel Entities

Create new files:
- `backend/src/models/conversation.py` - Conversation model
- `backend/src/models/chat_message.py` - ChatMessage model

Copy model definitions from `data-model.md`.

#### Step 1.4: Configure Cohere API

Create `backend/src/config/cohere.py`:

```python
import os
from openai import OpenAI

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set")

cohere_client = OpenAI(
    api_key=COHERE_API_KEY,
    base_url="https://api.cohere.ai/v1"
)
```

Add to `.env`:
```
COHERE_API_KEY=your_cohere_api_key_here
```

**Verification**:
```bash
python -c "from src.config.cohere import cohere_client; print('Cohere configured')"
```

---

### Phase 2: Backend Implementation (MCP Tools & Chat Service)

**Estimated Effort**: 4-5 hours

#### Step 2.1: Implement MCP Tools

Create `backend/src/services/mcp_tools.py` with six tool functions:
- `add_task(title, description, priority, due_date, user_id)`
- `list_tasks(status_filter, priority_filter, user_id)`
- `complete_task(task_id, user_id)`
- `delete_task(task_id, user_id)`
- `update_task(task_id, updates, user_id)`
- `get_user_info(query_type, user_id)`

Each tool should:
1. Validate parameters
2. Call existing Phase 2 task API or extract from JWT
3. Return structured JSON response
4. Handle errors with appropriate error codes

**Verification**:
```bash
pytest backend/tests/test_mcp_tools.py -v
```

#### Step 2.2: Implement Intent Parser

Create `backend/src/services/intent_parser.py`:

```python
from src.config.cohere import cohere_client
from src.services.mcp_tools import MCP_TOOLS

def parse_intent(user_message: str, conversation_history: list) -> dict:
    """Detect intent and extract parameters using Cohere"""
    messages = conversation_history + [
        {"role": "user", "content": user_message}
    ]

    response = cohere_client.chat.completions.create(
        model="command-r-plus",
        messages=messages,
        tools=MCP_TOOLS,
        tool_choice="auto"
    )

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        return {
            "intent": tool_call.function.name,
            "parameters": json.loads(tool_call.function.arguments),
            "response": response.choices[0].message.content
        }
    else:
        return {
            "intent": "unknown",
            "parameters": {},
            "response": response.choices[0].message.content
        }
```

**Verification**:
```bash
pytest backend/tests/test_intent_parser.py -v
```

#### Step 2.3: Implement Chat Service

Create `backend/src/services/chat_service.py`:

```python
from src.services.intent_parser import parse_intent
from src.services.mcp_tools import execute_tool
from src.models.conversation import Conversation
from src.models.chat_message import ChatMessage

async def process_chat_message(
    db: Session,
    user_id: int,
    message: str,
    conversation_id: Optional[UUID]
) -> dict:
    """Process chat message and return response"""
    # 1. Get or create conversation
    conversation = get_or_create_conversation(db, conversation_id, user_id)

    # 2. Load conversation history
    history = get_conversation_history(db, conversation.id, user_id)

    # 3. Parse intent and extract parameters
    intent_result = parse_intent(message, history)

    # 4. Execute MCP tool if intent detected
    if intent_result["intent"] != "unknown":
        tool_result = execute_tool(
            intent_result["intent"],
            intent_result["parameters"]
        )
        response_text = format_tool_response(tool_result)
    else:
        response_text = intent_result["response"]

    # 5. Save messages to database
    save_message(db, conversation.id, user_id, "user", message)
    save_message(db, conversation.id, user_id, "bot", response_text)

    # 6. Return response
    return {
        "success": True,
        "response": response_text,
        "conversation_id": str(conversation.id),
        "timestamp": datetime.utcnow().isoformat()
    }
```

#### Step 2.4: Create Chat API Endpoint

Create `backend/src/api/chat.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from src.services.chat_service import process_chat_message
from src.middleware.jwt_auth import get_current_user

router = APIRouter()

@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: int,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate user_id matches JWT token
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # Process chat message
    result = await process_chat_message(
        db,
        user_id,
        request.message,
        request.conversation_id
    )

    return result
```

Register router in `backend/src/main.py`:
```python
from src.api.chat import router as chat_router
app.include_router(chat_router)
```

**Verification**:
```bash
# Start backend
uvicorn src.main:app --reload

# Test endpoint
curl -X POST http://localhost:8000/api/123/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk", "conversation_id": null}'
```

---

### Phase 3: Frontend Implementation (Chat UI)

**Estimated Effort**: 5-6 hours

#### Step 3.1: Install Dependencies

```bash
cd frontend
npm install lucide-react
```

#### Step 3.2: Create Chat Components

Create component files in `frontend/src/components/chat/`:

1. **ChatWidget.tsx** (root component)
2. **ChatIcon.tsx** (floating button)
3. **ChatWindow.tsx** (main window)
4. **ChatHeader.tsx** (header with close button)
5. **MessageList.tsx** (scrollable messages)
6. **Message.tsx** (individual bubble)
7. **ChatInput.tsx** (input with buttons)
8. **VoiceButton.tsx** (microphone button)

See `chatbot-frontend.md` for detailed component specifications.

#### Step 3.3: Create Chat Hooks

Create hooks in `frontend/src/hooks/`:

1. **useChat.ts** - Chat state management
```typescript
export function useChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (text: string) => {
    // Implementation
  };

  return { isOpen, setIsOpen, messages, sendMessage, isLoading };
}
```

2. **useVoiceInput.ts** - Voice recognition
```typescript
export function useVoiceInput() {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");

  const startRecording = () => {
    // Web Speech API implementation
  };

  return { isRecording, transcript, startRecording, stopRecording };
}
```

3. **useChatAPI.ts** - API integration
```typescript
export function useChatAPI() {
  const sendChatMessage = async (message: string, conversationId: string | null) => {
    const response = await fetch(`/api/${userId}/chat`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message, conversation_id: conversationId })
    });
    return response.json();
  };

  return { sendChatMessage };
}
```

#### Step 3.4: Add Chat to Dashboard

Edit `frontend/src/app/dashboard/page.tsx`:

```typescript
import ChatWidget from "@/components/chat/ChatWidget";

export default function DashboardPage() {
  return (
    <div>
      {/* Existing dashboard content */}

      {/* Add chat widget */}
      <ChatWidget />
    </div>
  );
}
```

#### Step 3.5: Add Urdu Translations

Create translation files:

`frontend/public/locales/en/chat.json`:
```json
{
  "welcome": "Hi! I'm your AI assistant. I can help you manage your tasks.",
  "placeholder": "Type a message...",
  "send": "Send",
  "voice": "Voice input"
}
```

`frontend/public/locales/ur/chat.json`:
```json
{
  "welcome": "سلام! میں آپ کا AI اسسٹنٹ ہوں۔ میں آپ کے کاموں کو منظم کرنے میں مدد کر سکتا ہوں۔",
  "placeholder": "پیغام لکھیں...",
  "send": "بھیجیں",
  "voice": "آواز ان پٹ"
}
```

**Verification**:
```bash
npm run dev
# Open http://localhost:3000/dashboard
# Click chat icon, send message, verify response
```

---

### Phase 4: Testing & Validation

**Estimated Effort**: 2-3 hours

#### Step 4.1: Backend Tests

Run all backend tests:
```bash
cd backend
pytest tests/ -v --cov=src
```

Test coverage should be >80% for new code.

#### Step 4.2: Frontend Tests

Run frontend tests:
```bash
cd frontend
npm test
```

#### Step 4.3: Integration Testing

**Test Scenarios**:

1. **Task Creation**:
   - Send: "Add a task to buy groceries"
   - Verify: Task appears in task list with correct details

2. **Task Listing**:
   - Send: "Show me all my tasks"
   - Verify: All tasks displayed with IDs, titles, status

3. **Task Completion**:
   - Send: "Mark task 123 as done"
   - Verify: Task status changes to completed

4. **Task Deletion**:
   - Send: "Delete task 456"
   - Verify: Task removed from list

5. **Task Update**:
   - Send: "Update task 789 to high priority"
   - Verify: Task priority updated

6. **User Info**:
   - Send: "What's my email?"
   - Verify: Correct email displayed

7. **Urdu Support**:
   - Send: "ٹاسک شامل کریں: دودھ خریدنا"
   - Verify: Task created, response in Urdu, RTL layout

8. **Voice Input**:
   - Click microphone, speak "Add task to call dentist"
   - Verify: Speech transcribed, task created

9. **Conversation History**:
   - Send multiple messages
   - Refresh page
   - Verify: History persists

10. **Error Handling**:
    - Send: "Mark task 999 as done" (non-existent)
    - Verify: Friendly error message

#### Step 4.4: User Isolation Testing

Verify users cannot access other users' data:
```bash
# User 123 tries to access user 456's chat
curl -X POST http://localhost:8000/api/456/chat \
  -H "Authorization: Bearer $JWT_TOKEN_USER_123" \
  -d '{"message": "Show my tasks"}'
# Expected: 403 Forbidden
```

---

### Phase 5: Deployment

**Estimated Effort**: 1-2 hours

#### Step 5.1: Environment Variables

**Backend** (Render/Railway):
```
COHERE_API_KEY=your_cohere_api_key
DATABASE_URL=your_neon_postgres_url
BETTER_AUTH_SECRET=your_auth_secret
CORS_ORIGINS=https://your-frontend.vercel.app
```

**Frontend** (Vercel):
```
NEXT_PUBLIC_API_URL=https://your-backend.render.com
```

#### Step 5.2: Database Migration

Run migration on production database:
```bash
alembic upgrade head
```

#### Step 5.3: Deploy Backend

```bash
git push origin 001-ai-chatbot
# Deploy via Render/Railway dashboard
```

#### Step 5.4: Deploy Frontend

```bash
cd frontend
vercel --prod
```

#### Step 5.5: Smoke Test

Test deployed application:
1. Open deployed frontend URL
2. Log in with test account
3. Click chat icon
4. Send test message
5. Verify response received

---

## Troubleshooting

### Common Issues

**Issue**: Cohere API returns 401 Unauthorized
- **Solution**: Verify `COHERE_API_KEY` is set correctly in environment

**Issue**: Chat endpoint returns 403 Forbidden
- **Solution**: Ensure JWT token user_id matches URL user_id parameter

**Issue**: Voice input not working
- **Solution**: Check browser compatibility (Chrome/Edge/Safari only), verify microphone permissions

**Issue**: Urdu text not displaying correctly
- **Solution**: Ensure Urdu fonts installed, check RTL CSS direction

**Issue**: Conversation history not loading
- **Solution**: Verify conversation_id persisted in local storage, check database query

**Issue**: Slow response times (>5 seconds)
- **Solution**: Check Cohere API latency, optimize database queries, verify network connection

---

## Performance Benchmarks

**Target Metrics**:
- Chat response time: <3 seconds (P95)
- Conversation history load: <500ms
- Intent detection accuracy: >90%
- Voice transcription success: >85%

**Monitoring**:
```bash
# Backend response times
curl -w "@curl-format.txt" -X POST http://localhost:8000/api/123/chat ...

# Database query times
psql $DATABASE_URL -c "EXPLAIN ANALYZE SELECT * FROM chat_messages WHERE conversation_id = '...';"
```

---

## Next Steps

After completing implementation:

1. ✅ Run full test suite (backend + frontend)
2. ✅ Verify all bonus features (Urdu + Voice)
3. ✅ Update README with Phase 3 documentation
4. ✅ Record <90 second demo video
5. ✅ Submit via Google Form

---

## Support & Resources

- **Specifications**: See `specs/001-ai-chatbot/` directory
- **API Contracts**: `specs/001-ai-chatbot/contracts/`
- **Data Model**: `specs/001-ai-chatbot/data-model.md`
- **Architecture**: `specs/001-ai-chatbot/chatbot-architecture.md`
- **MCP Tools**: `specs/001-ai-chatbot/chatbot-tools.md`
- **Frontend**: `specs/001-ai-chatbot/chatbot-frontend.md`

---

## Success Criteria Checklist

- [ ] All 6 MCP tools implemented and tested
- [ ] Chat endpoint accepts natural language messages
- [ ] Intent detection works for English and Urdu
- [ ] All CRUD operations executable via chat
- [ ] User info queries return correct data
- [ ] Conversation history persists across sessions
- [ ] Floating chat icon visible on dashboard
- [ ] Voice input transcribes and executes commands
- [ ] Urdu messages display with RTL layout
- [ ] User isolation enforced (no cross-user access)
- [ ] Error messages are user-friendly
- [ ] Response times meet performance targets
- [ ] All tests passing (backend + frontend)
- [ ] Application deployed and accessible
- [ ] Demo video recorded (<90 seconds)

---

**Implementation Complete!** 🎉

The AI Todo Chatbot is now fully integrated into your Phase 2 application. Users can manage tasks through natural language conversation in English and Urdu, with voice input support for hands-free operation.
