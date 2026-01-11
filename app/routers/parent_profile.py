from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.parent_profile import ParentProfile
from app.schemas.parent_profile import (
    ParentProfileCreate,
    ParentProfileResponse
)
from app.models.user import User

router = APIRouter(
    prefix="/parent/profile",
    tags=["Parent Profile"]
)


@router.post("/", response_model=ParentProfileResponse)
def create_profile(
    payload: ParentProfileCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "parent":
        raise HTTPException(status_code=403, detail="Only parents allowed")

    if db.query(ParentProfile).filter_by(user_id=user.id).first():
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = ParentProfile(
        user_id=user.id,
        phone=payload.phone,
        occupation=payload.occupation
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get("/", response_model=ParentProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = db.query(ParentProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
