from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.digital_twin_event import DigitalTwinEvent
from app.models.user import User

router = APIRouter(
    prefix="/digital-twin/events",
    tags=["Digital Twin Events"]
)


@router.post("/")
def add_event(
    category: str,
    value: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    event = DigitalTwinEvent(
        student_id=user.id,
        category=category,
        value=value
    )

    db.add(event)
    db.commit()
    return {"status": "recorded"}
