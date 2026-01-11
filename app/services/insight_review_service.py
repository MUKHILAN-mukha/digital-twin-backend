from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.insight_review import InsightReview, ReviewerRole


def acknowledge_insight(
    db: Session,
    *,
    child_id,
    reviewer_id,
    reviewer_role: ReviewerRole,
):
    """
    Records acknowledgment of insights.
    Enforces idempotency at DB + service level.
    """

    existing = (
        db.query(InsightReview)
        .filter(
            InsightReview.child_id == child_id,
            InsightReview.reviewer_id == reviewer_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Insights already acknowledged",
        )

    review = InsightReview(
        child_id=child_id,
        reviewer_id=reviewer_id,
        reviewer_role=reviewer_role,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review
