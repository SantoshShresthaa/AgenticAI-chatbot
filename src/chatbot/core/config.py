import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Basic configuration
class Config:
    """Basic configuration class."""

    # LLM Settings
    OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
    OPEN_ROUTER_BASE_URL = os.getenv("OPEN_ROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    OPEN_ROUTER_MODEL = os.getenv("OPEN_ROUTER_MODEL", "openai/gpt-oss-20b:free")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Global config instance
config = Config()