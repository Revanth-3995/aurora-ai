from __future__ import annotations

import datetime as dt
import logging
from typing import Any, Dict

from backend.tools.calendar.google_calendar_client import create_event, find_conflicts, list_events

logger = logging.getLogger(__name__)


def _parse_iso_or_date_time(value: str, timezone: str) -> dt.datetime:
    """
    Parse a human-ish datetime string into an aware datetime.
    Expect ISO 8601 or `YYYY-MM-DD HH:MM` in the given timezone.
    """
    from zoneinfo import ZoneInfo

    try:
        parsed = dt.datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo(timezone))
        return parsed
    except Exception:
        pass

    try:
        parsed = dt.datetime.strptime(value, "%Y-%m-%d %H:%M")
        parsed = parsed.replace(tzinfo=ZoneInfo(timezone))
        return parsed
    except Exception as exc:
        raise ValueError(f"Could not parse datetime '{value}': {exc}") from exc


def schedule_event_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Schedule a calendar event using Google Calendar.

    Expected payload:
      - title: str
      - start: str (ISO or 'YYYY-MM-DD HH:MM')
      - end: str (ISO or 'YYYY-MM-DD HH:MM')
      - timezone: str (IANA, e.g. 'UTC' or 'America/Los_Angeles')
      - attendees: list[str] (optional)
      - description: str (optional)
      - location: str (optional)
    """
    title = str(payload.get("title") or "").strip()
    start_raw = str(payload.get("start") or "").strip()
    end_raw = str(payload.get("end") or "").strip()
    timezone = str(payload.get("timezone") or "UTC").strip() or "UTC"

    if not title or not start_raw or not end_raw:
        raise ValueError("title, start, and end are required fields.")

    attendees = payload.get("attendees") or []
    description = payload.get("description") or None
    location = payload.get("location") or None

    start_dt = _parse_iso_or_date_time(start_raw, timezone)
    end_dt = _parse_iso_or_date_time(end_raw, timezone)

    if end_dt <= start_dt:
        raise ValueError("end must be after start.")

    event = create_event(
        title=title,
        start=start_dt,
        end=end_dt,
        timezone=timezone,
        attendees=attendees,
        description=description,
        location=location,
    )

    summary = f"Scheduled '{title}' from {start_dt.isoformat()} to {end_dt.isoformat()} ({timezone})."

    return {
        "ok": True,
        "summary": summary,
        "event": event,
    }


def check_availability_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check availability within a time range and list conflicts.

    Expected payload:
      - start: str
      - end: str
      - timezone: str (optional, default 'UTC')
      - max_results: int (optional)
    """
    start_raw = str(payload.get("start") or "").strip()
    end_raw = str(payload.get("end") or "").strip()
    timezone = str(payload.get("timezone") or "UTC").strip() or "UTC"
    max_results = int(payload.get("max_results") or 50)

    if not start_raw or not end_raw:
        raise ValueError("start and end are required fields.")

    start_dt = _parse_iso_or_date_time(start_raw, timezone)
    end_dt = _parse_iso_or_date_time(end_raw, timezone)

    events = list_events(start_dt, end_dt, max_results=max_results)
    conflicts = find_conflicts(start_dt, end_dt)

    busy = len(conflicts) > 0
    summary = (
        f"You are busy between {start_dt.isoformat()} and {end_dt.isoformat()} ({timezone})."
        if busy
        else f"You are free between {start_dt.isoformat()} and {end_dt.isoformat()} ({timezone})."
    )

    return {
        "ok": True,
        "busy": busy,
        "summary": summary,
        "events": events,
        "conflicts": conflicts,
    }


def calendar_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for the Google Calendar tool.

    Expected payload:
      - action: 'schedule_event' | 'check_availability'
      - ...additional fields depending on the action...
    """
    action = str(payload.get("action") or "").strip()

    logger.info("Calendar tool invoked with action=%s", action)

    if action == "schedule_event":
        return schedule_event_tool(payload)
    if action == "check_availability":
        return check_availability_tool(payload)

    raise ValueError(f"Unsupported calendar action: {action!r}")

