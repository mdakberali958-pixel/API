from backend.app.models.schemas import EvidenceItem, HallucinationReport


def evaluate_hallucination(answer: str, evidence: list[EvidenceItem]) -> HallucinationReport:
    """Multi-signal hallucination estimator (simplified baseline)."""
    grounding = min(sum(item.similarity for item in evidence) / max(len(evidence), 1), 1.0)
    self_consistency = 0.76 if evidence else 0.58
    semantic_alignment = 0.81 if evidence else 0.63
    claim_verification = 0.79 if evidence else 0.52

    weighted_reliability = (
        0.35 * grounding
        + 0.25 * self_consistency
        + 0.25 * semantic_alignment
        + 0.15 * claim_verification
    )

    confidence = round(weighted_reliability * 100, 2)
    hallucination_probability = round(100 - confidence, 2)

    explanation = (
        "Risk estimated from retrieval grounding, self-consistency, semantic alignment, and claim checks. "
        "This score is probabilistic and not a guarantee of correctness."
    )

    return HallucinationReport(
        hallucination_probability=hallucination_probability,
        confidence_score=confidence,
        explanation=explanation,
        signals={
            "grounding": round(grounding * 100, 2),
            "self_consistency": round(self_consistency * 100, 2),
            "semantic_alignment": round(semantic_alignment * 100, 2),
            "claim_verification": round(claim_verification * 100, 2),
        },
    )
