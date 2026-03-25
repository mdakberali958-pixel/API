from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/metrics")
def metrics() -> dict:
    return {
        "daily_active_users": 128,
        "queries_today": 2048,
        "avg_hallucination_probability": 21.6,
        "verified_mode_usage_pct": 63.4,
    }
