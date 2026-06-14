from fastapi import APIRouter, HTTPException
from backend.schemas.api import ScheduleEventRequest, ScheduleEventResponse
from backend.tools.calendar.tool_calendar_google import calendar_tool
from datetime import datetime, timedelta

router = APIRouter()

@router.post("", response_model=ScheduleEventResponse)
async def schedule_event(request: ScheduleEventRequest):
    try:
        # Convert date and time to start and end
        # Assumes request.date is YYYY-MM-DD and request.time is HH:MM
        start_str = f"{request.date} {request.time}"

        # Default duration 1 hour
        start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(hours=1)
        end_str = end_dt.strftime("%Y-%m-%d %H:%M")

        payload = {
            "action": "schedule_event",
            "title": request.title,
            "start": start_str,
            "end": end_str,
            "description": request.description
        }

        result = calendar_tool(payload)

        return ScheduleEventResponse(
            status="Success" if result.get("ok") else "Failed",
            message=result.get("message", str(result)),
            event=result.get("event", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
