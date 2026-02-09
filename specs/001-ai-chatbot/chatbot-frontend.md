# Chatbot Frontend Specification

**Feature**: AI Todo Chatbot Integration
**Branch**: `001-ai-chatbot`
**Created**: 2026-02-09
**Status**: Draft

## Overview

This document defines the frontend chat interface for the Phase 3 AI Todo Chatbot, including the floating chat icon, chat window UI, voice input integration, Urdu language support with RTL layout, and connection to the backend chat API.

## Component Architecture

### Component Hierarchy

```
Dashboard Layout
└─ ChatWidget (floating, always visible)
   ├─ ChatIcon (bottom-right corner)
   └─ ChatWindow (conditional, opens on click)
      ├─ ChatHeader
      │  ├─ Title
      │  └─ CloseButton
      ├─ MessageList
      │  ├─ WelcomeMessage (first time only)
      │  └─ Message[] (user and bot messages)
      │     ├─ MessageBubble
      │     ├─ Timestamp
      │     └─ Sender (user/bot indicator)
      ├─ ChatInput
      │  ├─ TextInput
      │  ├─ VoiceButton (bonus feature)
      │  └─ SendButton
      └─ LoadingIndicator (during API calls)
```

### Component Responsibilities

**ChatWidget**: Root component, manages chat state (open/closed), conversation ID
**ChatIcon**: Floating button that opens/closes chat window
**ChatWindow**: Main chat interface container
**ChatHeader**: Title bar with close button
**MessageList**: Scrollable list of messages with auto-scroll to bottom
**Message**: Individual message bubble with sender styling
**ChatInput**: Input field with voice button and send button
**VoiceButton**: Microphone button for voice input (bonus feature)

## Floating Chat Icon

### Visual Design

