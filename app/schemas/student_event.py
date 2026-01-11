from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class StudentEventCreate(BaseModel):
    event_type: str
    event_name: str | None = None
    score: int | None = None
    score_range: str | None = None


class StudentEventResponse(StudentEventCreate):
    id: UUID
    student_id: UUID
    recorded_at: datetime

    class Config:
        from_attributes = True
