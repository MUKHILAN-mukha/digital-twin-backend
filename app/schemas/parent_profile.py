from pydantic import BaseModel, Field
from uuid import UUID


class ParentProfileBase(BaseModel):
    phone: str = Field(..., min_length=8, max_length=20)
    occupation: str = Field(..., min_length=2, max_length=100)


class ParentProfileCreate(ParentProfileBase):
    pass


class ParentProfileUpdate(ParentProfileBase):
    """
    FULL UPDATE ONLY.
    All fields mandatory.
    """
    pass


class ParentProfileResponse(ParentProfileBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
