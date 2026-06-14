from __future__ import annotations

import datetime as dt
import logging
from typing import Any, Dict, List, Optional

from backend.config.config import settings

logger = logging.getLogger(__name__)

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
except Exception:  # pragma: no cover - optional dependency
    Credentials = None  # type: ignore
    Request = None  # type: ignore
    build = None  # type: ignore
    InstalledAppFlow = None  # type: ignore


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _ensure_google_deps() -> None:
    if Credentials is None or Request is None or build is None or InstalledAppFlow is None:
        raise RuntimeError(
            "Google Calendar dependencies are not installed. "
            "Install 'google-api-python-client google-auth-httplib2 google-auth-oauthlib'."
        )


def build_google_calendar_service(
    credentials_path: Optional[str] = None,
    token_path: Optional[str] = None,
):
    """
    Build and return an authenticated Google Calendar service client.

    In local development, this will perform an OAuth flow on first run
    and cache the token to `token_path`. In production, you can mount
    pre-generated tokens or use different auth mechanisms by adapting
    this helper.
    """
    _ensure_google_deps()

    from pathlib import Path

    credentials_path = credentials_path or settings.google_credentials_path
    token_path = token_path or settings.google_token_path

    if not credentials_path:
        raise RuntimeError("GOOGLE_CREDENTIALS_PATH is not configured.")

    creds = None
    token_file = Path(token_path) if token_path else None

    if token_file and token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)  # type: ignore[arg-type]

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired Google credentials.")
            creds.refresh(Request())  # type: ignore[operator]
        else:
            logger.info("Running Google OAuth flow to obtain new credentials.")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)  # type: ignore[arg-type]
            creds = flow.run_local_server(port=0)

        if token_file:
            token_file.parent.mkdir(parents=True, exist_ok=True)
            token_file.write_text(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def list_events(
    start: dt.datetime,
    end: dt.datetime,
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    service = build_google_calendar_service()
    time_min = start.astimezone(dt.timezone.utc).isoformat()
    time_max = end.astimezone(dt.timezone.utc).isoformat()

    logger.info("Listing Google Calendar events between %s and %s", time_min, time_max)
    events_result = (
        service.events()  # type: ignore[no-untyped-call]
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])


def create_event(
    title: str,
    start: dt.datetime,
    end: dt.datetime,
    timezone: str,
    attendees: Optional[List[str]] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
) -> Dict[str, Any]:
    service = build_google_calendar_service()

    event_body: Dict[str, Any] = {
        "summary": title,
        "start": {"dateTime": start.isoformat(), "timeZone": timezone},
        "end": {"dateTime": end.isoformat(), "timeZone": timezone},
    }

    if attendees:
        event_body["attendees"] = [{"email": email} for email in attendees]
    if description:
        event_body["description"] = description
    if location:
        event_body["location"] = location

    logger.info("Creating Google Calendar event: %s", title)
    event = (
        service.events()  # type: ignore[no-untyped-call]
        .insert(calendarId="primary", body=event_body)
        .execute()
    )
    return event


def find_conflicts(
    start: dt.datetime,
    end: dt.datetime,
) -> List[Dict[str, Any]]:
    """
    Return events that overlap with the given window.
    """
    events = list_events(start, end, max_results=250)

    conflicts: List[Dict[str, Any]] = []
    for ev in events:
        ev_start_raw = ev.get("start", {}).get("dateTime") or ev.get("start", {}).get("date")
        ev_end_raw = ev.get("end", {}).get("dateTime") or ev.get("end", {}).get("date")
        if not ev_start_raw or not ev_end_raw:
            continue

        try:
            ev_start = dt.datetime.fromisoformat(ev_start_raw)
            ev_end = dt.datetime.fromisoformat(ev_end_raw)
        except ValueError:
            continue

        # Basic overlap check
        if ev_start < end and ev_end > start:
            conflicts.append(ev)

    logger.info("Found %d conflicting events", len(conflicts))
    return conflicts

