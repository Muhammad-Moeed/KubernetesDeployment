"""
Chat Service
Orchestrates chat message processing, intent parsing, and MCP tool execution
"""
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import Session, select

from services.intent_parser import parse_intent
from services import mcp_tools
from models.conversation import Conversation
from models.chat_message import ChatMessage, MessageSender


def process_chat_message(
    session: Session,
    user_id: str,
    message: str,
    conversation_id: Optional[UUID] = None,
    user_email: Optional[str] = None,
    user_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process a chat message from the user

    This is the main orchestration function that:
    1. Gets or creates a conversation
    2. Saves the user's message
    3. Parses intent from the message
    4. Executes appropriate MCP tool
    5. Generates response
    6. Saves bot's response
    7. Returns response to frontend

    Args:
        session: Database session
        user_id: User ID from JWT token
        message: User's message text
        conversation_id: Optional conversation ID (None for new conversation)
        user_email: User email from JWT token (for get_user_info tool)
        user_name: User name from JWT token (for get_user_info tool)

    Returns:
        Dictionary with response, conversation_id, and metadata

    Example Response:
        {
            "response": "I've created a task 'buy milk' with ID 45.",
            "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
            "intent": "add_task",
            "success": True
        }
    """
    try:
        # Step 1: Get or create conversation
        conversation = _get_or_create_conversation(session, user_id, conversation_id)

        # Step 2: Save user message to database
        user_message = ChatMessage(
            conversation_id=conversation.id,
            user_id=user_id,
            sender=MessageSender.USER,
            message_text=message,
            message_metadata=None
        )
        session.add(user_message)
        session.commit()

        # Step 3: Parse intent from message
        intent_data = parse_intent(message)
        intent = intent_data.get("intent", "unknown")
        parameters = intent_data.get("parameters", {})
        language = intent_data.get("language", "en")

        # Step 4: Execute appropriate MCP tool based on intent
        tool_result = _execute_tool(
            session=session,
            user_id=user_id,
            intent=intent,
            parameters=parameters,
            user_email=user_email,
            user_name=user_name
        )

        # Step 5: Generate natural language response
        response_text = _generate_response(
            intent=intent,
            tool_result=tool_result,
            language=language
        )

        # Step 6: Save bot response to database
        bot_message = ChatMessage(
            conversation_id=conversation.id,
            user_id=user_id,
            sender=MessageSender.BOT,
            message_text=response_text,
            message_metadata={
                "intent": intent,
                "tool_result": tool_result,
                "language": language
            }
        )
        session.add(bot_message)
        session.commit()

        # Step 7: Return response
        return {
            "response": response_text,
            "conversation_id": str(conversation.id),
            "intent": intent,
            "success": tool_result.get("success", False),
            "language": language
        }

    except Exception as e:
        print(f"[ERROR] Chat message processing failed: {type(e).__name__}: {e}")

        # Return error response
        return {
            "response": "I'm sorry, I encountered an error processing your message. Please try again.",
            "conversation_id": str(conversation_id) if conversation_id else None,
            "intent": "error",
            "success": False,
            "error": str(e)
        }


def _get_or_create_conversation(
    session: Session,
    user_id: str,
    conversation_id: Optional[UUID] = None
) -> Conversation:
    """
    Get existing conversation or create a new one

    Args:
        session: Database session
        user_id: User ID
        conversation_id: Optional conversation ID

    Returns:
        Conversation object
    """
    if conversation_id:
        # Try to get specific conversation
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()
        if conversation:
            return conversation

    # Check if user already has a conversation
    statement = select(Conversation).where(Conversation.user_id == user_id)
    conversation = session.exec(statement).first()
    
    if conversation:
        return conversation

    # Create new conversation only if user has none
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    return conversation


def _execute_tool(
    session: Session,
    user_id: str,
    intent: str,
    parameters: Dict[str, Any],
    user_email: Optional[str] = None,
    user_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute the appropriate MCP tool based on detected intent

    Args:
        session: Database session
        user_id: User ID
        intent: Detected intent
        parameters: Extracted parameters
        user_email: User email from JWT
        user_name: User name from JWT

    Returns:
        Tool execution result
    """
    if intent == "add_task":
        return mcp_tools.add_task(
            session=session,
            user_id=user_id,
            title=parameters.get("title", ""),
            description=parameters.get("description"),
            priority=parameters.get("priority", "medium"),
            due_date=parameters.get("due_date")
        )

    elif intent == "list_tasks":
        return mcp_tools.list_tasks(
            session=session,
            user_id=user_id,
            status_filter=parameters.get("status_filter"),
            priority_filter=parameters.get("priority_filter")
        )

    elif intent == "complete_task":
        return mcp_tools.complete_task(
            session=session,
            user_id=user_id,
            task_id=parameters.get("task_id", 0)
        )

    elif intent == "delete_task":
        return mcp_tools.delete_task(
            session=session,
            user_id=user_id,
            task_id=parameters.get("task_id", 0)
        )

    elif intent == "update_task":
        return mcp_tools.update_task(
            session=session,
            user_id=user_id,
            task_id=parameters.get("task_id", 0),
            title=parameters.get("title"),
            description=parameters.get("description"),
            priority=parameters.get("priority"),
            due_date=parameters.get("due_date"),
            completed=parameters.get("completed")
        )

    elif intent == "get_user_info":
        return mcp_tools.get_user_info(
            user_id=user_id,
            email=user_email,
            name=user_name,
            query_type=parameters.get("query_type", "all")
        )

    elif intent == "unknown":
        return {
            "success": False,
            "error": {
                "code": "UNKNOWN_INTENT",
                "message": "I didn't understand that command",
                "details": "I can help you add, list, complete, delete, or update tasks, and get your account information."
            }
        }

    else:
        # Fallback for any unhandled intent
        return {
            "success": False,
            "error": {
                "code": "NOT_IMPLEMENTED",
                "message": f"The '{intent}' feature is not available",
                "details": "I can help you add, list, complete, delete, or update tasks, and get your account information."
            }
        }


def _generate_response(
    intent: str,
    tool_result: Dict[str, Any],
    language: str = "en"
) -> str:
    """
    Generate natural language response based on tool result

    Args:
        intent: Detected intent
        tool_result: Result from MCP tool execution
        language: Language code ("en" or "ur")

    Returns:
        Natural language response string
    """
    success = tool_result.get("success", False)

    # Handle errors
    if not success:
        error = tool_result.get("error", {})
        error_message = error.get("message", "An error occurred")

        if language == "ur":
            return f"معذرت، {error_message}"
        else:
            return f"Sorry, {error_message}"

    # Generate response based on intent
    if intent == "add_task":
        task = tool_result.get("task", {})
        task_id = task.get("id")
        title = task.get("title")
        priority = task.get("priority")

        if language == "ur":
            return f"میں نے '{title}' کا کام بنا دیا ہے (ID {task_id})۔ ترجیح: {priority}"
        else:
            return f"I've created a task '{title}' with ID {task_id}. Priority: {priority}."

    elif intent == "list_tasks":
        tasks = tool_result.get("tasks", [])
        count = tool_result.get("count", 0)

        if count == 0:
            if language == "ur":
                return "آپ کے پاس کوئی کام نہیں ہے۔"
            else:
                return "You don't have any tasks."

        # Format task list
        task_list = []
        for i, task in enumerate(tasks[:5], 1):  # Show first 5 tasks
            task_id = task.get("id")
            title = task.get("title")
            status = task.get("status")
            priority = task.get("priority")
            task_list.append(f"{i}. {title} (ID {task_id}, {status}, {priority})")

        tasks_text = "\n".join(task_list)

        if language == "ur":
            return f"آپ کے {count} کام ہیں:\n{tasks_text}"
        else:
            more_text = f"\n\n...and {count - 5} more." if count > 5 else ""
            return f"You have {count} task{'s' if count != 1 else ''}:\n{tasks_text}{more_text}"

    elif intent == "complete_task":
        task = tool_result.get("task", {})
        task_id = task.get("id")
        title = task.get("title")

        if language == "ur":
            return f"کام '{title}' (ID {task_id}) مکمل ہو گیا ہے۔ ✅"
        else:
            return f"Task '{title}' (ID {task_id}) has been marked as completed. ✅"

    elif intent == "delete_task":
        task_id = tool_result.get("task_id")
        message = tool_result.get("message", "")

        if language == "ur":
            return f"کام حذف ہو گیا ہے۔ {message}"
        else:
            return message

    elif intent == "update_task":
        task = tool_result.get("task", {})
        task_id = task.get("id")
        title = task.get("title")
        message = tool_result.get("message", "")

        if language == "ur":
            return f"کام '{title}' (ID {task_id}) اپ ڈیٹ ہو گیا ہے۔"
        else:
            return message

    elif intent == "get_user_info":
        user_info = tool_result.get("user_info", {})
        email = user_info.get("email")
        name = user_info.get("name")
        user_id = user_info.get("user_id")

        if language == "ur":
            if email and name:
                return f"آپ کا نام: {name}\nآپ کا ای میل: {email}"
            elif email:
                return f"آپ کا ای میل: {email}"
            elif name:
                return f"آپ کا نام: {name}"
            else:
                return f"آپ کا یوزر ID: {user_id}"
        else:
            if email and name:
                return f"Your name: {name}\nYour email: {email}"
            elif email:
                return f"Your email: {email}"
            elif name:
                return f"Your name: {name}"
            else:
                return f"Your user ID: {user_id}"

    elif intent == "unknown":
        if language == "ur":
            return "معذرت، میں آپ کی بات نہیں سمجھا۔ میں آپ کی مدد کر سکتا ہوں: کام شامل کریں، کام دکھائیں، مکمل کریں، حذف کریں، یا اپ ڈیٹ کریں۔"
        else:
            return "I didn't understand that. I can help you: add, list, complete, delete, or update tasks, and get your account information."

    else:
        if language == "ur":
            return "یہ فیچر دستیاب نہیں ہے۔"
        else:
            return "This feature is not available."


def get_conversation_history(
    session: Session,
    user_id: str,
    conversation_id: UUID,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Retrieve conversation history for display in chat UI

    Args:
        session: Database session
        user_id: User ID (for user isolation)
        conversation_id: Conversation ID
        limit: Maximum number of messages to retrieve (default: 100)

    Returns:
        Dictionary with messages array and conversation metadata
    """
    try:
        # Get conversation with user isolation
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            return {
                "success": False,
                "error": "Conversation not found"
            }

        # Get messages for this conversation
        messages_statement = select(ChatMessage).where(
            ChatMessage.conversation_id == conversation_id,
            ChatMessage.user_id == user_id
        ).order_by(ChatMessage.created_at.asc()).limit(limit)

        messages = session.exec(messages_statement).all()

        # Format messages for response
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "id": str(msg.id),
                "sender": msg.sender.value,
                "message": msg.message_text,
                "timestamp": msg.created_at.isoformat()
            })

        return {
            "success": True,
            "conversation_id": str(conversation.id),
            "messages": formatted_messages,
            "count": len(formatted_messages)
        }

    except Exception as e:
        print(f"[ERROR] Failed to get conversation history: {type(e).__name__}: {e}")

        return {
            "success": False,
            "error": str(e)
        }
