import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai

# Load env
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Available models in priority order
MODELS = [
    "gemini-2.5-flash",       # main
    "gemini-2.5-flash-lite",  # fast backup
    "gemini-1.5-flash",       # stable fallback
    "gemini-1.5-flash-8b"     # last resort
]

def generate_response(prompt):
    for model in MODELS:
        try:
            print(f"Trying {model}...")
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            print(f"❌ {model} failed: {e}")

    return "⚠️ All models are currently unavailable. Please try again later."

# Test
print(generate_response("Say hello"))