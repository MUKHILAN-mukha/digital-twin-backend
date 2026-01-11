from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.schemas.student_profile import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
)
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles

router = APIRouter(
    prefix="/student",
    tags=["Student"],
)


@router.post(
    "/profile",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student_profile(
    payload: StudentProfileCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("student")),
):
    if db.query(StudentProfile).filter_by(user_id=user.id).first():
        raise HTTPException(
            status_code=400,
            detail="Student profile already exists",
        )

    profile = StudentProfile(
        user_id=user.id,
        class_level=payload.class_level,
        board=payload.board,
        school_name=payload.school_name,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get(
    "/profile",
    response_model=StudentProfileResponse,
)
def get_student_profile(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("student")),
):
    profile = db.query(StudentProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put(
    "/profile",
    response_model=StudentProfileResponse,
)
def update_student_profile(
    payload: StudentProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("student")),
):
    profile = db.query(StudentProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # FULL REPLACEMENT
    profile.class_level = payload.class_level
    profile.board = payload.board
    profile.school_name = payload.school_name

    db.commit()
    db.refresh(profile)
    return profile
