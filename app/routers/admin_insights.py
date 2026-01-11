from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.permissions import require_roles
from app.models.insight_review import InsightReview

router = APIRouter(
    prefix="/admin/insights",
    tags=["Admin – Governance"],
)


@router.get("/acknowledgments")
def insight_ack_audit(
    db: Session = Depends(get_db),
    admin = Depends(require_roles("admin")),
):
    return (
        db.query(InsightReview)
        .order_by(InsightReview.reviewed_at.desc())
        .all()
    )
