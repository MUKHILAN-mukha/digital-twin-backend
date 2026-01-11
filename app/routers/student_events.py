from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.student_event import StudentAcademicEvent
from app.schemas.student_event import (
    StudentEventCreate,
    StudentEventResponse
)
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/student/events",
    tags=["Student Academic Events"]
)


@router.post("/", response_model=StudentEventResponse)
def create_event(
    payload: StudentEventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    event = StudentAcademicEvent(
        student_id=user.id,
        event_type=payload.event_type,
        event_name=payload.event_name,
        score=payload.score,
        score_range=payload.score_range,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.get("/", response_model=list[StudentEventResponse])
def get_my_events(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    return (
        db.query(StudentAcademicEvent)
        .filter(StudentAcademicEvent.student_id == user.id)
        .order_by(StudentAcademicEvent.recorded_at.desc())
        .all()
    )
