# app/services/twin_state_logic.py

from app.models.digital_twin import TwinStateEnum


def compute_twin_state(
    academic_score: float,
    attendance_score: float,
    behavior_score: float,
) -> TwinStateEnum:
    """
    Deterministic Digital Twin state computation.
    Same inputs will always produce the same state.
    """

    # 1️⃣ At-risk conditions (early exit)
    if (
        academic_score < 40
        or attendance_score < 50
        or behavior_score < 40
    ):
        return TwinStateEnum.AT_RISK

    # 2️⃣ Improving trajectory
    if (
        academic_score >= 50
        and attendance_score >= 50
        and behavior_score >= 50
        and (
            academic_score >= 70
            or attendance_score >= 70
            or behavior_score >= 70
        )
    ):
        return TwinStateEnum.IMPROVING

    # 3️⃣ Default stable state
    return TwinStateEnum.STABLE
