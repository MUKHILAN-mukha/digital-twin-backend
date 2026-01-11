from pydantic import BaseModel, Field
from uuid import UUID


class StudentProfileBase(BaseModel):
    class_level: int = Field(..., ge=1, le=12)
    board: str
    school_name: str


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(StudentProfileBase):
    """
    FULL UPDATE:
    All fields required.
    Missing field = client error.
    """
    pass


class StudentProfileResponse(StudentProfileBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
