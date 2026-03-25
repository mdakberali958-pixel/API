from backend.app.models.schemas import EvidenceItem


def retrieve_context(query: str, top_k: int = 4) -> list[EvidenceItem]:
    """Placeholder retrieval service.
    Replace with Chroma/FAISS similarity search in production.
    """
    return [
        EvidenceItem(
            doc_id="doc-001",
            title="Policy Handbook",
            snippet="Enterprise QA policy states all claims should cite primary sources.",
            similarity=0.87,
            source_url="https://example.org/policy",
        ),
        EvidenceItem(
            doc_id="doc-002",
            title="Model Ops Guide",
            snippet="Self-consistency can reduce brittle single-pass model outputs.",
            similarity=0.81,
            source_url="https://example.org/model-ops",
        ),
    ][:top_k]
