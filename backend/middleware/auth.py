"""
JWT Authentication Middleware
FastAPI dependency for verifying JWT tokens and enforcing user isolation
"""
from fastapi import Header, HTTPException, status, Depends
from typing import Optional, Annotated
from .jwt_utils import verify_token, extract_user_id, validate_token_and_user
from models.schemas import URDU_TRANSLATIONS


class AuthenticatedUser:
    """
    Represents an authenticated user extracted from JWT token.
    Used as dependency injection result.
    """
    def __init__(self, user_id: str, token_payload: dict):
        self.user_id = user_id
        self.payload = token_payload

    def __str__(self):
        return f"AuthenticatedUser(user_id={self.user_id})"


async def verify_jwt_token(
    authorization: Annotated[Optional[str], Header()] = None
) -> AuthenticatedUser:
    """
    FastAPI dependency to verify JWT token from Authorization header.

    This dependency:
    1. Extracts Bearer token from Authorization header
    2. Verifies token signature using BETTER_AUTH_SECRET
    3. Checks token expiration
    4. Extracts user_id from token payload
    5. Returns AuthenticatedUser object

    Usage in routes:
        @router.get("/tasks")
        async def get_tasks(
            user: AuthenticatedUser = Depends(verify_jwt_token)
        ):
            user_id = user.user_id
            # ...

    Args:
        authorization: Authorization header value (injected by FastAPI)

    Returns:
        AuthenticatedUser object containing user_id and token payload

    Raises:
        HTTPException 401: If token is missing, invalid, or expired
    """
    # Check if Authorization header is present
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Authentication required",
                "error_urdu": URDU_TRANSLATIONS.get("Authentication required"),
                "detail": "Missing Authorization header"
            }
        )

    # Extract Bearer token
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid token format",
                "error_urdu": URDU_TRANSLATIONS.get("Invalid token"),
                "detail": "Authorization header must be: Bearer <token>"
            }
        )

    token = parts[1]

    # Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid or expired token",
                "error_urdu": URDU_TRANSLATIONS.get("Token expired"),
                "detail": "JWT token is invalid or has expired"
            }
        )

    # Extract user_id from payload
    user_id = extract_user_id(payload)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid token payload",
                "error_urdu": URDU_TRANSLATIONS.get("Invalid token"),
                "detail": "Token does not contain user ID"
            }
        )

    return AuthenticatedUser(user_id=user_id, token_payload=payload)


async def verify_user_id_match(
    path_user_id: str,
    user: AuthenticatedUser = Depends(verify_jwt_token)
) -> AuthenticatedUser:
    """
    FastAPI dependency to verify that JWT user_id matches path parameter user_id.

    This enforces user isolation by ensuring authenticated user can only access
    their own resources.

    Usage in routes:
        @router.get("/{user_id}/tasks")
        async def get_tasks(
            user_id: str,
            user: AuthenticatedUser = Depends(verify_user_id_match)
        ):
            # user.user_id is guaranteed to match user_id from path
            # ...

    Args:
        path_user_id: User ID from URL path parameter
        user: Authenticated user from JWT (dependency)

    Returns:
        AuthenticatedUser object if user_id matches

    Raises:
        HTTPException 403: If JWT user_id doesn't match path user_id
    """
    if user.user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied",
                "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                "detail": "You can only access your own resources"
            }
        )

    return user


def create_user_verifier(path_user_id: str):
    """
    Factory function to create a user ID verification dependency.

    This is a convenience function for creating a dependency that verifies
    both JWT authentication and user_id match in one step.

    Args:
        path_user_id: User ID from URL path parameter

    Returns:
        Dependency function that verifies JWT and user_id match
    """
    async def verify():
        user = await verify_jwt_token()
        if user.user_id != path_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Access denied",
                    "error_urdu": URDU_TRANSLATIONS.get("Access denied"),
                    "detail": "User ID mismatch"
                }
            )
        return user

    return Depends(verify)


# Optional: Rate limiting decorator (future enhancement)
def require_auth():
    """
    Simplified decorator for requiring authentication.
    Returns the verify_jwt_token dependency.
    """
    return Depends(verify_jwt_token)
