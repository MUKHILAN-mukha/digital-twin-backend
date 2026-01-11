from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Dict, Any


class DigitalTwinEventCreate(BaseModel):
    event_type: str = Field(..., min_length=3, max_length=50)
    payload: Dict[str, Any]


class DigitalTwinEventResponse(BaseModel):
    id: UUID
    student_id: UUID
    event_type: str
    payload: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
