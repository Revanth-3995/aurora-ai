import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file with override
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Configuration validations
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    print("WARNING: GEMINI_API_KEY is not set or is using the default template value.")

if not TAVILY_API_KEY or TAVILY_API_KEY == "your_tavily_api_key_here":
    print("WARNING: TAVILY_API_KEY is not set or is using the default template value.")
