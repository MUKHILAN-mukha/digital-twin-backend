from typing import Optional
from app.models.digital_twin import DigitalTwin


CRITICAL_ACADEMIC = 40
CRITICAL_ATTENDANCE = 60
CRITICAL_BEHAVIOR = 40


def compute_twin_state(
    *,
    academic_score: float,
    attendance_score: float,
    behavior_score: float,
    prev_academic: Optional[float] = None,
    prev_attendance: Optional[float] = None,
    prev_behavior: Optional[float] = None,
    failure_probability: Optional[float] = None,
) -> str:
    """
    Deterministic Digital Twin State Logic
    """

    # 1️⃣ AT_RISK — absolute conditions
    if (
        academic_score < CRITICAL_ACADEMIC
        or attendance_score < CRITICAL_ATTENDANCE
        or behavior_score < CRITICAL_BEHAVIOR
        or (failure_probability is not None and failure_probability >= 0.6)
    ):
        return "AT_RISK"

    # 2️⃣ IMPROVING — trend-based
    if prev_academic is not None:
        improvements = 0

        if academic_score - prev_academic >= 5:
            improvements += 1
        if attendance_score - prev_attendance >= 5:
            improvements += 1
        if behavior_score - prev_behavior >= 5:
            improvements += 1

        if improvements >= 2:
            return "IMPROVING"

    # 3️⃣ Default
    return "STABLE"
