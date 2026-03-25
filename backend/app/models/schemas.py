from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ChatMode(str, Enum):
    STANDARD = "standard"
    VERIFIED = "verified"


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    query: str
    mode: ChatMode = ChatMode.STANDARD
    conversation_id: str | None = None


class EvidenceItem(BaseModel):
    doc_id: str
    title: str
    snippet: str
    similarity: float
    source_url: str | None = None


class HallucinationReport(BaseModel):
    hallucination_probability: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)
    explanation: str
    signals: dict[str, float]


class ChatResponse(BaseModel):
    answer: str
    mode: ChatMode
    report: HallucinationReport
    evidence: list[EvidenceItem] = []
