# Todo App - Full-Stack Multi-User Task Management

A modern, full-stack todo application with AI-powered chatbot integration, built with Next.js and FastAPI.

## 🚀 Features

### Phase 2: Core Todo Application
- ✅ User authentication with Better Auth (JWT tokens)
- ✅ Full CRUD operations for tasks
- ✅ Multi-user support with user isolation
- ✅ Priority levels (low, medium, high)
- ✅ Task completion tracking
- ✅ Due date management
- ✅ Dark mode support
- ✅ Responsive design

### Phase 3: AI Chatbot Integration 🤖

#### Core Features
- ✅ **Natural Language Task Creation**: Create tasks by simply saying "Add a task to buy groceries"
- ✅ **Full CRUD via Chat**: List, complete, delete, and update tasks through conversation
- ✅ **User Information Queries**: Ask "What's my email?" or "What's my name?"
- ✅ **Conversation History**: Chat history persists across sessions
- ✅ **Floating Chat Interface**: Always-accessible chat icon in bottom-right corner

#### Bonus Features 🎁
- ✅ **Urdu Language Support** (+100 points): Full bilingual support with RTL layout
- ✅ **Voice Input** (+200 points): Hands-free task management with Web Speech API

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT
- **Voice Recognition**: Web Speech API
- **State Management**: React Hooks

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **AI/NLP**: Cohere API (command-r-plus model)
- **Authentication**: JWT with Better Auth integration
- **Architecture**: RESTful API with MCP tools

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.13+
- PostgreSQL database (Neon recommended)
- Cohere API key (for AI chatbot)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-FullStack
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add:
# - DATABASE_URL (Neon PostgreSQL connection string)
# - BETTER_AUTH_SECRET (must match frontend)
# - COHERE_API_KEY (from https://dashboard.cohere.com/api-keys)

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
# Edit .env.local and add:
# - NEXT_PUBLIC_API_URL=http://localhost:8000
# - BETTER_AUTH_SECRET (must match backend)
# - DATABASE_URL (same as backend)

# Start the development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## 🎯 Using the AI Chatbot

### Getting Started

1. **Sign up** or **log in** to your account
2. Navigate to the **Dashboard**
3. Click the **floating chat icon** in the bottom-right corner
4. Start chatting with the AI assistant!

### Example Commands

#### Task Creation
```
"Add a task to buy groceries"
"Create a high priority task to finish the report by Friday"
"ٹاسک شامل کریں: دودھ خریدنا" (Urdu)
```

#### Task Management
```
"Show me all my tasks"
"List my incomplete tasks"
"Mark task 5 as done"
"Delete task 3"
"Update task 2 to high priority"
```

#### User Information
```
"What's my email?"
"What's my name?"
"میری ای میل کیا ہے؟" (Urdu)
```

#### Voice Input
1. Click the **microphone icon** in the chat input
2. Speak your command (e.g., "Add a task to call the dentist")
3. The speech will be transcribed and sent automatically

### Supported Languages

- **English**: Full support for all commands
- **Urdu**: Complete bilingual support with RTL layout
  - The chatbot automatically detects Urdu text
  - Responses are provided in the same language as your input
  - UI adapts with right-to-left text direction

## 🏗️ Architecture

### Backend Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── routes/
│   ├── tasks.py           # Task CRUD endpoints
│   ├── auth.py            # Authentication endpoints
│   └── chat.py            # AI chatbot endpoints
├── services/
│   ├── mcp_tools.py       # MCP tools (add_task, list_tasks, etc.)
│   ├── intent_parser.py   # Cohere-based NLP intent detection
│   └── chat_service.py    # Chat orchestration and response generation
├── models/
│   ├── task.py            # Task SQLModel
│   ├── user.py            # User SQLModel
│   ├── conversation.py    # Conversation SQLModel
│   └── chat_message.py    # ChatMessage SQLModel
├── middleware/
│   └── auth.py            # JWT verification middleware
└── database/
    ├── connection.py      # Database session management
    └── queries.py         # Database query functions
```

### Frontend Architecture

```
frontend/
├── src/
│   ├── app/
│   │   ├── (dashboard)/
│   │   │   ├── dashboard/page.tsx    # Main dashboard with ChatWidget
│   │   │   ├── tasks/page.tsx        # Task management page
│   │   │   └── settings/page.tsx     # User settings
│   │   ├── login/page.tsx            # Login page
│   │   └── signup/page.tsx           # Signup page
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatWidget.tsx        # Root chat component
│   │   │   ├── ChatIcon.tsx          # Floating chat button
│   │   │   ├── ChatWindow.tsx        # Chat window container
│   │   │   ├── ChatHeader.tsx        # Chat header with close button
│   │   │   ├── MessageList.tsx       # Scrollable message list
│   │   │   ├── Message.tsx           # Individual message bubble
│   │   │   ├── ChatInput.tsx         # Text input with send button
│   │   │   └── VoiceButton.tsx       # Voice input button
│   │   └── layout/
│   │       └── dashboard-layout.tsx  # Dashboard layout wrapper
│   ├── hooks/
│   │   ├── useChat.ts                # Chat state management
│   │   └── useChatAPI.ts             # Chat API integration
│   ├── services/
│   │   └── chatService.ts            # HTTP client for chat API
│   ├── types/
│   │   └── chat.ts                   # TypeScript type definitions
│   └── styles/
│       └── chat.css                  # Chat-specific styles
└── public/
    └── locales/
        ├── en/chat.json              # English translations
        └── ur/chat.json              # Urdu translations
