import uuid
import enum
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReviewerRole(str, enum.Enum):
    student = "student"
    parent = "parent"
    admin = "admin"


class InsightReview(Base):
    __tablename__ = "insight_reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    reviewer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    reviewer_role: Mapped[ReviewerRole] = mapped_column(
        SAEnum(ReviewerRole, name="reviewer_role_enum"),
        nullable=False,
    )

    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        # 🔒 Prevent duplicate acknowledgments
        UniqueConstraint(
            "child_id",
            "reviewer_id",
            name="uq_insight_ack_once",
        ),
    )
