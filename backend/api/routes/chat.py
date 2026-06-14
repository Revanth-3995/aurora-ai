from fastapi import APIRouter, HTTPException
from backend.schemas.api import ChatRequest, ChatResponse
import google.generativeai as genai
from backend.utils.llm_wrapper import FallbackGenerativeModel
from backend.agents.intent_agent import classify_intent
from backend.agents.planner_agent import generate_plan
from backend.agents.executor_agent import execute_plan
from backend.memory.chroma_manager import get_memory_manager
from backend.config.config import settings
from datetime import datetime
import os

router = APIRouter()

BASE_SYSTEM_PROMPT = f"You are AURORA-AI. The current system date and time is {datetime.now().strftime('%A, %B %d, %Y %I:%M %p %Z')}. Use this exact date as your unshakeable absolute reference for any temporal queries (today, tomorrow, next week). You MUST autonomously infer the user's timezone from this system time (e.g., IST -> Asia/Kolkata). Never ask the user for their timezone."

@router.post("", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_gemini_api_key_here":
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured.")

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    user_input = request.message

    try:
        # 1. Long-Term Memory Retrieval
        memory_manager = get_memory_manager()
        retrieved_facts = memory_manager.retrieve_related_memories(user_input, n_results=3)

        dynamic_system_prompt = BASE_SYSTEM_PROMPT
        if retrieved_facts:
            facts_str = "\n".join([f"- {fact}" for fact in retrieved_facts])
            dynamic_system_prompt += f"\n\n[LONG-TERM MEMORY CONTEXT]\nThe following facts are known about the user:\n{facts_str}"

        # 2. Intent Analysis
        intent_model = FallbackGenerativeModel(
            "gemini-2.5-flash", "gemini-2.5-flash-lite",
            system_instruction=dynamic_system_prompt
        )
        intent_dict = classify_intent(user_input, intent_model)
        category = intent_dict.get("category", "CHAT")
        reasoning = intent_dict.get("reasoning", "")

        if category == "CHAT":
            chat_model = FallbackGenerativeModel(
                "gemini-2.5-flash", "gemini-2.5-flash-lite",
                system_instruction=dynamic_system_prompt
            )
            chat = chat_model.start_chat(history=[])
            response = chat.send_message(user_input)

            return ChatResponse(
                response=response.text,
                intent=category,
                tool_used="None",
                reasoning=reasoning,
                workflow=[]
            )

        # 3. Planning
        available_tools_string = "research_advanced, calendar_google, code_advanced, rag_tool, memory_save"
        plan = generate_plan(user_input, intent_model, available_tools_info=available_tools_string)

        # 4. Execution
        final_result, workflow_history = execute_plan(plan, system_prompt=dynamic_system_prompt, capture_workflow=True)

        # Format tools used
        tools_used = list(set([step.get("target_tool", "none") for step in plan.get("steps", [])]))
        tools_str = ", ".join(tools_used) if tools_used else "None"

        return ChatResponse(
            response=final_result,
            intent=category,
            tool_used=tools_str,
            reasoning=reasoning,
            workflow=workflow_history
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
