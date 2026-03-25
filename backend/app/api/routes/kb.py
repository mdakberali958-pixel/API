from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from backend.app.services.ingestion import chunk_text, embed_chunks

router = APIRouter(prefix="/kb", tags=["knowledge-base"])


class IndexRequest(BaseModel):
    text: str


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "status": "received",
    }


@router.post("/index")
def index_document(payload: IndexRequest) -> dict:
    chunks = chunk_text(payload.text)
    vectors = embed_chunks(chunks)
    return {
        "chunks_indexed": len(chunks),
        "embedding_dimensions": len(vectors[0]) if vectors else 0,
    }
