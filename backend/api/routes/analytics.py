from fastapi import APIRouter

router = APIRouter()

# In-memory mock data for dashboard until DB is implemented
MOCK_STATS = {
    "total_chats": 142,
    "research_queries": 35,
    "uploaded_documents": 12,
    "calendar_events": 28,
    "avg_response_time_ms": 1250,
    "recent_activity": [
        {"id": 1, "type": "chat", "summary": "Discussed agent architecture", "time": "10 mins ago"},
        {"id": 2, "type": "research", "summary": "Researched quantum computing", "time": "1 hour ago"},
        {"id": 3, "type": "calendar", "summary": "Scheduled team meeting", "time": "2 hours ago"}
    ],
    "chart_data": [
        {"name": "Mon", "chats": 20, "research": 5},
        {"name": "Tue", "chats": 25, "research": 8},
        {"name": "Wed", "chats": 18, "research": 4},
        {"name": "Thu", "chats": 30, "research": 10},
        {"name": "Fri", "chats": 49, "research": 8}
    ]
}

@router.get("")
async def get_analytics():
    return MOCK_STATS

@router.get("/workflow-history")
async def get_workflow_history():
    return {"history": []}
