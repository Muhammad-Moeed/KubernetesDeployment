"""
Intent Parser Service
Uses Cohere API (via OpenAI SDK) to parse natural language messages and detect intent
"""
from typing import Dict, Any, Optional
import json
from config.cohere import cohere_client, COHERE_MODEL, COHERE_MAX_TOKENS, COHERE_TEMPERATURE


def parse_intent(message: str, language: str = "en") -> Dict[str, Any]:
    """
    Parse natural language message to detect intent and extract parameters

    This function uses Cohere's command-r-plus model via OpenAI SDK to analyze
    user messages and determine what action they want to perform.

    Args:
        message: User's natural language message
        language: Language code ("en" for English, "ur" for Urdu)

    Returns:
        Dictionary with intent, parameters, confidence, and language

    Example Response:
        {
            "intent": "add_task",
            "parameters": {
                "title": "buy groceries",
                "priority": "medium",
                "due_date": None
            },
            "confidence": 0.95,
            "language": "en"
        }

    Supported Intents:
        - add_task: Create a new task
        - list_tasks: Retrieve tasks
        - complete_task: Mark task as done
        - delete_task: Remove task
        - update_task: Modify task
        - get_user_info: Retrieve user information
        - unknown: Unrecognized intent
    """
    try:
        # Detect language if not specified
        if language == "en" and _contains_urdu(message):
            language = "ur"

        # Build system prompt for intent detection
        system_prompt = _build_system_prompt(language)

        # Call Cohere API via OpenAI SDK
        response = cohere_client.chat.completions.create(
            model=COHERE_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=COHERE_MAX_TOKENS,
            temperature=COHERE_TEMPERATURE
        )

        # Extract response content
        response_text = response.choices[0].message.content.strip()

        # Parse JSON response from Cohere
        try:
            parsed_response = json.loads(response_text)
        except json.JSONDecodeError:
            # If Cohere doesn't return valid JSON, try to extract intent manually
            parsed_response = _fallback_intent_detection(message, language)

        # Validate and normalize response
        intent_data = {
            "intent": parsed_response.get("intent", "unknown"),
            "parameters": parsed_response.get("parameters", {}),
            "confidence": parsed_response.get("confidence", 0.5),
            "language": language
        }

        return intent_data

    except Exception as e:
        print(f"[ERROR] Intent parsing failed: {type(e).__name__}: {e}")

        # Fallback to keyword-based detection on Cohere API failure
        fallback_result = _fallback_intent_detection(message, language)

        # Add error information
        fallback_result["error"] = str(e)
        fallback_result["fallback_used"] = True

        return fallback_result


def _build_system_prompt(language: str) -> str:
    """
    Build system prompt for Cohere to detect intent and extract parameters

    Args:
        language: Language code ("en" or "ur")

    Returns:
        System prompt string
    """
    if language == "ur":
        return """You are an AI assistant that analyzes Urdu messages to detect user intent for a todo task management system.

Analyze the user's message and respond with ONLY a JSON object (no other text) with this structure:
{
    "intent": "add_task|list_tasks|complete_task|delete_task|update_task|get_user_info|unknown",
    "parameters": {
        "title": "task title (for add_task)",
        "description": "task description (optional)",
        "priority": "low|medium|high (default: medium)",
        "due_date": "YYYY-MM-DD format (optional)",
        "task_id": "task ID number (for complete/delete/update)",
        "status_filter": "pending|completed (for list_tasks)",
        "query_type": "email|name|user_id|all (for get_user_info)"
    },
    "confidence": 0.0-1.0
}

Intent Detection Rules:
- "ٹاسک شامل کریں", "نیا کام", "یاد دلائیں" → add_task
- "تمام کام دکھاؤ", "ٹاسک لسٹ", "کام دکھائیں" → list_tasks
- "ٹاسک مکمل کریں", "کام ہو گیا", "ختم کریں" → complete_task
- "ٹاسک حذف کریں", "کام ہٹائیں" → delete_task
- "ٹاسک تبدیل کریں", "ترجیح تبدیل کریں" → update_task
- "میری ای میل", "میرا نام", "میں کون ہوں" → get_user_info
- Otherwise → unknown

Extract parameters from the message context. Return ONLY the JSON object."""

    else:  # English
        return """You are an AI assistant that analyzes English messages to detect user intent for a todo task management system.

Analyze the user's message and respond with ONLY a JSON object (no other text) with this structure:
{
    "intent": "add_task|list_tasks|complete_task|delete_task|update_task|get_user_info|unknown",
    "parameters": {
        "title": "task title (for add_task)",
        "description": "task description (optional)",
        "priority": "low|medium|high (default: medium)",
        "due_date": "YYYY-MM-DD format (optional)",
        "task_id": "task ID number (for complete/delete/update)",
        "status_filter": "pending|completed (for list_tasks)",
        "query_type": "email|name|user_id|all (for get_user_info)"
    },
    "confidence": 0.0-1.0
}

Intent Detection Rules:
- "add task", "create task", "new task", "I need to", "remind me to" → add_task
- "show tasks", "list tasks", "what are my tasks", "my tasks" → list_tasks
- "mark task as done", "complete task", "finish task", "task is done" → complete_task
- "delete task", "remove task", "cancel task" → delete_task
- "update task", "change task", "modify task", "set priority" → update_task
- "what's my email", "what's my name", "who am I", "my account" → get_user_info
- Otherwise → unknown

Priority Detection:
- "high", "urgent", "important" → high
- "low" → low
- Default → medium

Extract parameters from the message context. Return ONLY the JSON object."""


