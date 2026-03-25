from fastapi import APIRouter
from backend.app.models.schemas import ChatRequest, ChatResponse, ChatMode
from backend.app.services.retrieval import retrieve_context
from backend.app.services.llm_service import generate_answer
from backend.app.services.hallucination import evaluate_hallucination

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/query", response_model=ChatResponse)
def query_chat(payload: ChatRequest) -> ChatResponse:
    evidence = retrieve_context(payload.query) if payload.mode == ChatMode.VERIFIED else []
    answer = generate_answer(payload.query, payload.mode, evidence)
    report = evaluate_hallucination(answer, evidence)
    return ChatResponse(answer=answer, mode=payload.mode, report=report, evidence=evidence)
