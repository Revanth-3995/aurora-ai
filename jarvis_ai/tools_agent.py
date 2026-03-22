"""
AURORA tool layer for Gemini: no LangChain. Uses google-generativeai and backend tools only.
"""
import sys
import json
from pathlib import Path
from typing import Any, List

# ── Fix: add both jarvis_ai/ and project root to sys.path ────────────────────
_here = Path(__file__).resolve().parent   # .../agentic_ai_project/jarvis_ai
_root = _here.parent                      # .../agentic_ai_project

for _p in [str(_here), str(_root)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)
# ─────────────────────────────────────────────────────────────────────────────

from google.generativeai.types import content_types
from backend.tools import get_tool_registry

_registry = get_tool_registry()
_calendar_backend = _registry.get("calendar_google")
_code_backend = _registry.get("code_advanced")
_research_backend = _registry.get("research_advanced")
_memory_backend = _registry.get("memory_save")


def _to_dict(struct: Any) -> dict:
    """Convert protos.Struct or dict to plain dict."""
    if struct is None:
        return {}
    if isinstance(struct, dict):
        return struct
    if hasattr(struct, "items"):
        return dict(struct.items())
    return {}


# --- Gemini function declarations (OpenAPI-style schema) ---
# NOTE: Gemini's Schema proto does NOT support "default" — omit it everywhere.

_CALENDAR_SCHEMA = {
    "type": "object",
    "properties": {
        "action":      {"type": "string",  "description": "Either 'schedule_event' or 'check_availability'"},
        "start":       {"type": "string",  "description": "Start time, e.g. '2025-03-20 15:00' or ISO 8601"},
        "end":         {"type": "string",  "description": "End time"},
        "timezone":    {"type": "string",  "description": "IANA timezone, e.g. 'America/Los_Angeles'. Defaults to UTC if omitted."},
        "title":       {"type": "string",  "description": "Event title (required for schedule_event)"},
        "attendees":   {"type": "array",   "items": {"type": "string"}, "description": "List of attendee email addresses"},
        "description": {"type": "string",  "description": "Optional event description"},
        "location":    {"type": "string",  "description": "Optional event location"},
    },
    "required": ["action", "start", "end"],
}

_CODE_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": "Python code snippet to execute"},
    },
    "required": ["code"],
}

_RESEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "query":          {"type": "string",  "description": "Research question or topic"},
        "max_results":    {"type": "integer", "description": "Number of sources to return (default is 5 if omitted)"},
        "save_to_memory": {"type": "boolean", "description": "If true, persist results for long-term reference"},
    },
    "required": ["query"],
}

_MEMORY_SCHEMA = {
    "type": "object",
    "properties": {
        "fact": {"type": "string", "description": "The specific fact, goal, or preference to save permanently."},
    },
    "required": ["fact"],
}


