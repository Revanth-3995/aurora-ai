from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable

from backend.tools.types import ResearchSnippet

logger = logging.getLogger(__name__)


def persist_research_snippets(
    snippets: Iterable[ResearchSnippet],
    path: str = "data/research_snippets.jsonl",
) -> None:
    """
    Persist research snippets in a simple JSONL file.

    This is intentionally minimal and filesystem-based so it can be
    replaced with a cloud database implementation without changing
    the tool interface.
    """
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("a", encoding="utf-8") as f:
        for snip in snippets:
            record = {
                "title": snip.title,
                "url": snip.url,
                "summary": snip.summary,
                "key_points": snip.key_points,
                "published_at": snip.published_at,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    logger.info("Persisted %s research snippets to %s", len(list(snippets)), out_path)

