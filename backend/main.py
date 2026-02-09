"""
FastAPI Main Application
Multi-User Todo Backend API with JWT Authentication
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database initialization
from database.init_db import create_db_and_tables

# Import routes
from routes import tasks, chat

# Import error response model
from models.schemas import ErrorResponse, URDU_TRANSLATIONS

# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="Multi-user Todo application with JWT authentication and user isolation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "tasks",
            "description": "Task management operations with user isolation"
        },
        {
            "name": "chat",
            "description": "AI chatbot chat operations with natural language processing"
        },
        {
            "name": "health",
            "description": "Health check and status endpoints"
        }
    ]
)

# CORS Configuration - ALLOW ALL ORIGINS
# This allows requests from any origin (debugging mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    max_age=86400  # Cache preflight requests for 24 hours
)


# Startup Event: Initialize Database
@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Initializes database tables and indexes.
    """
    print("=" * 50)
    print("Starting Todo API...")
    print("=" * 50)

    try:
        # Create database tables and indexes
        create_db_and_tables()
        print("[OK] Database initialization successful")
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        print("[WARNING] Application may not function correctly")

    print("=" * 50)
    print("Todo API started successfully")
    print(f"Documentation available at: /docs")
    print("=" * 50)


# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    Cleanup operations before shutdown.
    """
    print("=" * 50)
    print("Shutting down Todo API...")
    print("=" * 50)


# Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors (422 Unprocessable Entity).
    Returns structured error response with details.
    """
    errors = exc.errors()
    error_messages = []
    for error in errors:
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid request",
            "error_urdu": URDU_TRANSLATIONS.get("Invalid request"),
            "detail": "; ".join(error_messages)
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected server errors (500 Internal Server Error).
    Returns structured error response without exposing internal details.
    """
    print(f"Unexpected error: {type(exc).__name__}: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Server error",
            "error_urdu": URDU_TRANSLATIONS.get("Server error"),
            "detail": "An unexpected error occurred. Please try again later."
        }
    )


# Health check endpoints
@app.get("/", tags=["health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "healthy",
        "message": "Todo API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "JWT Authentication",
            "User Isolation",
            "Task CRUD Operations",
            "Advanced Filtering",
            "Sorting",
            "Urdu Translations",
            "AI Chatbot (Phase 3)"
        ]
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "ok",
        "database": "connected",
        "version": "1.0.0"
    }


# Mount task routes
app.include_router(
    tasks.router,
    prefix="/api",
    tags=["tasks"]
)

# Mount chat routes (Phase 3 AI Chatbot)
app.include_router(
    chat.router,
    prefix="/api",
    tags=["chat"]
)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )
