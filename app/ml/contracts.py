from typing import TypedDict


class StudentFeatureVector(TypedDict):
    attendance_rate: float
    avg_sleep_hours: float | None
    avg_study_hours: float | None
    total_events: int
