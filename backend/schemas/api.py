from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str

class WorkflowStep(BaseModel):
    step_number: int
    target_tool: str
    instruction: str
    expected_outcome: str
    depends_on: List[int]

class ChatResponse(BaseModel):
    response: str
    intent: str
    tool_used: str
    reasoning: str
    workflow: List[Dict[str, Any]]

class DocumentUploadResponse(BaseModel):
    filename: str
    status: str
    pages: int
    size_bytes: int

class AskDocumentRequest(BaseModel):
    question: str

class ResearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5
    save_to_memory: Optional[bool] = False

class ResearchSource(BaseModel):
    url: str
    title: str
    content: str

class ResearchResponse(BaseModel):
    summary: str
    sources: List[Dict[str, Any]]

class ScheduleEventRequest(BaseModel):
    title: str
    date: str
    time: str
    description: Optional[str] = ""

class ScheduleEventResponse(BaseModel):
    status: str
    message: str
    event: Dict[str, Any]

class WorkflowResponse(BaseModel):
    history: List[Dict[str, Any]]
