"""
Chat API Routes
FastAPI routes for AI chatbot chat functionality with JWT authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from database.connection import get_session
from middleware.auth import verify_jwt_token, AuthenticatedUser
from services.chat_service import process_chat_message, get_conversation_history
from models.schemas import URDU_TRANSLATIONS


# Create router
router = APIRouter()


# Request/Response Models
class ChatMessageRequest(BaseModel):
    """Request model for sending a chat message"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's message text")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for continuing a conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add a task to buy groceries",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ChatMessageResponse(BaseModel):
    """Response model for chat message"""
    response: str = Field(..., description="Bot's response message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for this chat session")
    intent: str = Field(..., description="Detected intent from user message")
    success: bool = Field(..., description="Whether the operation was successful")
    language: Optional[str] = Field("en", description="Detected language (en or ur)")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the response")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "I've created a task 'buy groceries' with ID 45.",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "intent": "add_task",
                "success": True,
                "language": "en",
                "timestamp": "2026-02-09T10:30:02Z"
            }
        }


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history"""
    success: bool
    conversation_id: Optional[str] = None
    messages: list = []
    count: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "messages": [
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440001",
                        "sender": "user",
                        "message": "Add a task to buy milk",
                        "timestamp": "2026-02-09T10:30:00Z"
                    },
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440002",
                        "sender": "bot",
                        "message": "I've created a task 'buy milk' with ID 45.",
                        "timestamp": "2026-02-09T10:30:02Z"
                    }
                ],
                "count": 2
            }
        }


@router.post(
    "/{user_id}/chat",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a chat message",
    description="Send a message to the AI chatbot and receive a response"
)
async def send_chat_message(
    user_id: str,
    request: ChatMessageRequest,
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Send a chat message to the AI chatbot

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only chat as themselves (user_id must match JWT)

    **Request Body**:
    - message: Required, 1-1000 characters
    - conversation_id: Optional, UUID of existing conversation

    **Response**: 200 OK with bot response and conversation ID

    **Flow**:
    1. Validate JWT and user_id match
    2. Parse intent from message using Cohere
    3. Execute appropriate MCP tool
    4. Generate natural language response
    5. Save conversation to database
    6. Return response to user
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only send messages as yourself"
            }
        )

    # Validate message length
    if len(request.message) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Message too long",
                "error_urdu": URDU_TRANSLATIONS.get("Invalid request"),
                "detail": "Message must be 1000 characters or less"
            }
        )

    # Parse conversation_id if provided
    conversation_id_uuid = None
    if request.conversation_id:
        try:
            conversation_id_uuid = UUID(request.conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid conversation ID",
                    "error_urdu": URDU_TRANSLATIONS.get("Invalid request"),
                    "detail": "Conversation ID must be a valid UUID"
                }
            )

    # Extract user info from JWT token payload
    user_email = user.payload.get("email")
    user_name = user.payload.get("name")

    # Process chat message
    try:
        result = process_chat_message(
            session=session,
            user_id=user.user_id,
            message=request.message,
            conversation_id=conversation_id_uuid,
            user_email=user_email,
            user_name=user_name
        )

        return ChatMessageResponse(
            response=result.get("response", "I'm sorry, I couldn't process that."),
            conversation_id=result.get("conversation_id", ""),
            intent=result.get("intent", "unknown"),
            success=result.get("success", False),
            language=result.get("language", "en"),
            timestamp=datetime.now().isoformat() + "Z"
        )

    except Exception as e:
        print(f"[ERROR] Chat endpoint failed: {type(e).__name__}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Server error",
                "error_urdu": URDU_TRANSLATIONS.get("Server error"),
                "detail": "Failed to process chat message. Please try again."
            }
        )


@router.get(
    "/{user_id}/chat/history/{conversation_id}",
    response_model=ConversationHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get conversation history",
    description="Retrieve message history for a conversation"
)
async def get_chat_history(
    user_id: str,
    conversation_id: str,
    user: AuthenticatedUser = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Get conversation history

    **Authentication**: Required (JWT token in Authorization header)

    **User Isolation**: User can only access their own conversations

    **Response**: 200 OK with array of messages in chronological order
    """
    # Enforce user isolation: JWT user_id must match path user_id
    if user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only access your own conversations"
            }
        )

    # Parse conversation_id
    try:
        conversation_id_uuid = UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid conversation ID",
                "error_urdu": URDU_TRANSLATIONS.get("Invalid request"),
                "detail": "Conversation ID must be a valid UUID"
            }
        )

    # Get conversation history
    try:
        result = get_conversation_history(
            session=session,
            user_id=user.user_id,
            conversation_id=conversation_id_uuid,
            limit=100
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "Conversation not found",
                    "error_urdu": URDU_TRANSLATIONS.get("Task not found"),
                    "detail": "The conversation does not exist or you don't have access to it"
                }
            )

        return ConversationHistoryResponse(
            success=True,
            conversation_id=result.get("conversation_id"),
            messages=result.get("messages", []),
            count=result.get("count", 0)
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Get history endpoint failed: {type(e).__name__}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Server error",
                "error_urdu": URDU_TRANSLATIONS.get("Server error"),
                "detail": "Failed to retrieve conversation history. Please try again."
            }
        )
