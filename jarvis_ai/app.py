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
from agents.planner_agent import generate_plan
from agents.executor_agent import execute_plan


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
            
            if category == "CHAT":
                chat_model = FallbackGenerativeModel(
                    "gemini-2.5-flash", "gemini-2.5-flash-lite",
                    system_instruction=SYSTEM_PROMPT
                )
                chat = chat_model.start_chat(history=conversation_history)
                response = chat.send_message(user_input)
                print(f"\nAURORA: {response.text}")
                conversation_history = chat.history
                continue
                
            print("AURORA is generating a multi-step execution plan...")
            # We explicitly declare the system's modular arsenal
            available_tools_string = "research_advanced, calendar_google, code_advanced, rag_tool"
            
            # Extract the last few turns of dialogue so the Planner has full conversational context
            context_string = "\n".join([f"{msg.role}: {msg.parts[0].text}" for msg in conversation_history[-4:]]) if conversation_history else ""
            enhanced_input = f"{context_string}\nUser Goal: {user_input}" if context_string else user_input
            
            plan = generate_plan(enhanced_input, intent_model, available_tools_info=available_tools_string)
            print(f"Plan Summary: {plan.get('plan_summary')}")
            
            print("AURORA is executing the plan autonomously...")
            final_result = execute_plan(plan, system_prompt=SYSTEM_PROMPT)
            
            print(f"\nAURORA: {final_result}")
            
            # Seamlessly ingest the complex interaction back into the short-term conversational history 
            # so the agent remembers what it just did!
            conversation_history.append({'role': 'user', 'parts': [{'text': user_input}]})
            conversation_history.append({'role': 'model', 'parts': [{'text': final_result}]})

        except KeyboardInterrupt:
            print("\nAURORA shutting down...")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()