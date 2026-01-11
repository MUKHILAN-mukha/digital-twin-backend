from sqlalchemy.orm import Session
from app.models.digital_twin_event import DigitalTwinEvent
from app.ml.contracts import StudentFeatureVector


def build_features(
    db: Session,
    student_id,
) -> StudentFeatureVector:
    events = (
        db.query(DigitalTwinEvent)
        .filter(DigitalTwinEvent.student_id == student_id)
        .all()
    )

    attendance = []
    sleep = []
    study = []

    for e in events:
        if e.event_type == "attendance":
            attendance.append(e.payload.get("present"))
        elif e.event_type == "sleep":
            sleep.append(e.payload.get("hours"))
        elif e.event_type == "study_hours":
            study.append(e.payload.get("hours"))

    return {
        "attendance_rate": (
            sum(attendance) / len(attendance)
            if attendance else 0.0
        ),
        "avg_sleep_hours": (
            sum(sleep) / len(sleep)
            if sleep else None
        ),
        "avg_study_hours": (
            sum(study) / len(study)
            if study else None
        ),
        "total_events": len(events),
    }
