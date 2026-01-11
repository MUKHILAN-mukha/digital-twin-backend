from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Any, List


class StudentSummary(BaseModel):
    student_id: UUID
    total_events: int
    event_breakdown: Dict[str, int]


class RiskSignal(BaseModel):
    student_id: UUID
    risk_level: str
    reasons: List[str]


class MLFeatureSnapshot(BaseModel):
    student_id: UUID
    features: Dict[str, Any]
