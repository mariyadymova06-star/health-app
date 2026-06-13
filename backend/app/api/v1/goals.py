from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.goal import Goal
from app.models.measurement import Measurement
from app.models.measurement_type import MeasurementType
from app.schemas.goal import GoalIn, GoalOut, GoalUpdate

router = APIRouter(prefix="/goals", tags=["goals"])


async def _attach_progress(goal: Goal, db: AsyncSession) -> GoalOut:
    result = await db.execute(
        select(Measurement.value)
        .where(
            Measurement.user_id == goal.user_id,
            Measurement.type_id == goal.type_id,
        )
        .order_by(Measurement.measured_at.desc())
        .limit(1)
    )
    latest = result.scalar_one_or_none()

    progress = None
    if latest is not None and goal.start_value is not None:
        span = goal.target_value - goal.start_value
        if span != 0:
            progress = round((latest - goal.start_value) / span * 100, 1)

    out = GoalOut.model_validate(goal)
    out.progress = progress
    return out


@router.get("", response_model=list[GoalOut])
async def get_goals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Goal)
        .options(selectinload(Goal.type))
        .where(Goal.user_id == current_user.id)
        .order_by(Goal.created_at.desc())
    )
    goals = result.scalars().all()
    return [await _attach_progress(g, db) for g in goals]


@router.post("", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
async def create_goal(
    data: GoalIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    type_exists = await db.execute(
        select(MeasurementType).where(MeasurementType.id == data.type_id)
    )
    if not type_exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Measurement type not found")

    goal = Goal(user_id=current_user.id, **data.model_dump())
    db.add(goal)
    await db.commit()

    result = await db.execute(
        select(Goal).options(selectinload(Goal.type)).where(Goal.id == goal.id)
    )
    goal = result.scalar_one()
    return await _attach_progress(goal, db)


@router.patch("/{goal_id}", response_model=GoalOut)
async def update_goal(
    goal_id: int,
    data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Goal)
        .options(selectinload(Goal.type))
        .where(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(goal, field, value)

    await db.commit()
    await db.refresh(goal)
    return await _attach_progress(goal, db)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    await db.delete(goal)
    await db.commit()
