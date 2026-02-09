"""
Pydantic Schemas for Request/Response Validation
Request models for creating and updating tasks
Response models for API responses
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from .enums import PriorityLevel


class TaskCreateRequest(BaseModel):
    """
    Request model for creating a new task (POST /api/{user_id}/tasks)

    Required:
    - title: Non-empty string, max 500 characters

    Optional:
    - description: Max 10,000 characters
    - priority: One of "high", "medium", "low" (default: "medium")
    - tags: Array of strings, max 20 tags, each max 50 characters
    - due_date: ISO 8601 datetime
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title (required, 1-500 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=10000,
        description="Optional detailed description (max 10,000 characters)"
    )
    priority: PriorityLevel = Field(
        default=PriorityLevel.MEDIUM,
        description="Priority level: high, medium, or low (default: medium)"
    )
    tags: Optional[List[str]] = Field(
        None,
        max_length=20,
        description="Array of tag strings (max 20 tags, each max 50 characters)"
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Optional deadline date/time (ISO 8601 format)"
    )

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace only"""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()

    @field_validator('description')
    @classmethod
    def description_strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip leading/trailing whitespace from description"""
        if v is None:
            return None
        return v.strip() if v.strip() else None

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """
        Validate tags:
        - Filter out empty strings
        - Remove duplicates
        - Trim whitespace
        - Limit to 50 characters each
        """
        if v is None:
            return None

        # Strip whitespace and filter empty strings
        cleaned_tags = [tag.strip() for tag in v if tag and tag.strip()]

        # Validate each tag length
        for tag in cleaned_tags:
            if len(tag) > 50:
                raise ValueError("Each tag must be 50 characters or less")

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in cleaned_tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        # Check max 20 tags
        if len(unique_tags) > 20:
            raise ValueError("Maximum 20 tags allowed")

        return unique_tags if unique_tags else None

    @field_validator('priority', mode='before')
    @classmethod
    def priority_case_insensitive(cls, v):
        """Allow case-insensitive priority values"""
        if isinstance(v, str):
            return v.lower()
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, bread, eggs, cheese",
                "priority": "high",
                "tags": ["home", "shopping", "urgent"],
                "due_date": "2026-01-10T18:00:00Z"
            }
        }
    }


class TaskUpdateRequest(BaseModel):
    """
    Request model for updating an existing task (PUT /api/{user_id}/tasks/{task_id})

    All fields are optional for partial updates.
    Only provided fields will be updated.
    """
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Updated task title (1-500 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=10000,
        description="Updated description (max 10,000 characters)"
    )
    priority: Optional[PriorityLevel] = Field(
        None,
        description="Updated priority level: high, medium, or low"
    )
    tags: Optional[List[str]] = Field(
        None,
        max_length=20,
        description="Updated array of tag strings (max 20 tags)"
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Updated deadline date/time (ISO 8601 format)"
    )
    completed: Optional[bool] = Field(
        None,
        description="Updated completion status (true = completed, false = pending)"
    )

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace only"""
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Title cannot be empty or whitespace only")
            return v.strip()
        return v

    @field_validator('description')
    @classmethod
    def description_strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip leading/trailing whitespace from description"""
        if v is None:
            return None
        return v.strip() if v.strip() else None

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """
        Validate tags:
        - Filter out empty strings
        - Remove duplicates
        - Trim whitespace
        - Limit to 50 characters each
        """
        if v is None:
            return None

        # Strip whitespace and filter empty strings
        cleaned_tags = [tag.strip() for tag in v if tag and tag.strip()]

        # Validate each tag length
        for tag in cleaned_tags:
            if len(tag) > 50:
                raise ValueError("Each tag must be 50 characters or less")

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in cleaned_tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        # Check max 20 tags
        if len(unique_tags) > 20:
            raise ValueError("Maximum 20 tags allowed")

        return unique_tags if unique_tags else None

    @field_validator('priority', mode='before')
    @classmethod
    def priority_case_insensitive(cls, v):
        """Allow case-insensitive priority values"""
        if isinstance(v, str):
            return v.lower()
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries (updated)",
                "completed": True
            }
        }
    }


class TaskResponse(BaseModel):
    """
    Response model for task objects
    Used in all endpoints that return task data
    """
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str  # "high", "medium", or "low"
    tags: Optional[List[str]]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,  # Allow creation from SQLModel objects (ORM mode)
        "json_schema_extra": {
            "example": {
                "id": 123,
                "user_id": "user_abc123",
                "title": "Buy groceries",
                "description": "Milk, bread, eggs, cheese",
                "completed": False,
                "priority": "high",
                "tags": ["home", "shopping", "urgent"],
                "due_date": "2026-01-10T18:00:00Z",
                "created_at": "2026-01-05T10:30:00Z",
                "updated_at": "2026-01-05T10:30:00Z"
            }
        }
    }


class ErrorResponse(BaseModel):
    """
    Standard error response model
    Used for all error responses (400, 401, 403, 404, 500)
    """
    error: str = Field(
        ...,
        description="Error message (English)"
    )
    detail: Optional[str] = Field(
        None,
        description="Optional detailed explanation"
    )
    error_urdu: Optional[str] = Field(
        None,
        description="Error message in Urdu (اردو)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "Task not found",
                "detail": "No task with ID 999 exists for this user",
                "error_urdu": "ٹاسک نہیں ملا"
            }
        }
    }


# Urdu Error Message Translations
URDU_TRANSLATIONS = {
    "Task not found": "ٹاسک نہیں ملا",
    "Invalid priority value": "غلط ترجیح کی قیمت",
    "Title is required": "عنوان ضروری ہے",
    "Invalid user ID": "غلط صارف کی شناخت",
    "Database connection failed": "ڈیٹا بیس کنکشن ناکام",
    "Task created successfully": "ٹاسک کامیابی سے بنایا گیا",
    "Task updated successfully": "ٹاسک کامیابی سے اپ ڈیٹ کیا گیا",
    "Task deleted successfully": "ٹاسک کامیابی سے حذف کیا گیا",
    "Authentication required": "تصدیق ضروری ہے",
    "Access denied": "رسائی مسترد",
    "Invalid date format": "غلط تاریخ کی شکل",
    "Server error": "سرور کی خرابی",
    "Invalid request": "غلط درخواست",
    "Title cannot be empty": "عنوان خالی نہیں ہو سکتا",
    "Invalid token": "غلط ٹوکن",
    "Token expired": "ٹوکن کی میعاد ختم",
    "User ID mismatch": "صارف کی شناخت میں فرق"
}
