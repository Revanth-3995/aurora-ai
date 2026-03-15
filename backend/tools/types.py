from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class CalendarEvent:
    id: Optional[str]
    title: str
    start: datetime
    end: datetime
    timezone: str
    attendees: List[str] = field(default_factory=list)
    description: Optional[str] = None
    location: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CodeExecutionResult:
    success: bool
    stdout: str
    stderr: str
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    timed_out: bool = False
    attempts: int = 1


@dataclass
class ResearchSnippet:
    title: str
    url: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    published_at: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchResult:
    query: str
    answer: str
    snippets: List[ResearchSnippet] = field(default_factory=list)

