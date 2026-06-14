from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.schemas.api import DocumentUploadResponse, AskDocumentRequest
import shutil
import os
from pathlib import Path
from backend.services.rag.ingest import ingest_documents
from backend.services.rag.retriever import get_rag_chain

router = APIRouter()
DATA_DIR = Path("data/documents")

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(DATA_DIR, exist_ok=True)
    # Sanitize the filename to prevent path traversal attacks
    safe_filename = os.path.basename(file.filename)
    file_path = DATA_DIR / safe_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trigger ingestion
        # We might want to run this asynchronously in production
        ingest_documents()

        # Simple size calc
        size = os.path.getsize(file_path)

        return DocumentUploadResponse(
            filename=file.filename,
            status="Uploaded and ingested",
            pages=0, # Could be calculated during ingest
            size_bytes=size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")

@router.post("/ask")
async def ask_document(request: AskDocumentRequest):
    rag_chain = get_rag_chain()
    if not rag_chain:
        raise HTTPException(status_code=400, detail="RAG system not initialized. Upload a document first.")

    try:
        response = rag_chain.invoke(request.question)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
