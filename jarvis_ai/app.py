"""
AURORA chat with tools: uses only google-generativeai (no LangChain).
"""
import sys
import time
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
from config.settings import GEMINI_API_KEY
from tools_agent import get_gemini_tools


def main() -> None:
    print("Initializing AURORA Tool-Enabled Chat...")

    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("❌ ERROR: Please set your GEMINI_API_KEY in the .env file.")
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)

    tools = get_gemini_tools()
    if not tools:
        print("⚠️  No tools enabled. Set env flags: ENABLE_GOOGLE_CALENDAR, ENABLE_ADVANCED_CODE_TOOL, ENABLE_ADVANCED_RESEARCH_TOOL")

    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            tools=tools,
        )
        chat = model.start_chat(
            history=[],
            enable_automatic_function_calling=True,
        )
    except Exception as e:
        print(f"❌ Failed to create model or chat: {e}")
        sys.exit(1)

    print("✅ AURORA is ready with tools. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                print("AURORA: Please enter a valid message. (Input cannot be empty)")
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("AURORA shutting down...")
                break

            print("AURORA is thinking (and may call tools)...")

            max_retries = 3
            retry_delay = 2
            last_error = None

            for attempt in range(max_retries):
                try:
                    response = chat.send_message(user_input, tools=tools)
                    text = response.text
                    print(f"\nAURORA: {text}")
                    last_error = None
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