def _contains_urdu(text: str) -> bool:
    """
    Check if text contains Urdu characters

    Args:
        text: Text to check

    Returns:
        True if text contains Urdu characters, False otherwise
    """
    # Urdu Unicode range: U+0600 to U+06FF (Arabic/Urdu script)
    for char in text:
        if '\u0600' <= char <= '\u06FF':
            return True
    return False


def _fallback_intent_detection(message: str, language: str) -> Dict[str, Any]:
    """
    Fallback intent detection using simple keyword matching

    This is used when Cohere doesn't return valid JSON or API fails.

    Args:
        message: User message
        language: Language code

    Returns:
        Dictionary with intent and parameters
    """
    message_lower = message.lower()

    # English keyword matching
    if language == "en":
        if any(keyword in message_lower for keyword in ["add task", "create task", "new task", "remind me", "add ", "task add"]):
            # Extract title after common patterns
            title = message_lower.replace("add task", "").replace("create task", "").replace("new task", "").replace("remind me to", "").replace("add ", "").replace("task add", "").strip()
            return {
                "intent": "add_task",
                "parameters": {"title": title or "New task", "priority": "medium"},
                "confidence": 0.6
            }

        if any(keyword in message_lower for keyword in ["show tasks", "list tasks", "my tasks", "what are my tasks", "all tasks", "get tasks", "show all", "list"]):
            return {
                "intent": "list_tasks",
                "parameters": {},
                "confidence": 0.7
            }

        if any(keyword in message_lower for keyword in ["complete task", "mark task", "finish task", "done", "complete", "mark done"]):
            # Try to extract task ID
            import re
            task_id_match = re.search(r'\d+', message)
            task_id = int(task_id_match.group()) if task_id_match else None
            return {
                "intent": "complete_task",
                "parameters": {"task_id": task_id},
                "confidence": 0.6
            }

        if any(keyword in message_lower for keyword in ["delete task", "remove task", "cancel task", "delete ", "remove", "dlete task"]):
            import re
            task_id_match = re.search(r'\d+', message)
            task_id = int(task_id_match.group()) if task_id_match else None
            return {
                "intent": "delete_task",
                "parameters": {"task_id": task_id},
                "confidence": 0.6
            }

        if any(keyword in message_lower for keyword in ["update task", "change task", "edit task", "rename task", "update", "upgrade", "updatge"]):
            import re
            task_id_match = re.search(r'\d+', message)
            task_id = int(task_id_match.group()) if task_id_match else None
            
            # Extract new title (anything after "to" or "title" or just the rest of message)
            new_title = message_lower
            for pattern in ["update task", "change task", "edit task", "rename task", "update", "upgrade", "updatge"]:
                new_title = new_title.replace(pattern, "")
            
            for keyword in ["to title", "title", "to", "with"]:
                if keyword in new_title:
                    new_title = new_title.split(keyword)[-1].strip()
                    break
            
            return {
                "intent": "update_task",
                "parameters": {"task_id": task_id, "title": new_title or "Updated task"},
                "confidence": 0.6
            }

        if any(keyword in message_lower for keyword in ["my email", "my name", "who am i", "account info", "user info", "profile"]):
            query_type = "email" if "email" in message_lower else "name" if "name" in message_lower else "all"
            return {
                "intent": "get_user_info",
                "parameters": {"query_type": query_type},
                "confidence": 0.7
            }

    # Urdu keyword matching
    elif language == "ur":
        if "ٹاسک شامل" in message or "نیا کام" in message:
            return {
                "intent": "add_task",
                "parameters": {"title": "نیا کام", "priority": "medium"},
                "confidence": 0.6
            }

        if "کام دکھاؤ" in message or "ٹاسک لسٹ" in message or "سب کام" in message:
            return {
                "intent": "list_tasks",
                "parameters": {},
                "confidence": 0.7
            }

        if "مکمل کریں" in message or "ختم کریں" in message:
            import re
            task_id_match = re.search(r'\d+', message)
            task_id = int(task_id_match.group()) if task_id_match else None
            return {
                "intent": "complete_task",
                "parameters": {"task_id": task_id},
                "confidence": 0.6
            }

        if "حذف کریں" in message or "کام ہٹائیں" in message:
            import re
            task_id_match = re.search(r'\d+', message)
            task_id = int(task_id_match.group()) if task_id_match else None
            return {
                "intent": "delete_task",
                "parameters": {"task_id": task_id},
                "confidence": 0.6
            }

        if "تبدیل کریں" in message or "اپڈیٹ کریں" in message or "نام تبدیل" in message:
            import re
            task_id_match = re.search(r'\d+', message)
            task_id = int(task_id_match.group()) if task_id_match else None
            return {
                "intent": "update_task",
                "parameters": {"task_id": task_id, "title": "اپڈیٹ شدہ کام"},
                "confidence": 0.6
            }

        if "میری معلومات" in message or "میرا نام" in message or "میرا ای میل" in message:
            return {
                "intent": "get_user_info",
                "parameters": {"query_type": "all"},
                "confidence": 0.7
            }

    # Unknown intent
    return {
        "intent": "unknown",
        "parameters": {},
        "confidence": 0.3
    }
