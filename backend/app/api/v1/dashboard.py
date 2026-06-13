from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.measurement import Measurement
from app.models.measurement_type import MeasurementType
from app.models.profile import Profile
from app.schemas.dashboard import DashboardSummary, MetricSummary, ChartData, ChartPoint

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    types_result = await db.execute(select(MeasurementType))
    all_types = types_result.scalars().all()

    metrics = []
    weight_value = None

    for mtype in all_types:
        result = await db.execute(
            select(Measurement)
            .where(
                Measurement.user_id == current_user.id,
                Measurement.type_id == mtype.id,
            )
            .order_by(Measurement.measured_at.desc())
            .limit(1)
        )
        measurement = result.scalar_one_or_none()
        if measurement:
            if mtype.key == "weight":
                weight_value = measurement.value
            metrics.append(
                MetricSummary(
                    type_key=mtype.key,
                    name=mtype.name,
                    unit=mtype.unit,
                    value=measurement.value,
                    secondary_value=measurement.secondary_value,
                    measured_at=measurement.measured_at,
                )
            )

    bmi = None
    if weight_value is not None:
        profile_result = await db.execute(
            select(Profile).where(Profile.user_id == current_user.id)
        )
        profile = profile_result.scalar_one_or_none()
        if profile and profile.height_cm:
            height_m = profile.height_cm / 100
            bmi = round(weight_value / (height_m ** 2), 1)

    return DashboardSummary(metrics=metrics, bmi=bmi)


@router.get("/chart/{type_key}", response_model=ChartData)
async def get_chart(
    type_key: str,
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    type_result = await db.execute(
        select(MeasurementType).where(MeasurementType.key == type_key)
    )
    mtype = type_result.scalar_one_or_none()
    if not mtype:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement type not found")

    since = datetime.now(timezone.utc) - timedelta(days=days)
    result = await db.execute(
        select(Measurement)
        .where(
            Measurement.user_id == current_user.id,
            Measurement.type_id == mtype.id,
            Measurement.measured_at >= since,
        )
        .order_by(Measurement.measured_at.asc())
    )
    measurements = result.scalars().all()

    return ChartData(
        type_key=mtype.key,
        name=mtype.name,
        unit=mtype.unit,
        points=[
            ChartPoint(
                measured_at=m.measured_at,
                value=m.value,
                secondary_value=m.secondary_value,
            )
            for m in measurements
        ],
    )
