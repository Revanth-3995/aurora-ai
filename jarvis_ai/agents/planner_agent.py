import json
import logging
from typing import List, Dict, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)

def generate_plan(user_input: str, model: genai.GenerativeModel, available_tools_info: str = "") -> dict:
    """
    Takes a complex user goal and breaks it down into a step-by-step execution plan 
    for the Executor Agent to follow.
    
    Returns a dict containing:
    {
        "plan_summary": "...",
        "steps": [
            {
                "step_number": 1,
                "target_tool": "research_advanced",
                "instruction": "...",
                "expected_outcome": "...",
                "depends_on": []
            }
        ]
    }
    """
    
    # OpenAPI style schema for Gemini JSON structured output
    planner_schema = {
        "type": "object",
        "properties": {
            "plan_summary": {
                "type": "string",
                "description": "A high-level summary of how the agent intends to solve the user's objective."
            },
            "steps": {
                "type": "array",
                "description": "The sequential list of steps to execute.",
                "items": {
                    "type": "object",
                    "properties": {
                        "step_number": {
                            "type": "integer",
                            "description": "The 1-indexed order of execution."
                        },
                        "target_tool": {
                            "type": "string",
                            "description": "The EXACT name of the tool to be used for this step (e.g., 'research_advanced', 'calendar_google', 'code_advanced', 'rag_tool'). Use 'none' if it requires direct LLM reasoning without a tool."
                        },
                        "instruction": {
                            "type": "string",
                            "description": "The exact strict prompt or query to be given to the Executor Agent/Tool for this step."
                        },
                        "expected_outcome": {
                            "type": "string",
                            "description": "What this step must produce before the next step can begin."
                        },
                        "depends_on": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "A list of previous step numbers that must succeed before this step can run. Empty if no dependencies."
                        }
                    },
                    "required": ["step_number", "target_tool", "instruction", "expected_outcome", "depends_on"]
                }
            }
        },
        "required": ["plan_summary", "steps"]
    }

    prompt = f"""
You are the Planner Agent for AURORA-AI. 
Your job is to receive a complex user objective and break it down into an explicit, sequential execution plan.
You must return your output strictly adhering to the JSON schema provided.

The Executor Agent is quite literal and will follow your steps exactly as written.
Make sure the "target_tool" strictly matches one of the available tools.

Available Tools context:
{available_tools_info if available_tools_info else "Assume standard tools: research_advanced, calendar_google, code_advanced, rag_tool"}

User Objective: "{user_input}"

Create a highly detailed, step-by-step plan.
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=planner_schema,
                temperature=0.2, # slight freedom for planning
            ),
        )
        data = json.loads(response.text)
        logger.info("Plan Generated: %s with %d steps.", data.get("plan_summary"), len(data.get("steps", [])))
        return data
    except Exception as e:
        logger.error("Failed to generate plan: %s", e)
        # Fallback trivial plan
        return {
            "plan_summary": "Fallback plan due to generation error.",
            "steps": [
                {
                    "step_number": 1,
                    "target_tool": "none",
                    "instruction": f"Inform user of planning error: {str(e)}",
                    "expected_outcome": "User informed of error.",
                    "depends_on": []
                }
            ]
        }
