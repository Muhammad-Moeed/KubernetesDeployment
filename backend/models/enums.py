"""
Enumerations for Task Model
Defines all enum types used in the database models
"""
from enum import Enum


class PriorityLevel(str, Enum):
    """
    Task priority levels

    Stored as string values in database: "high", "medium", "low"
    String-based enum for better JSON serialization and readability
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
