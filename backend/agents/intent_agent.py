import json
import logging
import google.generativeai as genai
from google.generativeai.types import content_types

logger = logging.getLogger(__name__)

def classify_intent(user_input: str, model: genai.GenerativeModel) -> dict:
    """
    Classifies the user input into a specific operational intent for AURORA.
    Returns a dict with {"category": "...", "reasoning": "..."}
    """
    intent_schema = {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "The category of the user's intent. Must be exactly one of: CHAT, SCHEDULE, RESEARCH, CODE, RAG, MEMORY.",
            },
            "reasoning": {
                "type": "string",
                "description": "A brief explanation of why this category was chosen.",
            },
        },
        "required": ["category", "reasoning"],
    }

    prompt = f"""
You are the Intent Classification Agent for AURORA-AI.
Analyze the user's input and categorize it strictly into one of the following intent categories:

- CHAT: General conversation, greetings, pleasantries, or basic knowledge questions that don't require external tools.
- SCHEDULE: Any request related to booking meetings, adding calendar events, or checking availability/time.
- RESEARCH: Questions requiring up-to-date information, news, or deep web searches via Tavily.
- CODE: Requests that involve high-level math, writing scripts, or executing Python code.
- RAG: Requests asking to summarize, read, or search through the user's uploaded personal documents, notes, or PDFs.
- MEMORY: Any explicit request for you to remember, save, or store a fact, preference, or goal about the user for the long term.

User Input: "{user_input}"
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=intent_schema,
                temperature=0.0,
            ),
        )
        data = json.loads(response.text)
        logger.info("Intent Classified: %s - %s", data.get("category"), data.get("reasoning"))
        return data
    except Exception as e:
        logger.error("Failed to classify intent: %s. Falling back to CHAT.", e)
        return {"category": "CHAT", "reasoning": f"Fallback intent due to classification error: {str(e)}"}
