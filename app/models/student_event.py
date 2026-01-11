import uuid
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StudentAcademicEvent(Base):
    __tablename__ = "student_academic_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    # attendance | exam | practice

    event_name: Mapped[str | None] = mapped_column(
        String(100)
    )
    # quarterly | half_yearly | board | writing_practice

    score: Mapped[int | None] = mapped_column(Integer)
    # marks or attendance %

    score_range: Mapped[str | None] = mapped_column(
        String(20)
    )
    # <50 | 50-75 | 76-100

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
