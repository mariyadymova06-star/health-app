from __future__ import annotations
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import Float, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.measurement_type import MeasurementType


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("measurement_types.id"), nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    start_value: Mapped[float | None] = mapped_column(Float)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped[User] = relationship("User", back_populates="goals")
    type: Mapped[MeasurementType] = relationship("MeasurementType", back_populates="goals")