```

### AI Chatbot Flow

```
User Message → Intent Parser (Cohere) → MCP Tool Execution → Response Generation → Database Persistence
```

1. **User sends message** via chat interface
2. **Intent Parser** analyzes message using Cohere API
   - Detects intent (add_task, list_tasks, complete_task, etc.)
   - Extracts parameters (title, priority, task_id, etc.)
   - Identifies language (English or Urdu)
3. **MCP Tool Executor** performs the requested operation
   - Validates parameters
   - Executes database operations
   - Returns structured result
4. **Response Generator** creates natural language response
   - Formats result in detected language
   - Generates user-friendly message
5. **Database Persistence** saves conversation
   - Stores user message
   - Stores bot response
   - Updates conversation timestamp

## 🔐 Security

- **JWT Authentication**: All API endpoints require valid JWT tokens
- **User Isolation**: Users can only access their own data
- **Input Validation**: All user inputs are validated and sanitized
- **SQL Injection Prevention**: SQLModel ORM with parameterized queries
- **CORS Configuration**: Configurable allowed origins
- **Environment Variables**: Sensitive data stored in .env files

## 🧪 Testing

### Manual Testing Checklist

#### User Story 1: Natural Language Task Creation
- [ ] Open chat interface
- [ ] Send "Add a task to buy milk"
- [ ] Verify task appears in task list
- [ ] Verify bot responds with confirmation

#### User Story 2: Task Management via Chat
- [ ] Send "Show me all my tasks"
- [ ] Send "Mark task X as done"
- [ ] Send "Delete task Y"
- [ ] Send "Update task Z to high priority"
- [ ] Verify all operations succeed

#### User Story 3: User Information & History
- [ ] Ask "What's my email?"
- [ ] Close and reopen chat
- [ ] Verify conversation history persists

#### User Story 4: Urdu Language Support
- [ ] Send "ٹاسک شامل کریں: دودھ خریدنا"
- [ ] Verify task created with Urdu title
- [ ] Verify bot responds in Urdu
- [ ] Verify RTL layout applied

#### User Story 5: Voice Input
- [ ] Click microphone icon
- [ ] Speak "Add task to buy groceries"
- [ ] Verify transcription and task creation

## 📊 Database Schema

### Tables

#### tasks
- `id` (INTEGER, PK)
- `user_id` (VARCHAR, FK → users.id)
- `title` (VARCHAR, NOT NULL)
- `description` (TEXT)
- `completed` (BOOLEAN, DEFAULT false)
- `priority` (ENUM: low, medium, high)
- `due_date` (TIMESTAMP)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### conversations
- `id` (UUID, PK)
- `user_id` (VARCHAR, FK → users.id)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### chat_messages
- `id` (UUID, PK)
- `conversation_id` (UUID, FK → conversations.id)
- `user_id` (VARCHAR, FK → users.id)
- `sender` (ENUM: user, bot)
- `message_text` (TEXT, NOT NULL)
- `message_metadata` (JSONB)
- `created_at` (TIMESTAMP)

## 🚀 Deployment

### Backend Deployment (Render/Railway)

1. Create a new web service
2. Connect your GitHub repository
3. Set environment variables:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - `COHERE_API_KEY`
   - `FRONTEND_URL`
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel)

1. Import your GitHub repository
2. Set framework preset: Next.js
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` (your backend URL)
   - `BETTER_AUTH_SECRET`
   - `DATABASE_URL`
4. Deploy

## 📝 API Documentation

### Chat Endpoints

#### POST /api/{user_id}/chat
Send a message to the AI chatbot.

**Request:**
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-uuid"
}
```

**Response:**
```json
{
  "response": "I've created a task 'buy groceries' with ID 45.",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "add_task",
  "success": true,
  "language": "en"
}
```

#### GET /api/{user_id}/chat/history/{conversation_id}
Retrieve conversation history.

**Response:**
```json
{
  "success": true,
  "conversation_id": "uuid",
  "messages": [...],
  "count": 10
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Cohere**: AI-powered natural language processing
- **Neon**: Serverless PostgreSQL database
- **Better Auth**: Authentication solution
- **Next.js**: React framework
- **FastAPI**: Modern Python web framework

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ for Hackathon II: Evolution of Todo**

**Bonus Features Earned**: +300 points (Urdu +100, Voice +200)
