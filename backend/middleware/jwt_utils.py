"""
JWT Utility Functions
Functions for decoding and verifying JWT tokens issued by Better Auth
"""
from jose import jwt, JWTError
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get JWT secret from environment (must match frontend Better Auth secret)
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

# JWT algorithm (Better Auth uses HS256 by default)
ALGORITHM = "HS256"


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token and return its payload without verification.

    Args:
        token: JWT token string

    Returns:
        Dictionary containing token payload, or None if decoding fails

    Note: This function does NOT verify the token signature or expiration.
    Use verify_token() for secure token validation.
    """
    try:
        # Decode without verification (for debugging only)
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM],
            options={"verify_signature": False, "verify_exp": False}
        )
        return payload
    except JWTError as e:
        print(f"JWT decode error: {e}")
        return None


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token's signature and expiration, then return its payload.

    This function:
    1. Verifies the token signature using BETTER_AUTH_SECRET
    2. Checks if the token has expired
    3. Returns the payload if valid, None otherwise

    Args:
        token: JWT token string

    Returns:
        Dictionary containing token payload if valid, None otherwise

    Raises:
        JWTError: If token is invalid, expired, or signature verification fails
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except JWTError as e:
        print(f"JWT verification error: {e}")
        return None


def extract_user_id(payload: Dict[str, Any]) -> Optional[str]:
    """
    Extract user_id from JWT payload.

    Better Auth tokens typically include:
    - "sub" (subject): User ID
    - "userId": User ID (alternative field)
    - "user_id": User ID (alternative field)

    This function checks all common fields and returns the user ID.

    Args:
        payload: Decoded JWT payload dictionary

    Returns:
        User ID string if found, None otherwise
    """
    if not payload:
        return None

    # Check common JWT user ID fields
    user_id = (
        payload.get("sub") or
        payload.get("userId") or
        payload.get("user_id") or
        payload.get("id")
    )

    return user_id


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Convenience function to verify token and extract user_id in one step.

    Args:
        token: JWT token string

    Returns:
        User ID string if token is valid, None otherwise
    """
    payload = verify_token(token)
    if not payload:
        return None
    return extract_user_id(payload)


def validate_token_and_user(token: str, expected_user_id: str) -> bool:
    """
    Validate that token is valid and matches the expected user_id.

    This is the primary function for user isolation enforcement.
    Use this to ensure authenticated user matches the path parameter user_id.

    Args:
        token: JWT token string
        expected_user_id: User ID from URL path parameter

    Returns:
        True if token is valid AND user_id matches, False otherwise
    """
    user_id = extract_user_id_from_token(token)
    if not user_id:
        return False
    return user_id == expected_user_id
