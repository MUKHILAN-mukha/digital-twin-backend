from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.core.permissions import require_roles
from app.models.insight_review import InsightReview
from app.models.user import User
from app.models.risk_score import RiskScore

router = APIRouter(
    prefix="/admin/acknowledgments",
    tags=["Admin Governance"],
)

@router.get("/")
def acknowledgment_audit(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    rows = (
        db.query(
            RiskScore.student_id,
            func.max(RiskScore.calculated_at).label("risk_time"),
            InsightReview.reviewed_at,
        )
        .outerjoin(
            InsightReview,
            InsightReview.child_id == RiskScore.student_id,
        )
        .group_by(
            RiskScore.student_id,
            InsightReview.reviewed_at,
        )
        .all()
    )

    return [
        {
            "student_id": str(r.student_id),
            "risk_generated_at": r.risk_time,
            "acknowledged": bool(r.reviewed_at),
            "acknowledged_at": r.reviewed_at,
        }
        for r in rows
    ]
