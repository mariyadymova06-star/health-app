from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.measurement import Measurement
    from app.models.goal import Goal


class MeasurementType(Base):
    __tablename__ = "measurement_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    has_secondary: Mapped[bool] = mapped_column(Boolean, default=False)
    secondary_unit: Mapped[str | None] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(50), default="general")
    icon: Mapped[str | None] = mapped_column(String(50))

    measurements: Mapped[list[Measurement]] = relationship(
        "Measurement", back_populates="type"
    )
    goals: Mapped[list[Goal]] = relationship("Goal", back_populates="type")
