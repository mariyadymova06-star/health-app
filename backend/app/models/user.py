from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.measurement import Measurement
    from app.models.goal import Goal


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    profile: Mapped[Profile | None] = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    measurements: Mapped[list[Measurement]] = relationship(
        "Measurement", back_populates="user", cascade="all, delete-orphan"
    )
    goals: Mapped[list[Goal]] = relationship(
        "Goal", back_populates="user", cascade="all, delete-orphan"
    )
