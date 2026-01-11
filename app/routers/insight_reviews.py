from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.insight_review import InsightReview
from app.models.user import User

router = APIRouter(
    prefix="/insights",
    tags=["Insight Reviews"],
)

# ---------------------------------------------------------
# POST — Acknowledge Insight
# ---------------------------------------------------------
@router.post("/acknowledge")
def acknowledge_insight(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role not in {"student", "parent"}:
        raise HTTPException(
            status_code=403,
            detail="Only student or parent can acknowledge insights",
        )

    # Prevent duplicate acknowledgments
    existing = (
        db.query(InsightReview)
        .filter(
            InsightReview.child_id == user.id,
            InsightReview.reviewer_id == user.id,
        )
        .first()
    )

    if existing:
        return {
            "status": "already_acknowledged",
            "acknowledged_at": existing.reviewed_at,
        }

    review = InsightReview(
        child_id=user.id,
        reviewer_id=user.id,
        reviewer_role=user.role,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "status": "acknowledged",
        "acknowledged_at": review.reviewed_at,
    }


# ---------------------------------------------------------
# GET — Check acknowledgment status
# ---------------------------------------------------------
@router.get("/acknowledgment-status")
def insight_ack_status(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    review = (
        db.query(InsightReview)
        .filter(
            InsightReview.child_id == user.id,
            InsightReview.reviewer_id == user.id,
        )
        .first()
    )

    return {
        "acknowledged": bool(review),
        "acknowledged_at": review.reviewed_at if review else None,
    }
