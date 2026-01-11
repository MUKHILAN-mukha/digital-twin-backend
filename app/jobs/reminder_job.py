from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.insight_review import InsightReview

REMINDER_HOURS = 24


def run_acknowledgment_reminders(db: Session):
    alerts = (
        db.query(Alert)
        .filter(Alert.resolved == False)
        .all()
    )

    for alert in alerts:
        acknowledged = (
            db.query(InsightReview)
            .filter(InsightReview.child_id == alert.student_id)
            .first()
        )

        hours_passed = (
            datetime.utcnow() - alert.created_at
        ).total_seconds() / 3600

        if not acknowledged and hours_passed >= REMINDER_HOURS:
            alert.message = "Reminder: Please review academic risk insights"
            db.commit()
