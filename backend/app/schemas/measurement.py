from datetime import datetime
from pydantic import BaseModel


class MeasurementTypeOut(BaseModel):
    id: int
    key: str
    name: str
    unit: str
    has_secondary: bool
    secondary_unit: str | None
    category: str
    icon: str | None

    model_config = {"from_attributes": True}


class MeasurementIn(BaseModel):
    type_id: int
    value: float
    secondary_value: float | None = None
    measured_at: datetime
    notes: str | None = None


class MeasurementOut(BaseModel):
    id: int
    type_id: int
    value: float
    secondary_value: float | None
    measured_at: datetime
    notes: str | None
    created_at: datetime
    type: MeasurementTypeOut

    model_config = {"from_attributes": True}
