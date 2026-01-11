from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.permissions import require_roles
from app.models.user import User
from app.models.historical_student import HistoricalStudent
from app.models.recommendation import Recommendation
from app.services.feature_service import get_student_feature_dict
from app.ml.similarity_engine import compute_similarity

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

# --------------------------------------------------
# SIM-2: Similar Students (Motivational)
# --------------------------------------------------
@router.get("/similar")
def similar_students(
    db: Session = Depends(get_db),
    student: User = Depends(require_roles("student")),
):
    feature_dict = get_student_feature_dict(db, student.id)

    if not feature_dict:
        raise HTTPException(
            status_code=404,
            detail="Student features not available yet",
        )

    historical_records = db.query(HistoricalStudent).all()

    if not historical_records:
        return []

    matches = compute_similarity(
        current_features=feature_dict,
        historical_records=historical_records,
        top_k=3,
    )

    return [
        {
            "profile_summary": _build_profile_summary(m),
            "actions_taken": m["actions_taken"],
            "outcome": m["outcome"],
        }
        for m in matches
    ]


def _build_profile_summary(match: dict) -> str:
    similarity = match["similarity"]

    if similarity > 0.9:
        return "Very similar academic and behavioral profile"
    elif similarity > 0.75:
        return "Moderately similar learning pattern"
    else:
        return "Loosely similar academic background"


# --------------------------------------------------
# REC-3: Personalized Recommendations (Actions)
# --------------------------------------------------
@router.get("/actions")
def get_personalized_recommendations(
    db: Session = Depends(get_db),
    student: User = Depends(require_roles("student")),
):
    records = (
        db.query(Recommendation)
        .filter(Recommendation.child_id == student.id)
        .order_by(
            Recommendation.priority.desc(),
            Recommendation.generated_at.desc(),
        )
        .all()
    )

    return {
        "recommendations": [
            {
                "area": r.area,
                "suggestion": r.suggestion,
                "priority": r.priority,
            }
            for r in records
        ]
    }
