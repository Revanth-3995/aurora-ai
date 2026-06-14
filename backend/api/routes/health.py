from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

@router.get("")
async def health_check():
    return {"status": "healthy", "service": "AURORA-AI"}
