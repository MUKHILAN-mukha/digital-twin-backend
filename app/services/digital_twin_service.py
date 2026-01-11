from datetime import datetime
from sqlalchemy.orm import Session

from app.models.digital_twin import DigitalTwin
from app.services.digital_twin_versioning import persist_twin_version


def get_or_create_digital_twin(db: Session, student_id):
    """
    Guarantees that every student has exactly one Digital Twin.
    Initialization is deterministic and ML-agnostic.
    """

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.student_id == student_id)
        .first()
    )

    if twin:
        return twin

    twin = DigitalTwin(
        student_id=student_id,
        academic_score=0.0,
        attendance_score=0.0,
        behavior_score=0.0,
        twin_state="STABLE",  # neutral initial state
        last_updated=datetime.utcnow(),
    )

    db.add(twin)
    db.commit()
    db.refresh(twin)

    return twin


def update_digital_twin(
    db: Session,
    twin: DigitalTwin,
    *,
    academic_score: float,
    attendance_score: float,
    behavior_score: float,
    twin_state: str,
    predicted_gpa: float | None = None,
    failure_probability: float | None = None,
    forecast_confidence: float | None = None,
    explanation: str | None = None,
):
    """
    🔴 CRITICAL RULE:
    Every Digital Twin update MUST snapshot history first.
    """

    # 1️⃣ Persist previous state (DT-3)
    persist_twin_version(db, twin)

    # 2️⃣ Apply deterministic updates
    twin.academic_score = academic_score
    twin.attendance_score = attendance_score
    twin.behavior_score = behavior_score
    twin.twin_state = twin_state

    twin.predicted_gpa = predicted_gpa
    twin.failure_probability = failure_probability
    twin.forecast_confidence = forecast_confidence
    twin.explanation = explanation

    twin.last_updated = datetime.utcnow()

    db.commit()
    db.refresh(twin)

    return twin
