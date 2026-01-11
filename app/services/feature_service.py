from datetime import datetime
from sqlalchemy.orm import Session

from app.models.student_feature import StudentFeature
from app.ml.feature_schema import FEATURE_SCHEMA_VERSION, FEATURE_COLUMNS


def upsert_student_features(db: Session, student_id, feature_dict: dict):
    # 🚨 Hard validation (no silent corruption)
    unknown = set(feature_dict.keys()) - FEATURE_COLUMNS
    if unknown:
        raise ValueError(f"Unknown feature fields: {unknown}")

    features = (
        db.query(StudentFeature)
        .filter(StudentFeature.student_id == student_id)
        .first()
    )

    if not features:
        features = StudentFeature(
            student_id=student_id,
            feature_version=FEATURE_SCHEMA_VERSION,
        )
        db.add(features)

    # 🚨 Version mismatch protection
    if features.feature_version != FEATURE_SCHEMA_VERSION:
        raise RuntimeError(
            f"Feature version mismatch: "
            f"{features.feature_version} != {FEATURE_SCHEMA_VERSION}"
        )

    for key, value in feature_dict.items():
        setattr(features, key, value)

    features.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(features)
    return features


def get_student_feature_dict(db: Session, student_id):
    features = (
        db.query(StudentFeature)
        .filter(StudentFeature.student_id == student_id)
        .first()
    )

    if not features:
        return None

    if features.feature_version != FEATURE_SCHEMA_VERSION:
        raise RuntimeError(
            "Feature schema version mismatch during read"
        )

    return {
        "attendance_7d": features.attendance_7d,
        "attendance_30d": features.attendance_30d,
        "attendance_delta": features.attendance_delta,
        "test_score_7d": features.test_score_7d,
        "test_score_30d": features.test_score_30d,
        "test_score_delta": features.test_score_delta,
        "behavior_score_avg": features.behavior_score_avg,
    }
