from __future__ import annotations

from typing import Any, Dict, List

from backend.tools.types import ResearchResult, ResearchSnippet


def normalize_results(query: str, raw: Dict[str, Any]) -> ResearchResult:
    """
    Normalize a Tavily-style response into a ResearchResult.
    """
    raw_results = raw.get("results") or []
    answer = str(raw.get("answer") or "")

    snippets: List[ResearchSnippet] = []

    for item in raw_results:
        title = str(item.get("title") or "").strip() or "Untitled"
        url = str(item.get("url") or "").strip() or ""
        snippet_text = str(item.get("content") or item.get("snippet") or "").strip()

        # Derive some naive bullet points by splitting sentences
        key_points: List[str] = []
        for sentence in snippet_text.split("."):
            sentence = sentence.strip()
            if sentence:
                key_points.append(sentence)

        published = item.get("published_date") or item.get("date")

        snippets.append(
            ResearchSnippet(
                title=title,
                url=url,
                summary=snippet_text[:500],
                key_points=key_points[:8],
                published_at=str(published) if published is not None else None,
                raw=item,
            )
        )

    return ResearchResult(query=query, answer=answer, snippets=snippets)

