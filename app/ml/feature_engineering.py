from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student_academic_event import StudentAcademicEvent
from app.models.digital_twin_event import DigitalTwinEvent
from app.services.feature_store import upsert_student_features


def compute_student_features(db: Session, student_id):
    now = datetime.utcnow()

    # ---------- Attendance ----------
    attendance_7d = (
        db.query(func.avg(StudentAcademicEvent.value))
        .filter(
            StudentAcademicEvent.student_id == student_id,
            StudentAcademicEvent.event_type == "attendance",
            StudentAcademicEvent.created_at >= now - timedelta(days=7),
        )
        .scalar()
        or 0.0
    )

    attendance_30d = (
        db.query(func.avg(StudentAcademicEvent.value))
        .filter(
            StudentAcademicEvent.student_id == student_id,
            StudentAcademicEvent.event_type == "attendance",
            StudentAcademicEvent.created_at >= now - timedelta(days=30),
        )
        .scalar()
        or 0.0
    )

    # ---------- Academic Performance ----------
    test_score_7d = (
        db.query(func.avg(StudentAcademicEvent.value))
        .filter(
            StudentAcademicEvent.student_id == student_id,
            StudentAcademicEvent.event_type == "test",
            StudentAcademicEvent.created_at >= now - timedelta(days=7),
        )
        .scalar()
        or 0.0
    )

    test_score_30d = (
        db.query(func.avg(StudentAcademicEvent.value))
        .filter(
            StudentAcademicEvent.student_id == student_id,
            StudentAcademicEvent.event_type == "test",
            StudentAcademicEvent.created_at >= now - timedelta(days=30),
        )
        .scalar()
        or 0.0
    )

    # ---------- Behavior ----------
    behavior_score_avg = (
        db.query(func.avg(DigitalTwinEvent.value))
        .filter(
            DigitalTwinEvent.student_id == student_id,
            DigitalTwinEvent.created_at >= now - timedelta(days=30),
        )
        .scalar()
        or 0.0
    )

    # ---------- Persist to Feature Store ----------
    return upsert_student_features(
        db=db,
        student_id=student_id,
        attendance_7d=attendance_7d,
        attendance_30d=attendance_30d,
        test_score_7d=test_score_7d,
        test_score_30d=test_score_30d,
        behavior_score_avg=behavior_score_avg,
    )
