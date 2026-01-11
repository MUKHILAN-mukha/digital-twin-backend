from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from app.db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)

    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    area: Mapped[str] = mapped_column(
        Enum("attendance", "academics", "behavior", name="recommendation_area"),
        nullable=False,
    )

    suggestion: Mapped[str] = mapped_column(Text, nullable=False)

    priority: Mapped[str] = mapped_column(
        Enum("HIGH", "MEDIUM", "LOW", name="recommendation_priority"),
        nullable=False,
    )

    acknowledged: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