**Position**: Fixed position in bottom-right corner of viewport
**Dimensions**: 60px × 60px circular button
**Colors**:
- Background: Primary brand color (e.g., #3B82F6 blue)
- Icon: White chat bubble or message icon
- Hover: Slightly darker shade with subtle scale animation
- Active: Pressed state with scale down

**Icon**: Chat bubble icon (e.g., from Heroicons, Lucide, or similar)

**Z-Index**: High value (e.g., 1000) to stay above other content

**Spacing**: 24px from bottom edge, 24px from right edge

### Behavior

**Initial State**: Visible on all authenticated dashboard pages
**Click Action**: Toggle chat window open/closed
**Hover Effect**: Scale up slightly (1.05x) with smooth transition
**Notification Badge**: Optional red dot indicator for new messages (future enhancement)

**Accessibility**:
- `aria-label="Open chat"`
- `role="button"`
- Keyboard accessible (Tab to focus, Enter/Space to activate)

### Responsive Design

**Desktop (>768px)**: 60px × 60px, 24px spacing
**Tablet (768px-1024px)**: 56px × 56px, 20px spacing
**Mobile (<768px)**: 52px × 52px, 16px spacing

## Chat Window

### Visual Design

**Position**: Fixed position in bottom-right corner, above chat icon
**Dimensions**:
- Desktop: 400px width × 600px height
- Tablet: 380px width × 550px height
- Mobile: Full screen (100vw × 100vh)

**Colors**:
- Background: White (#FFFFFF)
- Border: Light gray (#E5E7EB)
- Shadow: Subtle drop shadow for depth

**Border Radius**: 12px (desktop/tablet), 0px (mobile full screen)

**Animation**: Slide up from bottom with fade in (300ms ease-out)

### Layout Structure

```
┌─────────────────────────────────────┐
│ Chat Header                    [X]  │ ← 60px height
├─────────────────────────────────────┤
│                                     │
│  Welcome Message (first time)      │
│                                     │
│  ┌─────────────────────────────┐  │
│  │ User: Add task to buy milk  │  │
│  └─────────────────────────────┘  │
│                                     │
│  ┌─────────────────────────────┐  │
│  │ Bot: I've created task...   │  │
│  └─────────────────────────────┘  │
│                                     │
│  ┌─────────────────────────────┐  │
│  │ User: Show my tasks         │  │
│  └─────────────────────────────┘  │
│                                     │
│  ┌─────────────────────────────┐  │
│  │ Bot: You have 5 tasks...    │  │
│  └─────────────────────────────┘  │
│                                     │
│  [Scrollable message area]         │
│                                     │
├─────────────────────────────────────┤
│ [🎤] [Type a message...    ] [→]  │ ← 70px height
└─────────────────────────────────────┘
```

### Chat Header

**Content**: "AI Assistant" or "Todo Chat"
**Height**: 60px
**Background**: Gradient or solid primary color
**Text Color**: White
**Close Button**: X icon in top-right corner

**Accessibility**:
- Close button: `aria-label="Close chat"`
- Header: `role="banner"`

### Message List

**Scrolling**: Auto-scroll to bottom on new messages
**Padding**: 16px horizontal, 12px vertical
**Max Height**: Calculated (window height - header - input)
**Empty State**: Welcome message when no conversation history

**Message Spacing**: 12px between messages
**Grouping**: Messages from same sender within 1 minute grouped together

### Message Bubble Design

**User Messages**:
- Alignment: Right-aligned
- Background: Primary color (#3B82F6)
- Text Color: White
- Border Radius: 16px (rounded corners, flat on bottom-right)
- Max Width: 80% of container
- Padding: 12px 16px

**Bot Messages**:
- Alignment: Left-aligned
- Background: Light gray (#F3F4F6)
- Text Color: Dark gray (#1F2937)
- Border Radius: 16px (rounded corners, flat on bottom-left)
- Max Width: 80% of container
- Padding: 12px 16px

**Timestamp**:
- Font Size: 11px
- Color: Gray (#6B7280)
- Position: Below message bubble
- Format: "10:30 AM" or "Yesterday 3:45 PM"

**Sender Indicator**:
- User: "You" or user name
- Bot: "AI Assistant" or bot icon

### Welcome Message

**Content**: "Hi! I'm your AI assistant. I can help you manage your tasks. Try saying 'Add a task to buy groceries' or 'Show me all my tasks'."

**Styling**: Centered, light background, informational tone

**Display Logic**: Show only when conversation history is empty

### Loading Indicator

**Type**: Three animated dots or spinner
**Position**: Bottom of message list while waiting for bot response
**Animation**: Pulsing or bouncing dots
**Color**: Gray (#9CA3AF)

## Chat Input

### Text Input Field

**Placeholder**: "Type a message..." (English) or "پیغام لکھیں..." (Urdu)
**Height**: 44px
**Border**: 1px solid light gray, rounded corners
**Focus State**: Blue border, subtle shadow
**Max Length**: 1000 characters
**Multiline**: No (single line input)

**Accessibility**:
- `aria-label="Chat message input"`
- `placeholder` attribute
- `maxLength` attribute

### Send Button

**Icon**: Arrow right or paper plane icon
**Position**: Right side of input field
**Size**: 40px × 40px
**Color**: Primary color when enabled, gray when disabled
**Disabled State**: When input is empty or API call in progress

**Click Action**: Send message to backend API
**Keyboard Shortcut**: Enter key sends message

**Accessibility**:
- `aria-label="Send message"`
- `disabled` attribute when appropriate

### Voice Button (Bonus Feature)

**Icon**: Microphone icon
**Position**: Left side of input field
**Size**: 40px × 40px
**Color**: Gray when inactive, red when recording
**Animation**: Pulsing red when recording

**States**:
1. **Inactive**: Gray microphone icon
2. **Recording**: Red microphone icon with pulsing animation
3. **Transcribing**: Loading spinner
4. **Error**: Red with X overlay

**Click Action**: Toggle voice recording on/off

**Accessibility**:
- `aria-label="Voice input"`
- `aria-pressed` attribute for toggle state

## Voice Input Integration (Bonus Feature)

### Web Speech API

**Browser Support**: Chrome, Edge, Safari (check compatibility)
**Language Support**: English (en-US) and Urdu (ur-PK)

**Implementation Flow**:
1. User clicks microphone button
2. Request microphone permission (if not granted)
3. Start speech recognition
4. Display visual feedback (pulsing red icon)
5. Transcribe speech to text in real-time
6. Display transcribed text in input field
7. Auto-stop after 2 seconds of silence
8. Auto-send transcribed message

### Permission Handling

**First Time**: Browser prompts for microphone permission
**Granted**: Proceed with voice recording
**Denied**: Show error message: "Microphone access is required for voice input. Please enable it in your browser settings."

**Error Message Styling**: Red background, white text, dismissible

### Visual Feedback

**Recording Indicator**:
- Pulsing red microphone icon
- Optional: Waveform animation showing audio levels
- Text: "Listening..." below input field

**Transcription Indicator**:
- Spinner icon
- Text: "Transcribing..." below input field

**Success State**:
- Transcribed text appears in input field
- Microphone icon returns to gray
- Message auto-sends after 1 second

### Error Handling

**No Microphone**: "No microphone detected. Please connect a microphone and try again."
**Permission Denied**: "Microphone access denied. Please enable it in browser settings."
**Recognition Failed**: "Couldn't understand that. Please try again or type your message."
**Network Error**: "Voice recognition unavailable. Please type your message."

## Urdu Language Support (Bonus Feature)

### RTL Layout Detection

**Detection Logic**: Detect Urdu characters in message text using Unicode ranges
**Unicode Range**: U+0600 to U+06FF (Arabic/Urdu script)

**Automatic RTL**: When Urdu text detected, apply RTL layout to message bubble

### RTL Styling

**Message Bubbles**:
- User messages: Left-aligned (reversed from LTR)
- Bot messages: Right-aligned (reversed from LTR)
- Text direction: `dir="rtl"`
- Text alignment: `text-align: right`

**Input Field**:
- Text direction: Auto-detect based on first character
- Placeholder: Switch to Urdu when Urdu keyboard detected

**Font Support**:
- Primary: System Urdu fonts (Noto Nastaliq Urdu, Jameel Noori Nastaleeq)
- Fallback: Generic sans-serif with Urdu support

### Language-Specific UI

**Placeholder Text**:
- English: "Type a message..."
- Urdu: "پیغام لکھیں..."

**Button Labels**:
- Send: "→" (universal icon, no text)
- Voice: Microphone icon (universal)
- Close: "×" (universal)

**Welcome Message**:
- English: "Hi! I'm your AI assistant..."
- Urdu: "سلام! میں آپ کا AI اسسٹنٹ ہوں..."

## Backend API Integration

### API Endpoint

**URL**: `POST /api/{user_id}/chat`
**Method**: POST
**Headers**:
- `Authorization: Bearer {JWT_TOKEN}`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "uuid-string-or-null"
}
```

**Response Body**:
```json
{
  "success": true,
  "response": "I've created a task 'buy groceries' with ID 45.",
  "conversation_id": "uuid-string",
  "timestamp": "2026-02-09T10:30:00Z"
}
```

### Request Flow

1. User types message or uses voice input
2. Frontend validates message (not empty, max 1000 chars)
3. Frontend sends POST request with JWT token
4. Frontend displays loading indicator
5. Backend processes message and returns response
6. Frontend displays bot response in message list
7. Frontend persists conversation_id for subsequent messages

### Error Handling

**Network Error**: "Connection lost. Please check your internet and try again."
**401 Unauthorized**: "Your session has expired. Please log in again."
**403 Forbidden**: "Access denied. Please log in again."
**500 Server Error**: "Something went wrong. Please try again in a moment."
**Timeout**: "Request timed out. Please try again."

**Error Display**: Red banner at top of chat window, dismissible

### Loading States

**Sending Message**: Disable input and send button, show loading indicator
**Receiving Response**: Show typing indicator (three dots) in message list
**Timeout**: 30 seconds, then show error message

## State Management

### Component State

**Chat Widget State**:
- `isOpen`: boolean (chat window open/closed)
- `conversationId`: string | null (current conversation ID)
- `messages`: Message[] (array of message objects)
- `isLoading`: boolean (API call in progress)
- `error`: string | null (error message to display)

**Message Object**:
```typescript
{
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: Date;
  isRTL: boolean;
}
```

**Voice Input State**:
- `isRecording`: boolean (microphone active)
- `isTranscribing`: boolean (speech-to-text in progress)
- `transcript`: string (current transcription)

### Persistence

**Local Storage**:
- `chat_conversation_id`: Store conversation ID for session continuity
- `chat_is_open`: Store chat window state (optional)

**Session Storage**: Alternative to local storage for temporary persistence

**Clear on Logout**: Remove conversation ID when user logs out

## Responsive Design

### Desktop (>1024px)

- Chat icon: 60px × 60px, bottom-right corner
- Chat window: 400px × 600px, positioned above icon
- Message bubbles: Max 80% width
- Input field: Full width with padding

### Tablet (768px-1024px)

- Chat icon: 56px × 56px, bottom-right corner
- Chat window: 380px × 550px, positioned above icon
- Message bubbles: Max 85% width
- Input field: Full width with padding

### Mobile (<768px)

- Chat icon: 52px × 52px, bottom-right corner
- Chat window: Full screen (100vw × 100vh)
- Message bubbles: Max 90% width
- Input field: Fixed at bottom, full width
- Header: Fixed at top
- Message list: Scrollable between header and input

## Accessibility

### Keyboard Navigation

- Tab: Navigate between chat icon, input field, send button, voice button, close button
- Enter: Send message (when input focused)
- Escape: Close chat window
- Space: Activate buttons (when focused)

### Screen Reader Support

**ARIA Labels**:
- Chat icon: `aria-label="Open chat assistant"`
- Chat window: `role="dialog"`, `aria-label="Chat assistant"`
- Message list: `role="log"`, `aria-live="polite"`
- Input field: `aria-label="Type your message"`
- Send button: `aria-label="Send message"`
- Voice button: `aria-label="Voice input"`
- Close button: `aria-label="Close chat"`

**Focus Management**:
- When chat opens: Focus on input field
- When chat closes: Return focus to chat icon
- Trap focus within chat window when open

### Color Contrast

- Text on primary color: WCAG AA compliant (4.5:1 ratio)
- Text on light background: WCAG AA compliant
- Error messages: High contrast red

## Performance Optimization

### Lazy Loading

- Load chat component only when user clicks chat icon (first time)
- Lazy load voice recognition API only when voice button clicked

### Message Virtualization

- For conversations with >100 messages, use virtual scrolling
- Render only visible messages + buffer

### Debouncing

- Debounce typing indicator (show after 500ms of inactivity)
- Debounce auto-scroll (prevent excessive scroll events)

### Caching

- Cache conversation history in component state
- Avoid re-fetching history on every render

## Testing Scenarios

### Functional Tests

1. **Open/Close Chat**: Click icon to open, click close button to close
2. **Send Message**: Type message, click send, verify message appears
3. **Receive Response**: Verify bot response appears after API call
4. **Voice Input**: Click microphone, speak, verify transcription
5. **Urdu Support**: Type Urdu message, verify RTL layout
6. **Error Handling**: Simulate network error, verify error message
7. **Conversation History**: Reload page, verify history persists

### Visual Tests

1. **Responsive Design**: Test on desktop, tablet, mobile
2. **Message Bubbles**: Verify user/bot styling differences
3. **RTL Layout**: Verify Urdu messages display correctly
4. **Loading States**: Verify loading indicators appear
5. **Error States**: Verify error messages display correctly

### Accessibility Tests

1. **Keyboard Navigation**: Navigate using only keyboard
2. **Screen Reader**: Test with screen reader (NVDA, JAWS, VoiceOver)
3. **Color Contrast**: Verify all text meets WCAG AA standards
4. **Focus Management**: Verify focus moves correctly

## Cross-References

- **@specs/001-ai-chatbot/chatbot-architecture.md**: Backend API architecture
- **@specs/001-ai-chatbot/chatbot-tools.md**: MCP tools and intent handling
- **@specs/001-ai-chatbot/spec.md**: Overall feature specification
- **@specs/ui/dashboard.md**: Dashboard layout where chat is embedded
- **@specs/features/authentication.md**: JWT token handling

## Implementation Notes

### Technology Stack

- **Framework**: Next.js 16+ with App Router
- **Styling**: Tailwind CSS for utility classes
- **Icons**: Heroicons or Lucide React
- **Voice API**: Web Speech API (browser native)
- **HTTP Client**: fetch API or axios
- **State Management**: React useState/useReducer

### Component Files

```
frontend/src/components/chat/
├── ChatWidget.tsx          # Root component
├── ChatIcon.tsx            # Floating icon button
├── ChatWindow.tsx          # Main chat window
├── ChatHeader.tsx          # Header with close button
├── MessageList.tsx         # Scrollable message list
├── Message.tsx             # Individual message bubble
├── ChatInput.tsx           # Input field with buttons
├── VoiceButton.tsx         # Microphone button
└── hooks/
    ├── useChat.ts          # Chat state management
    ├── useVoiceInput.ts    # Voice recognition logic
    └── useChatAPI.ts       # API integration
```

### Styling Approach

- Use Tailwind CSS utility classes for rapid development
- Create custom CSS classes for complex animations
- Use CSS variables for theme colors
- Support dark mode (future enhancement)

### Browser Compatibility

- **Minimum**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Voice Input**: Chrome 90+, Edge 90+, Safari 14.1+ (limited Urdu support)
- **Fallback**: Graceful degradation for unsupported features
