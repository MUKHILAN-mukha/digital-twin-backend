from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.alert import Alert
from app.models.risk_score import RiskScore

# ==========================
# CONFIGURATION (POLICY)
# ==========================

ACADEMIC_HIGH = 70
ATTENDANCE_HIGH = 65
BEHAVIOR_HIGH = 60
TOTAL_HIGH = 75

COOLDOWN_HOURS = 24
ESCALATION_COUNT = 3
PERSISTENCE_DAYS = 14


# ==========================
# PUBLIC ENTRY POINT
# ==========================

def generate_alerts(db: Session, risk: RiskScore) -> None:
    """
    Deterministic, idempotent alert engine.
    Safe to call on every risk calculation.
    """

    _maybe_create_alert(
        db,
        risk.student_id,
        "ACADEMIC_RISK",
        risk.academic_risk,
        ACADEMIC_HIGH,
        "Academic performance shows high failure risk",
    )

    _maybe_create_alert(
        db,
        risk.student_id,
        "ATTENDANCE_RISK",
        risk.attendance_risk,
        ATTENDANCE_HIGH,
        "Attendance pattern indicates instability",
    )

    _maybe_create_alert(
        db,
        risk.student_id,
        "BEHAVIOR_RISK",
        risk.behavior_risk,
        BEHAVIOR_HIGH,
        "Behavioral consistency is declining",
    )

    _maybe_create_alert(
        db,
        risk.student_id,
        "OVERALL_RISK",
        risk.total_risk,
        TOTAL_HIGH,
        "Student is at high overall academic risk",
    )


# ==========================
# INTERNAL HELPERS
# ==========================

def _maybe_create_alert(
    db: Session,
    student_id,
    alert_type: str,
    value: float,
    threshold: float,
    message: str,
):
    if value < threshold:
        return

    severity = _determine_severity(alert_type, value)

    if _is_in_cooldown(db, student_id, alert_type):
        return

    severity = _apply_escalation(db, student_id, alert_type, severity)

    alert = Alert(
        student_id=student_id,
        alert_type=alert_type,
        severity=severity,
        message=message,
        resolved=False,
        created_at=datetime.utcnow(),
    )

    db.add(alert)
    db.commit()


def _determine_severity(alert_type: str, value: float) -> str:
    if alert_type == "OVERALL_RISK":
        return "HIGH"
    return "HIGH" if value >= 80 else "MEDIUM"


def _is_in_cooldown(db: Session, student_id, alert_type: str) -> bool:
    last_alert = (
        db.query(Alert)
        .filter(
            Alert.student_id == student_id,
            Alert.alert_type == alert_type,
            Alert.resolved == False,
        )
        .order_by(Alert.created_at.desc())
        .first()
    )

    if not last_alert:
        return False

    return datetime.utcnow() - last_alert.created_at < timedelta(hours=COOLDOWN_HOURS)


def _apply_escalation(
    db: Session,
    student_id,
    alert_type: str,
    current_severity: str,
) -> str:
    if current_severity != "MEDIUM":
        return current_severity

    since = datetime.utcnow() - timedelta(days=PERSISTENCE_DAYS)

    count = (
        db.query(func.count(RiskScore.id))
        .filter(
            RiskScore.student_id == student_id,
            RiskScore.total_risk >= TOTAL_HIGH,
            RiskScore.calculated_at >= since,
        )
        .scalar()
    )

    return "HIGH" if count >= ESCALATION_COUNT else current_severity
