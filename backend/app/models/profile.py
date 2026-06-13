from __future__ import annotations
import enum
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(100))
    gender: Mapped[GenderEnum | None] = mapped_column(Enum(GenderEnum))
    birth_date: Mapped[date | None] = mapped_column(Date)
    height_cm: Mapped[float | None] = mapped_column(Float)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped[User] = relationship("User", back_populates="profile")
