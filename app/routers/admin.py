from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.digital_twin_event import DigitalTwinEvent
from app.models.user import User
from app.schemas.admin_analytics import (
    StudentSummary,
    RiskSignal,
    MLFeatureSnapshot,
)
from app.core.permissions import require_roles

router = APIRouter(
    prefix="/admin",
    tags=["Admin Analytics"],
)
@router.get(
    "/students/summary",
    response_model=list[StudentSummary],
)
def get_student_summaries(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    rows = (
        db.query(
            DigitalTwinEvent.student_id,
            DigitalTwinEvent.event_type,
            func.count().label("count"),
        )
        .group_by(DigitalTwinEvent.student_id, DigitalTwinEvent.event_type)
        .all()
    )

    summary_map: dict = {}

    for student_id, event_type, count in rows:
        if student_id not in summary_map:
            summary_map[student_id] = {
                "student_id": student_id,
                "total_events": 0,
                "event_breakdown": {},
            }

        summary_map[student_id]["total_events"] += count
        summary_map[student_id]["event_breakdown"][event_type] = count

    return list(summary_map.values())
@router.get(
    "/students/risk",
    response_model=list[RiskSignal],
)
def detect_student_risks(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    risks = []

    students = (
        db.query(DigitalTwinEvent.student_id)
        .distinct()
        .all()
    )

    for (student_id,) in students:
        events = (
            db.query(DigitalTwinEvent)
            .filter(DigitalTwinEvent.student_id == student_id)
            .all()
        )

        reasons = []

        attendance = [
            e.payload.get("present")
            for e in events
            if e.event_type == "attendance"
        ]

        if attendance and attendance.count(False) >= 3:
            reasons.append("Frequent absences")

        sleep = [
            e.payload.get("hours")
            for e in events
            if e.event_type == "sleep"
        ]

        if sleep and sum(sleep) / len(sleep) < 6:
            reasons.append("Low average sleep")

        if reasons:
            risks.append(
                RiskSignal(
                    student_id=student_id,
                    risk_level="HIGH" if len(reasons) >= 2 else "MEDIUM",
                    reasons=reasons,
                )
            )

    return risks
@router.get(
    "/ml/features",
    response_model=list[MLFeatureSnapshot],
)
def export_ml_features(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    snapshots = []

    students = (
        db.query(DigitalTwinEvent.student_id)
        .distinct()
        .all()
    )

    for (student_id,) in students:
        events = (
            db.query(DigitalTwinEvent)
            .filter(DigitalTwinEvent.student_id == student_id)
            .all()
        )

        features = {
            "attendance_rate": 0,
            "avg_sleep_hours": None,
            "avg_study_hours": None,
            "total_events": len(events),
        }

        attendance = [
            e.payload.get("present")
            for e in events
            if e.event_type == "attendance"
        ]
        if attendance:
            features["attendance_rate"] = sum(attendance) / len(attendance)

        sleep = [
            e.payload.get("hours")
            for e in events
            if e.event_type == "sleep"
        ]
        if sleep:
            features["avg_sleep_hours"] = sum(sleep) / len(sleep)

        study = [
            e.payload.get("hours")
            for e in events
            if e.event_type == "study_hours"
        ]
        if study:
            features["avg_study_hours"] = sum(study) / len(study)

        snapshots.append(
            MLFeatureSnapshot(
                student_id=student_id,
                features=features,
            )
        )

    return snapshots
