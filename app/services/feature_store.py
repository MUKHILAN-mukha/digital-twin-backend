from sqlalchemy.orm import Session
from datetime import datetime

from app.models.student_feature import StudentFeature


def upsert_student_features(
    *,
    db: Session,
    student_id,
    attendance_7d: float,
    attendance_30d: float,
    test_score_7d: float,
    test_score_30d: float,
    behavior_score_avg: float,
):
    attendance_delta = attendance_7d - attendance_30d
    test_score_delta = test_score_7d - test_score_30d

    features = (
        db.query(StudentFeature)
        .filter(StudentFeature.student_id == student_id)
        .first()
    )

    if not features:
        features = StudentFeature(
            student_id=student_id,
            attendance_7d=attendance_7d,
            attendance_30d=attendance_30d,
            attendance_delta=attendance_delta,
            test_score_7d=test_score_7d,
            test_score_30d=test_score_30d,
            test_score_delta=test_score_delta,
            behavior_score_avg=behavior_score_avg,
            updated_at=datetime.utcnow(),
        )
        db.add(features)
    else:
        features.attendance_7d = attendance_7d
        features.attendance_30d = attendance_30d
        features.attendance_delta = attendance_delta
        features.test_score_7d = test_score_7d
        features.test_score_30d = test_score_30d
        features.test_score_delta = test_score_delta
        features.behavior_score_avg = behavior_score_avg
        features.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(features)
    return features
