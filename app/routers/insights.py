from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.risk_score import RiskScore
from app.models.prediction import StudentPrediction
from app.models.insight_review import ReviewerRole
from app.services.explanation_service import generate_explanation
from app.services.insight_review_service import acknowledge_insight

router = APIRouter(
    prefix="/insights",
    tags=["Insights"],
)

# =========================================================
# RISK-3 — Student Risk Insights
# =========================================================
@router.get("/self")
def get_self_insights(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Student access only")

    risk = (
        db.query(RiskScore)
        .filter(RiskScore.student_id == user.id)
        .order_by(RiskScore.calculated_at.desc())
        .first()
    )

    if not risk:
        raise HTTPException(status_code=404, detail="Risk data not found")

    prediction = (
        db.query(StudentPrediction)
        .filter(StudentPrediction.student_id == user.id)
        .order_by(StudentPrediction.created_at.desc())
        .first()
    )

    return {
        "risk_level": prediction.risk_level if prediction else "UNKNOWN",
        "scores": {
            "academic": risk.academic_risk,
            "attendance": risk.attendance_risk,
            "behavior": risk.behavior_risk,
        },
        "explanation": generate_explanation(risk),
        "last_updated": risk.calculated_at,
    }


# =========================================================
# GOV-1 — Insight Acknowledgement
# =========================================================
@router.post("/acknowledge/{student_id}")
def acknowledge_student_insight(
    student_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role not in {"student", "parent", "admin"}:
        raise HTTPException(status_code=403, detail="Invalid role")

    review = acknowledge_insight(
        db,
        child_id=student_id,
        reviewer_id=user.id,
        reviewer_role=ReviewerRole(user.role),
    )

    return {
        "status": "acknowledged",
        "reviewed_at": review.reviewed_at,
        "reviewer_role": review.reviewer_role,
    }
