import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DigitalTwinEvent(Base):
    __tablename__ = "digital_twin_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    """
    Examples:
    - attendance
    - test_score
    - study_hours
    - sleep
    - screen_time
    - physical_activity
    """

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    """
    Flexible ML-ready data:
    {
        "value": 85,
        "subject": "math",
        "duration": 6,
        "unit": "hours"
    }
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    student = relationship("User")
