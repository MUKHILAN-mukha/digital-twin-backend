from sqlalchemy.orm import Session

from app.models.digital_twin import DigitalTwin
from app.models.digital_twin_history import DigitalTwinHistory


def persist_twin_version(
    db: Session,
    twin: DigitalTwin,
):
    """
    Creates an immutable snapshot BEFORE mutation.
    Must NOT commit independently.
    """

    history = DigitalTwinHistory(
        student_id=twin.student_id,
        academic_score=twin.academic_score,
        attendance_score=twin.attendance_score,
        behavior_score=twin.behavior_score,
        twin_state=twin.twin_state,
        predicted_gpa=twin.predicted_gpa,
        failure_probability=twin.failure_probability,
        forecast_confidence=twin.forecast_confidence,
        explanation=twin.explanation,
    )

    db.add(history)
