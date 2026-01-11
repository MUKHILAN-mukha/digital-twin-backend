from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.parent_profile import ParentProfile
from app.models.user import User
from app.schemas.parent_profile import (
    ParentProfileCreate,
    ParentProfileUpdate,
    ParentProfileResponse,
)
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles

router = APIRouter(
    prefix="/parent",
    tags=["Parent"],
)


@router.post(
    "/profile",
    response_model=ParentProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_parent_profile(
    payload: ParentProfileCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("parent")),
):
    if db.query(ParentProfile).filter_by(user_id=user.id).first():
        raise HTTPException(
            status_code=400,
            detail="Parent profile already exists",
        )

    profile = ParentProfile(
        user_id=user.id,
        phone=payload.phone,
        occupation=payload.occupation,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get(
    "/profile",
    response_model=ParentProfileResponse,
)
def get_parent_profile(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("parent")),
):
    profile = db.query(ParentProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put(
    "/profile",
    response_model=ParentProfileResponse,
)
def update_parent_profile(
    payload: ParentProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("parent")),
):
    profile = db.query(ParentProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # FULL REPLACEMENT
    profile.phone = payload.phone
    profile.occupation = payload.occupation

    db.commit()
    db.refresh(profile)
    return profile
