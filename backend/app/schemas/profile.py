from datetime import date, datetime
from pydantic import BaseModel
from app.models.profile import GenderEnum


class ProfileOut(BaseModel):
    id: int
    user_id: int
    name: str | None
    gender: GenderEnum | None
    birth_date: date | None
    height_cm: float | None
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    name: str | None = None
    gender: GenderEnum | None = None
    birth_date: date | None = None
    height_cm: float | None = None
