import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from llm_wrapper import FallbackGenerativeModel

# Setup paths
_here = Path(__file__).resolve().parent
_root = _here.parent
for _p in [str(_here), str(_root)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

load_dotenv(dotenv_path=_here / ".env", override=True)

from agents.intent_agent import classify_intent
from config.settings import GEMINI_API_KEY

def test_intent_agent():
    print("🧠 Testing Intent Agent Classification...")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("❌ ERROR: Please set GEMINI_API_KEY in .env")
        sys.exit(1)
        
    genai.configure(api_key=GEMINI_API_KEY)
    model = FallbackGenerativeModel("gemini-2.5-flash", "gemini-2.5-flash-lite")
    
    test_prompts = [
        "Hello, how are you today?",
        "Schedule a meeting for tomorrow at 2 PM.",
        "What is the current stock price of Apple?",
        "Compute the first 50 digits of pi using Python.",
        "Summarize the information from the notes I uploaded."
    ]
    
    for prompt in test_prompts:
        print(f"\nUser Input: '{prompt}'")
        result = classify_intent(prompt, model)
        print(f"Classification: {result.get('category')}")
        print(f"Reasoning: {result.get('reasoning')}")

if __name__ == "__main__":
    test_intent_agent()
