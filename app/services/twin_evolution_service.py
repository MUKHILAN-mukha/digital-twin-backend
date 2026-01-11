# app/services/twin_evolution_service.py

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.digital_twin import DigitalTwin
from app.services.twin_state_logic import compute_twin_state
from app.services.digital_twin_service import get_or_create_digital_twin


def evolve_digital_twin(
    db: Session,
    student_id,
    *,
    academic_score: float,
    attendance_score: float,
    behavior_score: float,
    predicted_gpa: float | None = None,
    failure_probability: float | None = None,
    forecast_confidence: float | None = None,
    explanation: str | None = None,
) -> DigitalTwin:
    """
    Single source of truth for Digital Twin evolution.

    Rules:
    - Deterministic
    - No randomness
    - Always recompute state
    - One commit only
    """

    # 1️⃣ Ensure twin exists (DT-1 guarantee)
    twin = get_or_create_digital_twin(db, student_id)

    # 2️⃣ Update core scores
    twin.academic_score = academic_score
    twin.attendance_score = attendance_score
    twin.behavior_score = behavior_score

    # 3️⃣ Compute state (DT-2)
    twin.twin_state = compute_twin_state(
        academic_score=academic_score,
        attendance_score=attendance_score,
        behavior_score=behavior_score,
    ).value

    # 4️⃣ Optional forecast fields (ML-driven)
    if predicted_gpa is not None:
        twin.predicted_gpa = predicted_gpa

    if failure_probability is not None:
        twin.failure_probability = failure_probability

    if forecast_confidence is not None:
        twin.forecast_confidence = forecast_confidence

    # 5️⃣ Explanation (human-readable)
    if explanation:
        twin.explanation = explanation

    # 6️⃣ Timestamp
    twin.last_updated = datetime.utcnow()

    # 7️⃣ Persist
    db.add(twin)
    db.commit()
    db.refresh(twin)

    return twin
