from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.core.permissions import require_roles
from app.models.user import User
from app.models.digital_twin import DigitalTwin
from app.models.risk_score import RiskScore
from app.models.alert import Alert
from app.models.prediction import StudentPrediction
from app.models.insight_review import InsightReview

router = APIRouter(
    prefix="/dashboard",
    tags=["Admin Dashboard"],
)


@router.get("/admin")
def admin_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    # -------------------------------------------------
    # 1️⃣ User counts
    # -------------------------------------------------
    total_students = (
        db.query(User)
        .filter(User.role == "student")
        .count()
    )

    total_parents = (
        db.query(User)
        .filter(User.role == "parent")
        .count()
    )

    # -------------------------------------------------
    # 2️⃣ Digital Twin state distribution
    # -------------------------------------------------
    twin_states = dict(
        db.query(
            DigitalTwin.twin_state,
            func.count(DigitalTwin.id),
        )
        .group_by(DigitalTwin.twin_state)
        .all()
    )

    # -------------------------------------------------
    # 3️⃣ Latest Risk Scores (institution snapshot)
    # -------------------------------------------------
    latest_risk_subq = (
        db.query(
            RiskScore.student_id,
            func.max(RiskScore.calculated_at).label("latest"),
        )
        .group_by(RiskScore.student_id)
        .subquery()
    )

    latest_risks = (
        db.query(RiskScore)
        .join(
            latest_risk_subq,
            (RiskScore.student_id == latest_risk_subq.c.student_id)
            & (RiskScore.calculated_at == latest_risk_subq.c.latest),
        )
        .all()
    )

    avg_risk = (
        sum(r.total_risk for r in latest_risks) / len(latest_risks)
        if latest_risks else 0.0
    )

    high_risk_count = sum(
        1 for r in latest_risks if r.total_risk >= 75
    )

    # -------------------------------------------------
    # 4️⃣ Alerts overview
    # -------------------------------------------------
    alert_counts = dict(
        db.query(
            Alert.severity,
            func.count(Alert.id),
        )
        .filter(Alert.resolved == False)
        .group_by(Alert.severity)
        .all()
    )

    # -------------------------------------------------
    # 5️⃣ ML Prediction confidence
    # -------------------------------------------------
    avg_prediction_confidence = (
        db.query(func.avg(StudentPrediction.confidence))
        .scalar()
        or 0.0
    )

    # -------------------------------------------------
    # 6️⃣ Governance – unacknowledged insights
    # -------------------------------------------------
    acknowledged_students = (
        db.query(InsightReview.child_id)
        .distinct()
        .subquery()
    )

    unacknowledged_count = (
        db.query(DigitalTwin)
        .filter(
            ~DigitalTwin.student_id.in_(acknowledged_students)
        )
        .count()
    )

    # -------------------------------------------------
    # ✅ Final Admin Payload (PDF-aligned)
    # -------------------------------------------------
    return {
        "users": {
            "students": total_students,
            "parents": total_parents,
        },
        "digital_twins": {
            "state_distribution": {
                "STABLE": twin_states.get("STABLE", 0),
                "IMPROVING": twin_states.get("IMPROVING", 0),
                "AT_RISK": twin_states.get("AT_RISK", 0),
            }
        },
        "risk": {
            "average_risk": round(avg_risk, 2),
            "high_risk_students": high_risk_count,
        },
        "alerts": {
            "LOW": alert_counts.get("LOW", 0),
            "MEDIUM": alert_counts.get("MEDIUM", 0),
            "HIGH": alert_counts.get("HIGH", 0),
        },
        "ml": {
            "average_prediction_confidence": round(
                avg_prediction_confidence, 3
            )
        },
        "governance": {
            "unacknowledged_insights": unacknowledged_count
        },
    }
