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

from agents.planner_agent import generate_plan
from config.settings import GEMINI_API_KEY

def test_planner_agent():
    print("🗺️ Testing Planner Agent Decomposition...")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("❌ ERROR: Please set GEMINI_API_KEY in .env")
        sys.exit(1)
        
    genai.configure(api_key=GEMINI_API_KEY)
    model = FallbackGenerativeModel("gemini-2.5-flash", "gemini-2.5-flash-lite")
    
    complex_prompt = "Research the latest news on agentic AI frameworks from 2025, and then schedule a 2-hour study block for me tomorrow at 4 PM IST to review the findings."
    
    print(f"\nUser Input: '{complex_prompt}'\n")
    
    result = generate_plan(complex_prompt, model, available_tools_info="research_advanced, calendar_google")
    
    print(f"Plan Summary: {result.get('plan_summary')}\n")
    
    steps = result.get('steps', [])
    for step in steps:
        print(f"Step {step.get('step_number')}:")
        print(f"  Tool: {step.get('target_tool')}")
        print(f"  Instruction: {step.get('instruction')}")
        print(f"  Expected Outcome: {step.get('expected_outcome')}")
        print(f"  Depends On: {step.get('depends_on')}\n")

if __name__ == "__main__":
    test_planner_agent()
