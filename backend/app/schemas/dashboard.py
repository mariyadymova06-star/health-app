from datetime import datetime
from pydantic import BaseModel


class MetricSummary(BaseModel):
    type_key: str
    name: str
    unit: str
    value: float
    secondary_value: float | None
    measured_at: datetime


class ChartPoint(BaseModel):
    measured_at: datetime
    value: float
    secondary_value: float | None


class DashboardSummary(BaseModel):
    metrics: list[MetricSummary]
    bmi: float | None


class ChartData(BaseModel):
    type_key: str
    name: str
    unit: str
    points: list[ChartPoint]
