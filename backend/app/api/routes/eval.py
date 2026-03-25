from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.evaluator import run_evaluation

router = APIRouter(prefix="/eval", tags=["evaluation"])


class EvalRequest(BaseModel):
    dataset: str = "TruthfulQA"


@router.post("/run")
def run(payload: EvalRequest) -> dict:
    summary = run_evaluation(payload.dataset)
    return {
        "dataset": summary.dataset,
        "total_questions": summary.total_questions,
        "grounded_accuracy": summary.grounded_accuracy,
        "hallucination_rate": summary.hallucination_rate,
        "reduction_vs_baseline_pct": summary.reduction_vs_baseline,
    }
