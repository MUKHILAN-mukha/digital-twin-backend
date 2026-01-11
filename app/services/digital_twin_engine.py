from datetime import datetime
from sqlalchemy.orm import Session

from app.models.digital_twin import DigitalTwin
from app.services.digital_twin_logic import compute_twin_state


def evolve_digital_twin(
    *,
    db: Session,
    student_id,
    academic_score: float,
    attendance_score: float,
    behavior_score: float,
    failure_probability: float | None = None,
):
    """
    Core Digital Twin Evolution Engine
    """

    twin = (
        db.query(DigitalTwin)
        .filter(DigitalTwin.student_id == student_id)
        .first()
    )

    # --- Capture previous state for trend detection
    prev_academic = twin.academic_score if twin else None
    prev_attendance = twin.attendance_score if twin else None
    prev_behavior = twin.behavior_score if twin else None

    # --- Compute new state
    new_state = compute_twin_state(
        academic_score=academic_score,
        attendance_score=attendance_score,
        behavior_score=behavior_score,
        prev_academic=prev_academic,
        prev_attendance=prev_attendance,
        prev_behavior=prev_behavior,
        failure_probability=failure_probability,
    )

    # --- Create or Update Twin
    if not twin:
        twin = DigitalTwin(
            student_id=student_id,
            academic_score=academic_score,
            attendance_score=attendance_score,
            behavior_score=behavior_score,
            twin_state=new_state,
            predicted_gpa=None,
            failure_probability=failure_probability,
            forecast_confidence=None,
            explanation="Initial Digital Twin created",
            last_updated=datetime.utcnow(),
        )
        db.add(twin)
    else:
        twin.academic_score = academic_score
        twin.attendance_score = attendance_score
        twin.behavior_score = behavior_score
        twin.twin_state = new_state
        twin.failure_probability = failure_probability
        twin.last_updated = datetime.utcnow()
        twin.explanation = "Digital Twin updated from new event data"

    db.commit()
    db.refresh(twin)

    return twin
