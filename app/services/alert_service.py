from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.insight_review import InsightReview
from app.models.risk_score import RiskScore

ESCALATION_HOURS = 48
ADMIN_ESCALATION_HOURS = 72


def generate_or_escalate_alert(db: Session, student_id):
    # Latest risk
    risk = (
        db.query(RiskScore)
        .filter(RiskScore.student_id == student_id)
        .order_by(RiskScore.calculated_at.desc())
        .first()
    )

    if not risk:
        return None

    # Determine severity
    if risk.total_risk >= 75:
        severity = "HIGH"
    elif risk.total_risk >= 50:
        severity = "MEDIUM"
    else:
        return None  # no alert

    # Existing unresolved alert?
    alert = (
        db.query(Alert)
        .filter(
            Alert.student_id == student_id,
            Alert.resolved == False,
        )
        .first()
    )

    if not alert:
        alert = Alert(
            student_id=student_id,
            severity=severity,
            alert_type="RISK",
            message="Academic risk detected",
        )
        db.add(alert)
        db.commit()
        return alert

    # Check acknowledgment
    acknowledged = (
        db.query(InsightReview)
        .filter(InsightReview.child_id == student_id)
        .first()
    )

    hours_passed = (
        datetime.utcnow() - alert.created_at
    ).total_seconds() / 3600

    if not acknowledged and hours_passed >= ESCALATION_HOURS:
        alert.severity = "HIGH"
        alert.message = "Risk unacknowledged — escalation triggered"

    db.commit()
    return alert
