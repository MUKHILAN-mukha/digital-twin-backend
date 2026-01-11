# app/models/digital_twin.py

import uuid
from datetime import datetime
from sqlalchemy import Float, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DigitalTwin(Base):
    __tablename__ = "digital_twins"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )

    # --- CORE TWIN STATE (ONLY) ---
    academic_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    attendance_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    behavior_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    twin_state: Mapped[str] = mapped_column(
        String(20),
        default="STABLE",   # STABLE | IMPROVING | AT_RISK
        index=True,
        nullable=False,
    )

    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
