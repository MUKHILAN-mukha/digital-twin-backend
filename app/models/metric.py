import uuid
from sqlalchemy import Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class StudentMetric(Base):
    __tablename__ = "student_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    metric_name: Mapped[str] = mapped_column(String(50))  # avg_score, attendance_rate
    value: Mapped[float] = mapped_column(Float)
