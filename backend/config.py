import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for backend
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env if present
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Base application configuration."""
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"
    PORT = int(os.getenv("PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "algoquest-default-insecure-key")
    
    # MongoDB Atlas settings
    MONGO_URI = os.getenv("MONGO_URI", "").strip()
    DB_NAME = os.getenv("DB_NAME", "algoquest").strip()
    
    # Connection timeouts (milliseconds)
    MONGO_CONNECT_TIMEOUT_MS = int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", 3000))
    MONGO_SERVER_SELECTION_TIMEOUT_MS = int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", 3000))

    # AI Coach Configuration
    AI_ENABLED = os.getenv("AI_ENABLED", "true").strip().lower() in ("true", "1", "yes")
    AI_API_KEY = os.getenv("AI_API_KEY", os.getenv("GEMINI_API_KEY", "")).strip()
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").strip().lower()
    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "gemini-1.5-flash").strip()
    AI_TIMEOUT_SECONDS = int(os.getenv("AI_TIMEOUT_SECONDS", 5))
    AI_MAX_INPUT_CHARS = int(os.getenv("AI_MAX_INPUT_CHARS", 1000))
