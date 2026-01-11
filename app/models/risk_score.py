import uuid
from datetime import datetime
from sqlalchemy import Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

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

    # Final scores
    academic_risk: Mapped[float] = mapped_column(Float, nullable=False)
    attendance_risk: Mapped[float] = mapped_column(Float, nullable=False)
    behavior_risk: Mapped[float] = mapped_column(Float, nullable=False)
    volatility_risk: Mapped[float] = mapped_column(Float, nullable=False)

    total_risk: Mapped[float] = mapped_column(Float, nullable=False)

    # 🔍 Explainability payload
    factor_contributions: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
