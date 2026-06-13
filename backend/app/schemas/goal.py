from datetime import date, datetime
from pydantic import BaseModel
from app.schemas.measurement import MeasurementTypeOut


class GoalIn(BaseModel):
    type_id: int
    target_value: float
    start_value: float | None = None
    start_date: date
    end_date: date
    notes: str | None = None


class GoalUpdate(BaseModel):
    target_value: float | None = None
    end_date: date | None = None
    notes: str | None = None
    is_active: bool | None = None


class GoalOut(BaseModel):
    id: int
    type_id: int
    target_value: float
    start_value: float | None
    start_date: date
    end_date: date
    notes: str | None
    is_active: bool
    created_at: datetime
    type: MeasurementTypeOut
    progress: float | None = None

    model_config = {"from_attributes": True}