def _calendar_tool(**kwargs: Any) -> str:
    if _calendar_backend is None:
        return json.dumps({"ok": False, "error": "Calendar tool is not available."})
    payload = {
        "action":      kwargs.get("action"),
        "start":       kwargs.get("start"),
        "end":         kwargs.get("end"),
        "timezone":    kwargs.get("timezone", "UTC"),
        "title":       kwargs.get("title"),
        "attendees":   kwargs.get("attendees"),
        "description": kwargs.get("description"),
        "location":    kwargs.get("location"),
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    result = _calendar_backend(payload)
    return json.dumps(result, ensure_ascii=False)


def _code_tool(code: str) -> str:
    if _code_backend is None:
        return json.dumps({"ok": False, "error": "Code tool is not available."})
    result = _code_backend({"language": "python", "code": code})
    return json.dumps(result, ensure_ascii=False)


def _research_tool(query: str, max_results: int = 5, save_to_memory: bool = False) -> str:
    if _research_backend is None:
        return json.dumps({"ok": False, "error": "Research tool is not available."})
    result = _research_backend({
        "query": query,
        "max_results": max_results,
        "save_to_memory": save_to_memory,
    })
    return json.dumps(result, ensure_ascii=False)


def _memory_tool(fact: str) -> str:
    if _memory_backend is None:
        return json.dumps({"ok": False, "error": "Memory tool is not available."})
    result = _memory_backend({"fact": fact})
    return json.dumps(result, ensure_ascii=False)


def get_gemini_tools() -> List[content_types.Tool]:
    """Return a list of Tool objects for Gemini (function declarations only)."""
    declarations: List[content_types.FunctionDeclarationType] = []

    if _calendar_backend is not None:
        declarations.append(
            content_types.CallableFunctionDeclaration(
                name="calendar_google",
                description=(
                    "Use Google Calendar to schedule events or check availability. "
                    "For schedule_event provide title, start, end, timezone. "
                    "For check_availability provide start, end, timezone."
                ),
                parameters=_CALENDAR_SCHEMA,
                function=lambda **kw: _calendar_tool(**kw),
            )
        )

    if _code_backend is not None:
        declarations.append(
            content_types.CallableFunctionDeclaration(
                name="code_advanced",
                description="Execute Python code in a sandbox and return stdout, stderr, and success/failure.",
                parameters=_CODE_SCHEMA,
                function=lambda **kw: _code_tool(kw.get("code", "")),
            )
        )

    if _research_backend is not None:
        declarations.append(
            content_types.CallableFunctionDeclaration(
                name="research_advanced",
                description=(
                    "Perform web research via Tavily. Returns a concise answer and key sources. "
                    "Optionally save to long-term memory."
                ),
                parameters=_RESEARCH_SCHEMA,
                function=lambda **kw: _research_tool(
                    kw.get("query", ""),
                    int(kw.get("max_results", 5)),
                    bool(kw.get("save_to_memory", False)),
                ),
            )
        )

    if _memory_backend is not None:
        declarations.append(
            content_types.CallableFunctionDeclaration(
                name="memory_save",
                description="Save a specific permanent fact, preference, or goal about the user into long-term personal storage.",
                parameters=_MEMORY_SCHEMA,
                function=lambda **kw: _memory_tool(kw.get("fact", "")),
            )
        )

    if not declarations:
        return []
    return [content_types.Tool(function_declarations=declarations)]


def execute_tool(name: str, args: dict) -> Any:
    """Execute a tool by name with given args; returns a dict for Gemini function_response."""
    args = _to_dict(args)
    if name == "calendar_google":
        return _calendar_tool(**args)
    if name == "code_advanced":
        return _code_tool(args.get("code", ""))
    if name == "research_advanced":
        return _research_tool(
            args.get("query", ""),
            args.get("max_results", 5),
            args.get("save_to_memory", False),
        )
    if name == "memory_save":
        return _memory_tool(args.get("fact", ""))
    return {"error": f"Unknown tool: {name}"}


def build_aurora_agent(llm: Any):
    """
    For compatibility with app.py that expects an agent.
    We no longer use LangChain; app.py should use run_aurora_turn() instead.
    """
    raise NotImplementedError(
        "Use run_aurora_turn(model, history, user_input) from this module instead of build_aurora_agent."
    )

def filter_tools_for_intent(all_tools, intent_category):
    """Filters the generated tools based precisely on the identified intent."""
    if not all_tools or intent_category == "CHAT":
        return None
        
    declarations = all_tools[0].function_declarations
    filtered = []
    
    for dec in declarations:
        name = dec.name.lower()
        if intent_category == "SCHEDULE" and "calendar" in name:
            filtered.append(dec)
        elif intent_category == "RESEARCH" and "research" in name:
            filtered.append(dec)
        elif intent_category == "CODE" and "code" in name:
            filtered.append(dec)
        elif intent_category == "RAG" and "rag" in name:
            filtered.append(dec)
        elif intent_category == "MEMORY" and "memory" in name:
            filtered.append(dec)
            
    if not filtered:
        return None
        
    return [content_types.Tool(function_declarations=filtered)]