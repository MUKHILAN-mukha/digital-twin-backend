from sqlalchemy import Integer, JSON, Text, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class HistoricalStudent(Base):
    __tablename__ = "historical_students"

    id: Mapped[int] = mapped_column(primary_key=True)
    feature_vector: Mapped[dict] = mapped_column(JSON, nullable=False)
    actions_taken: Mapped[str] = mapped_column(Text, nullable=False)
    outcome: Mapped[str] = mapped_column(
        Enum("Improved", "Average", "Failed", name="outcome_enum"),
        nullable=False,
    )
    final_gpa: Mapped[float] = mapped_column(Float)
