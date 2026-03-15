from __future__ import annotations

import logging
from typing import Any, Dict

from backend.memory.hooks import persist_research_snippets
from backend.tools.research.postprocessors import normalize_results
from backend.tools.research.tavily_client import TavilyError, search

logger = logging.getLogger(__name__)


def research_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Advanced research tool using Tavily (or a compatible API).

    Expected payload:
      - query: str
      - max_results: int (optional, default 5)
      - save_to_memory: bool (optional, default False)
    """
    query = str(payload.get("query") or "").strip()
    if not query:
        raise ValueError("query is required for research_tool.")

    max_results = int(payload.get("max_results") or 5)
    save_to_memory = bool(payload.get("save_to_memory") or False)

    try:
        raw = search(query=query, max_results=max_results)
    except TavilyError as exc:
        logger.error("Research tool failed: %s", exc)
        raise

    result = normalize_results(query, raw)

    if save_to_memory and result.snippets:
        persist_research_snippets(result.snippets)

    # Construct a short answer if Tavily didn't provide one.
    answer = result.answer
    if not answer and result.snippets:
        # Simple heuristic summary from the first snippet
        answer = result.snippets[0].summary

    concise_answer = answer[:800]

    return {
        "ok": True,
        "query": result.query,
        "answer": concise_answer,
        "snippets": [
            {
                "title": snip.title,
                "url": snip.url,
                "summary": snip.summary,
                "key_points": snip.key_points,
                "published_at": snip.published_at,
            }
            for snip in result.snippets
        ],
    }

