from __future__ import annotations

import logging
from typing import Any, Dict, List

import requests

from backend.config import settings

logger = logging.getLogger(__name__)


class TavilyError(RuntimeError):
    pass


def search(
    query: str,
    max_results: int = 5,
    include_answer: bool = True,
    include_images: bool = False,
) -> Dict[str, Any]:
    """
    Perform a Tavily (or Tavily-compatible) web search.
    """
    api_key = settings.tavily_api_key
    if not api_key:
        raise TavilyError("TAVILY_API_KEY is not configured.")

    url = "https://api.tavily.com/search"
    payload: Dict[str, Any] = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "include_answer": include_answer,
        "include_images": include_images,
    }

    logger.info("Calling Tavily search for query=%r", query)
    resp = requests.post(url, json=payload, timeout=20)

    if resp.status_code != 200:
        raise TavilyError(f"Tavily API error {resp.status_code}: {resp.text}")

    data = resp.json()
    return data

