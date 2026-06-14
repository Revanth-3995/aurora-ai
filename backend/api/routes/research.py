from fastapi import APIRouter, HTTPException
from backend.schemas.api import ResearchRequest, ResearchResponse
from backend.tools.research.tool_research_advanced import research_tool

router = APIRouter()

@router.post("", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    try:
        # Wrap in a payload for the tool
        payload = {
            "query": request.query,
            "max_results": request.max_results,
            "save_to_memory": request.save_to_memory
        }

        # The tool returns a dictionary with 'result', 'sources', etc.
        # But looking at backend/tools/research/tool_research_advanced.py
        # it returns a structured result.
        result = research_tool(payload)

        # Assume it has 'summary' and 'sources' or we map them
        summary = result.get("summary", result.get("answer", "Research completed but no summary found."))
        sources = result.get("sources", [])

        return ResearchResponse(summary=summary, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
