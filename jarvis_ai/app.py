"""
AURORA chat with tools: uses only google-generativeai (no LangChain).
"""
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Fix: add both jarvis_ai/ and project root to sys.path ────────────────────
_here = Path(__file__).resolve().parent   # .../agentic_ai_project/jarvis_ai
_root = _here.parent                      # .../agentic_ai_project

for _p in [str(_here), str(_root)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)
# ─────────────────────────────────────────────────────────────────────────────

from dotenv import load_dotenv
load_dotenv(dotenv_path=_here / ".env", override=True)

import google.generativeai as genai
from llm_wrapper import FallbackGenerativeModel
from config.settings import GEMINI_API_KEY
from tools_agent import get_gemini_tools, filter_tools_for_intent
from google.generativeai.types import content_types
from agents.intent_agent import classify_intent


def main() -> None:
    print("Initializing AURORA Tool-Enabled Chat...")

    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("❌ ERROR: Please set your GEMINI_API_KEY in the .env file.")
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)

    tools = get_gemini_tools()
    if not tools:
        print("⚠️  No tools enabled. Set env flags: ENABLE_GOOGLE_CALENDAR, ENABLE_ADVANCED_CODE_TOOL, ENABLE_ADVANCED_RESEARCH_TOOL")

    # We no longer initialize the single `chat` object globally.
    # It is dynamically instantiated per turn based on the filtered Intent tools.
    pass

    print("✅ AURORA is ready with Intent Routing and Tools. Type 'exit' or 'quit' to stop.")

    # We manually manage history to recreate the chat object with specific tools per turn
    conversation_history = []
    
    SYSTEM_PROMPT = f"You are AURORA-AI. The current system date and time is {datetime.now().strftime('%A, %B %d, %Y %I:%M %p %Z')}. Use this exact date as your unshakeable absolute reference for any temporal queries (today, tomorrow, next week). You MUST autonomously infer the user's timezone from this system time (e.g., IST -> Asia/Kolkata). Never ask the user for their timezone."

    # Base model for Intent Classification (no tools)
    intent_model = FallbackGenerativeModel(
        "gemini-2.5-flash", "gemini-2.5-flash-lite", 
        system_instruction=SYSTEM_PROMPT
    )

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                print("AURORA: Please enter a valid message. (Input cannot be empty)")
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("AURORA shutting down...")
                break

            print("AURORA is analyzing intent...")
            intent_dict = classify_intent(user_input, intent_model)
            category = intent_dict.get("category", "CHAT")
            reasoning = intent_dict.get("reasoning", "")
            
            print(f"🧠 Intent Detected: {category} ({reasoning})")
            
            active_tools = filter_tools_for_intent(tools, category)
            tool_count = len(active_tools[0].function_declarations) if active_tools else 0
            
            print(f"AURORA is thinking (routing with {tool_count} enabled tools)...")
            
            # Spin up an exact model clone restricted to ONLY the permitted tools
            turn_model = FallbackGenerativeModel(
                "gemini-2.5-flash", "gemini-2.5-flash-lite",
                tools=active_tools,
                system_instruction=SYSTEM_PROMPT
            )
            chat = turn_model.start_chat(
                history=conversation_history,
                enable_automatic_function_calling=True
            )

            max_retries = 3
            retry_delay = 2
            last_error = None

            for attempt in range(max_retries):
                try:
                    response = chat.send_message(user_input)
                    text = response.text
                    print(f"\nAURORA: {text}")
                    last_error = None
                    # Save the latest history for the next turn
                    conversation_history = chat.history
                    break
                except Exception as api_error:
                    last_error = api_error
                    error_msg = str(api_error).lower()
                    if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                        print(
                            f"⚠️  Rate limit hit. Retrying in {retry_delay}s... "
                            f"(Attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        print(f"❌ Error: {api_error}")
                        break

            if last_error is not None:
                print("❌ Failed after maximum retries. Check your API key and network.")

        except KeyboardInterrupt:
            print("\nAURORA shutting down...")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()