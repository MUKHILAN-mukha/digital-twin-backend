from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.user import User
from app.models.risk_score import RiskScore
from app.core.permissions import require_roles

router = APIRouter(
    prefix="/dashboard/admin",
    tags=["Admin Dashboard"],
)


@router.get("")
def admin_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    total_students = db.query(User).filter(User.role == "student").count()

    high_risk = (
        db.query(RiskScore)
        .filter(RiskScore.total_risk >= 80)
        .count()
    )

    avg_risk = db.query(func.avg(RiskScore.total_risk)).scalar() or 0

    return {
        "total_students": total_students,
        "high_risk_students": high_risk,
        "average_risk": round(avg_risk, 2),
        "system_status": "HEALTHY",
    }
