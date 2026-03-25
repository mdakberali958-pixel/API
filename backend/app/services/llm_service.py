from backend.app.models.schemas import ChatMode, EvidenceItem


def generate_answer(query: str, mode: ChatMode, evidence: list[EvidenceItem]) -> str:
    """Production would call an LLM SDK with streaming and retries."""
    if mode == ChatMode.VERIFIED and evidence:
        return (
            f"Grounded answer for: '{query}'. "
            f"This response was generated with retrieved enterprise sources and should be audited."
        )
    return (
        f"Standard-mode answer for: '{query}'. "
        "No retrieval grounding was applied in this mode."
    )
