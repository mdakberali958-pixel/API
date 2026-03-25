from dataclasses import dataclass


@dataclass
class EvaluationSummary:
    dataset: str
    total_questions: int
    grounded_accuracy: float
    hallucination_rate: float
    reduction_vs_baseline: float


def run_evaluation(dataset: str = "TruthfulQA") -> EvaluationSummary:
    # Placeholder values for scaffold; replace with batch evaluation runner.
    baseline_hallucination = 0.37
    current_hallucination = 0.22
    reduction = (baseline_hallucination - current_hallucination) / baseline_hallucination * 100
    return EvaluationSummary(
        dataset=dataset,
        total_questions=817,
        grounded_accuracy=0.74,
        hallucination_rate=current_hallucination,
        reduction_vs_baseline=round(reduction, 2),
    )
