import uuid
from datetime import datetime
from sqlalchemy import Float, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DigitalTwinHistory(Base):
    __tablename__ = "digital_twin_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # Snapshot values
    academic_score: Mapped[float] = mapped_column(Float, nullable=False)
    attendance_score: Mapped[float] = mapped_column(Float, nullable=False)
    behavior_score: Mapped[float] = mapped_column(Float, nullable=False)

    twin_state: Mapped[str] = mapped_column(String(20), nullable=False)

    predicted_gpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    failure_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    forecast_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    versioned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        index=True,
        nullable=False,
    )
