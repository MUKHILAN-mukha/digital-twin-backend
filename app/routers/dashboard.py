from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.core.permissions import require_roles
from app.models.user import User

from app.models.parent_child_map import ParentChildMap
from app.models.digital_twin import DigitalTwin
from app.models.risk_score import RiskScore
from app.models.alert import Alert
from app.models.student_feature import StudentFeature
from app.models.prediction import StudentPrediction

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

# =========================================================
# DASH-1 — Student Dashboard
# =========================================================
@router.get("/student")
def student_dashboard(
    db: Session = Depends(get_db),
    student: User = Depends(require_roles("student")),
):
    # 1️⃣ Digital Twin
    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.student_id == student.id)
        .first()
    )

    if not twin:
        raise HTTPException(
            status_code=404,
            detail="Digital Twin not initialized",
        )

    # 2️⃣ Latest Risk Score
    risk = (
        db.query(RiskScore)
        .filter(RiskScore.student_id == student.id)
        .order_by(RiskScore.calculated_at.desc())
        .first()
    )

    # 3️⃣ Feature Snapshot
    features = (
        db.query(StudentFeature)
        .filter(StudentFeature.student_id == student.id)
        .order_by(StudentFeature.updated_at.desc())
        .first()
    )

    # 4️⃣ Alerts (unresolved)
    alerts = (
        db.query(Alert)
        .filter(
            Alert.student_id == student.id,
            Alert.resolved.is_(False),
        )
        .order_by(Alert.created_at.desc())
        .all()
    )

    # 5️⃣ Latest Prediction
    prediction = (
        db.query(StudentPrediction)
        .filter(StudentPrediction.student_id == student.id)
        .order_by(StudentPrediction.created_at.desc())
        .first()
    )

    # 6️⃣ Response (STRICT CONTRACT)
    return {
        "student_id": str(student.id),

        "twin": {
            "academic_score": twin.academic_score,
            "attendance_score": twin.attendance_score,
            "behavior_score": twin.behavior_score,
            "state": twin.twin_state,
        },

        "forecast": (
            {
                "predicted_gpa": prediction.predicted_gpa,
                "failure_probability": prediction.failure_probability,
                "confidence": prediction.confidence,
            }
            if prediction else None
        ),

        "risk": (
            {
                "academic_risk": risk.academic_risk,
                "attendance_risk": risk.attendance_risk,
                "behavior_risk": risk.behavior_risk,
                "volatility_risk": risk.volatility_risk,
                "total_risk": risk.total_risk,
            }
            if risk else None
        ),

        "features": (
            {
                "attendance_7d": features.attendance_7d,
                "attendance_30d": features.attendance_30d,
                "attendance_delta": features.attendance_delta,
                "test_score_7d": features.test_score_7d,
                "test_score_30d": features.test_score_30d,
                "test_score_delta": features.test_score_delta,
            }
            if features else None
        ),

        "alerts": [
            {
                "id": alert.id,
                "severity": alert.severity,
                "type": alert.alert_type,
                "message": alert.message,
                "created_at": alert.created_at,
            }
            for alert in alerts
        ],
    }


# =========================================================
# DASH-2 — Parent Dashboard
# =========================================================
@router.get("/parent")
def parent_dashboard(
    db: Session = Depends(get_db),
    parent: User = Depends(require_roles("parent")),
):
    # 1️⃣ Parent → Child mappings
    mappings = (
        db.query(ParentChildMap)
        .filter(ParentChildMap.parent_id == parent.id)
        .all()
    )

    if not mappings:
        return {
            "parent_id": str(parent.id),
            "children": [],
        }

    child_ids = [m.child_id for m in mappings]

    # 2️⃣ Digital Twins
    twins = {
        t.student_id: t
        for t in db.query(DigitalTwin)
        .filter(DigitalTwin.student_id.in_(child_ids))
        .all()
    }

    # 3️⃣ Latest Risk Score per child
    risk_subq = (
        db.query(
            RiskScore.student_id,
            func.max(RiskScore.calculated_at).label("latest"),
        )
        .filter(RiskScore.student_id.in_(child_ids))
        .group_by(RiskScore.student_id)
        .subquery()
    )

    risks = {
        r.student_id: r
        for r in (
            db.query(RiskScore)
            .join(
                risk_subq,
                (RiskScore.student_id == risk_subq.c.student_id)
                & (RiskScore.calculated_at == risk_subq.c.latest),
            )
            .all()
        )
    }

    # 4️⃣ Active alert counts
    alert_counts = dict(
        db.query(
            Alert.student_id,
            func.count(Alert.id),
        )
        .filter(
            Alert.student_id.in_(child_ids),
            Alert.resolved.is_(False),
        )
        .group_by(Alert.student_id)
        .all()
    )

    # 5️⃣ Response
    children_payload = []

    for child_id in child_ids:
        twin = twins.get(child_id)
        risk = risks.get(child_id)

        if not twin:
            continue

        children_payload.append(
            {
                "child_id": str(child_id),
                "twin_state": twin.twin_state,
                "academic_score": twin.academic_score,
                "attendance_score": twin.attendance_score,
                "behavior_score": twin.behavior_score,
                "risk_score": risk.total_risk if risk else None,
                "active_alerts": alert_counts.get(child_id, 0),
            }
        )

    return {
        "parent_id": str(parent.id),
        "children": children_payload,
    }
