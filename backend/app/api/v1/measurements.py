from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.measurement import Measurement
from app.models.measurement_type import MeasurementType
from app.schemas.measurement import MeasurementIn, MeasurementOut, MeasurementTypeOut

router = APIRouter(tags=["measurements"])


@router.get("/measurement-types", response_model=list[MeasurementTypeOut])
async def get_measurement_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MeasurementType).order_by(MeasurementType.id))
    return result.scalars().all()


@router.get("/measurements", response_model=list[MeasurementOut])
async def get_measurements(
    type_key: str | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    limit: int = Query(100, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Measurement)
        .options(selectinload(Measurement.type))
        .where(Measurement.user_id == current_user.id)
    )

    if type_key:
        query = query.join(MeasurementType).where(MeasurementType.key == type_key)
    if date_from:
        query = query.where(Measurement.measured_at >= date_from)
    if date_to:
        query = query.where(Measurement.measured_at <= date_to)

    query = query.order_by(Measurement.measured_at.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/measurements", response_model=MeasurementOut, status_code=status.HTTP_201_CREATED)
async def create_measurement(
    data: MeasurementIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    type_exists = await db.execute(
        select(MeasurementType).where(MeasurementType.id == data.type_id)
    )
    if not type_exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement type not found")

    measurement = Measurement(
        user_id=current_user.id,
        **data.model_dump(),
    )
    db.add(measurement)
    await db.commit()

    result = await db.execute(
        select(Measurement)
        .options(selectinload(Measurement.type))
        .where(Measurement.id == measurement.id)
    )
    return result.scalar_one()


@router.delete("/measurements/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement(
    measurement_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Measurement).where(
            Measurement.id == measurement_id,
            Measurement.user_id == current_user.id,
        )
    )
    measurement = result.scalar_one_or_none()
    if not measurement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement not found")

    await db.delete(measurement)
    await db.commit()
