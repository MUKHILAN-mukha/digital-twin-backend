from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.digital_twin_event import DigitalTwinEvent
from app.models.user import User
from app.schemas.digital_twin_event import (
    DigitalTwinEventCreate,
    DigitalTwinEventResponse,
)
from app.core.permissions import require_roles
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/digital-twin",
    tags=["Digital Twin"],
)
@router.post(
    "/events",
    response_model=DigitalTwinEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    payload: DigitalTwinEventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("student")),
):
    event = DigitalTwinEvent(
        student_id=user.id,
        event_type=payload.event_type,
        payload=payload.payload,
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    return event
@router.get(
    "/events",
    response_model=list[DigitalTwinEventResponse],
)
def get_my_events(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("student")),
):
    return (
        db.query(DigitalTwinEvent)
        .filter(DigitalTwinEvent.student_id == user.id)
        .order_by(DigitalTwinEvent.created_at.desc())
        .all()
    )
@router.get(
    "/admin/events/{student_id}",
    response_model=list[DigitalTwinEventResponse],
)
def admin_get_student_events(
    student_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    events = (
        db.query(DigitalTwinEvent)
        .filter(DigitalTwinEvent.student_id == student_id)
        .order_by(DigitalTwinEvent.created_at.desc())
        .all()
    )

    if not events:
        raise HTTPException(
            status_code=404,
            detail="No events found for student",
        )

    return events
