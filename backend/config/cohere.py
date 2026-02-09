"""
Cohere API Configuration
OpenAI Agents SDK configured with Cohere as LLM provider (Phase 3 AI Chatbot)
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Cohere API key from environment
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize OpenAI client with Cohere base URL
# Note: Will use placeholder key during development if not set
if not COHERE_API_KEY or COHERE_API_KEY == "eRRBLe3NVQMYgaB4rt865J0gaUaAgNRz1abXNLCR":
    print("[WARNING] COHERE_API_KEY not set or using placeholder. Chat features will not work.")
    print("[WARNING] Get your API key from: https://dashboard.cohere.com/api-keys")
    COHERE_API_KEY = "placeholder_key_for_development"

cohere_client = OpenAI(
    api_key=COHERE_API_KEY,
    base_url="https://api.cohere.ai/v1"
)

# Cohere model configuration
COHERE_MODEL = "command-r-plus"  # Best model for tool use and multilingual support
COHERE_MAX_TOKENS = 1000  # Maximum tokens in response
COHERE_TEMPERATURE = 0.7  # Creativity level (0.0 = deterministic, 1.0 = creative)

# Timeout configuration
COHERE_TIMEOUT = 30  # API request timeout in seconds

print(f"[OK] Cohere API configured with model: {COHERE_MODEL}")
