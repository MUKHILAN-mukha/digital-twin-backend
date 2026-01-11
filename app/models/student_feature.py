import uuid
from datetime import datetime
from sqlalchemy import Float, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StudentFeature(Base):
    __tablename__ = "student_features"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    # 🔒 Feature schema version
    feature_version: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        index=True,
    )

    # Attendance
    attendance_7d: Mapped[float] = mapped_column(Float, default=0.0)
    attendance_30d: Mapped[float] = mapped_column(Float, default=0.0)
    attendance_delta: Mapped[float] = mapped_column(Float, default=0.0)

    # Academics
    test_score_7d: Mapped[float] = mapped_column(Float, default=0.0)
    test_score_30d: Mapped[float] = mapped_column(Float, default=0.0)
    test_score_delta: Mapped[float] = mapped_column(Float, default=0.0)

    # Behavior
    behavior_score_avg: Mapped[float] = mapped_column(Float, default=0.0)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
