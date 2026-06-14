import json
import os
from datetime import datetime
from pathlib import Path
from langchain_core.tools import tool

CALENDAR_FILE = Path(__file__).parent.parent / "data" / "calendar.json"

def _load_calendar():
    if not os.path.exists(CALENDAR_FILE):
        os.makedirs(CALENDAR_FILE.parent, exist_ok=True)
        with open(CALENDAR_FILE, 'w') as f:
            json.dump([], f)
        return []
    with open(CALENDAR_FILE, 'r') as f:
        return json.load(f)

def _save_calendar(events):
    with open(CALENDAR_FILE, 'w') as f:
        json.dump(events, f, indent=4)

@tool
def add_calendar_event(title: str, date: str, time: str, description: str = "") -> str:
    """Add a new event to the user's calendar.
    Args:
        title: The name of the event.
        date: The date in YYYY-MM-DD format.
        time: The time in HH:MM format.
        description: Optional details about the event.
    """
    events = _load_calendar()
    new_event = {
        "id": len(events) + 1,
        "title": title,
        "date": date,
        "time": time,
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    events.append(new_event)
    _save_calendar(events)
    return f"Successfully added event: '{title}' on {date} at {time}."

@tool
def get_calendar_events(date: str = None) -> str:
    """Get upcoming calendar events. If date (YYYY-MM-DD) is provided, filters for that specific date."""
    events = _load_calendar()
    if not events:
        return "No events in calendar."
    
    if date:
        filtered = [e for e in events if e.get("date") == date]
        if not filtered:
            return f"No events on {date}."
        return json.dumps(filtered, indent=2)
    
    return json.dumps(events, indent=2)
