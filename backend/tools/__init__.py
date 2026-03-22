"""
Tool registry helpers for the AURORA backend.

The main agent orchestrator can import `get_tool_registry`
to obtain a mapping from tool names to callables. Each
callable should accept a single `dict` payload and return
serializable data.
"""

from typing import Any, Callable, Dict

from backend.config import settings


ToolFn = Callable[[Dict[str, Any]], Dict[str, Any]]


def get_tool_registry() -> Dict[str, ToolFn]:
    """
    Return a registry of available tools based on feature flags.

    The calling orchestrator can expose these tools to the LLM using
    its preferred function/tool-calling mechanism.
    """
    registry: Dict[str, ToolFn] = {}

    if settings.enable_google_calendar:
        try:
            from backend.tools.calendar.tool_calendar_google import calendar_tool

            registry["calendar_google"] = calendar_tool
        except Exception:
            # Calendar tool is optional; failures should not break startup.
            pass

    if settings.enable_advanced_code_tool:
        try:
            from backend.tools.code.tool_code_advanced import code_tool

            registry["code_advanced"] = code_tool
        except Exception:
            pass

    if settings.enable_advanced_research_tool:
        try:
            from backend.tools.research.tool_research_advanced import research_tool

            registry["research_advanced"] = research_tool
        except Exception:
            pass

    try:
        from backend.tools.memory.tool_memory import execute_memory_save
        registry["memory_save"] = execute_memory_save
    except Exception as e:
        print(f"Memory tool offline: {e}")

    return registry


