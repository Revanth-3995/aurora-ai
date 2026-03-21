import os
import sys
from pathlib import Path
from datetime import datetime
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

from agents.planner_agent import generate_plan
from agents.executor_agent import execute_plan
from config.settings import GEMINI_API_KEY

def test_executor_agent():
    print("🤖 Testing Full End-to-End Orchestration (Planner -> Executor)...")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("❌ ERROR: Please set GEMINI_API_KEY in .env")
        sys.exit(1)
        
    genai.configure(api_key=GEMINI_API_KEY)
    
    SYSTEM_PROMPT = f"You are AURORA-AI. The current system date and time is {datetime.now().strftime('%A, %B %d, %Y %I:%M %p %Z')}."
    model = FallbackGenerativeModel("gemini-2.5-flash", "gemini-2.5-flash-lite", system_instruction=SYSTEM_PROMPT)
    
    complex_prompt = "Research the latest stock price of NVIDIA and then schedule a 15-minute 'Buy Evaluation' meeting for me tomorrow at 10 AM IST."
    
    print(f"\nUser Objective: '{complex_prompt}'\n")
    
    print("1️⃣ Invoking Planner Agent...")
    plan = generate_plan(complex_prompt, model, available_tools_info="research_advanced, calendar_google")
    print(f"Plan Generated: {plan.get('plan_summary')} ({len(plan.get('steps', []))} steps)\n")
    
    print("2️⃣ Invoking Executor Agent...")
    final_result = execute_plan(plan, system_prompt=SYSTEM_PROMPT)
    
    print("\n✅ Final Aggregated Output:")
    print("-" * 50)
    print(final_result)
    print("-" * 50)

if __name__ == "__main__":
    test_executor_agent()
