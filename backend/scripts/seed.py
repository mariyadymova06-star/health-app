import asyncio
import random
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt

from app.core.config import settings
from app.models.user import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
from app.models.profile import Profile, GenderEnum
from app.models.measurement_type import MeasurementType
from app.models.measurement import Measurement
from app.models.goal import Goal

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 6, 14)

USERS = [
    {
        "email": "anna@example.com",
        "password": "password123",
        "profile": {
            "name": "Анна Иванова",
            "gender": GenderEnum.female,
            "birth_date": date(1997, 3, 15),
            "height_cm": 165.0,
        },
        "metrics": {
            "weight":         {"base": 72.0,  "trend": -0.05, "std": 0.3,  "freq": 0.7},
            "blood_pressure": {"base": 118.0, "trend": -0.02, "std": 5.0,  "freq": 0.8, "base2": 76.0, "std2": 3.0},
            "heart_rate":     {"base": 72.0,  "trend":  0.0,  "std": 4.0,  "freq": 0.9},
            "sleep":          {"base": 7.2,   "trend":  0.0,  "std": 0.8,  "freq": 0.9},
            "steps":          {"base": 8500,  "trend":  20.0, "std": 2000, "freq": 0.85},
            "blood_glucose":  {"base": 5.1,   "trend":  0.0,  "std": 0.3,  "freq": 0.5},
            "spo2":           {"base": 98.0,  "trend":  0.0,  "std": 0.5,  "freq": 0.4},
            "temperature":    {"base": 36.6,  "trend":  0.0,  "std": 0.15, "freq": 0.35},
        },
        "goals": [
            {"type_key": "weight",      "start_value": 72.0, "target_value": 65.0, "end_date": date(2026, 9, 1)},
            {"type_key": "steps",       "start_value": 8500, "target_value": 12000,"end_date": date(2026, 7, 1)},
            {"type_key": "blood_pressure","start_value": 118, "target_value": 110, "end_date": date(2026, 8, 1)},
        ],
    },
    {
        "email": "mikhail@example.com",
        "password": "password123",
        "profile": {
            "name": "Михаил Петров",
            "gender": GenderEnum.male,
            "birth_date": date(1990, 7, 22),
            "height_cm": 182.0,
        },
        "metrics": {
            "weight":         {"base": 88.0,  "trend": -0.03, "std": 0.4,  "freq": 0.65},
            "blood_pressure": {"base": 128.0, "trend": -0.03, "std": 6.0,  "freq": 0.75, "base2": 84.0, "std2": 4.0},
            "heart_rate":     {"base": 65.0,  "trend":  0.0,  "std": 5.0,  "freq": 0.85},
            "sleep":          {"base": 6.8,   "trend":  0.0,  "std": 1.0,  "freq": 0.85},
            "steps":          {"base": 11000, "trend":  15.0, "std": 2500, "freq": 0.8},
            "blood_glucose":  {"base": 5.5,   "trend":  0.0,  "std": 0.4,  "freq": 0.45},
            "spo2":           {"base": 97.5,  "trend":  0.0,  "std": 0.5,  "freq": 0.4},
            "temperature":    {"base": 36.7,  "trend":  0.0,  "std": 0.15, "freq": 0.3},
        },
        "goals": [
            {"type_key": "weight",      "start_value": 88.0, "target_value": 82.0, "end_date": date(2026, 10, 1)},
            {"type_key": "heart_rate",  "start_value": 65.0, "target_value": 58.0, "end_date": date(2026, 8, 15)},
            {"type_key": "sleep",       "start_value": 6.8,  "target_value": 8.0,  "end_date": date(2026, 7, 31)},
        ],
    },
    {
        "email": "elena@example.com",
        "password": "password123",
        "profile": {
            "name": "Елена Сидорова",
            "gender": GenderEnum.female,
            "birth_date": date(1979, 11, 5),
            "height_cm": 162.0,
        },
        "metrics": {
            "weight":         {"base": 68.0,  "trend":  0.01, "std": 0.3,  "freq": 0.6},
            "blood_pressure": {"base": 135.0, "trend": -0.04, "std": 7.0,  "freq": 0.85, "base2": 88.0, "std2": 5.0},
            "heart_rate":     {"base": 78.0,  "trend": -0.01, "std": 5.0,  "freq": 0.9},
            "sleep":          {"base": 6.5,   "trend":  0.01, "std": 0.9,  "freq": 0.88},
            "steps":          {"base": 6500,  "trend":  10.0, "std": 1500, "freq": 0.8},
            "blood_glucose":  {"base": 5.8,   "trend":  0.0,  "std": 0.5,  "freq": 0.7},
            "spo2":           {"base": 97.0,  "trend":  0.0,  "std": 0.6,  "freq": 0.5},
            "temperature":    {"base": 36.5,  "trend":  0.0,  "std": 0.2,  "freq": 0.4},
        },
        "goals": [
            {"type_key": "blood_pressure","start_value": 135, "target_value": 120, "end_date": date(2026, 9, 15)},
            {"type_key": "steps",         "start_value": 6500,"target_value": 9000,"end_date": date(2026, 8, 1)},
            {"type_key": "blood_glucose", "start_value": 5.8, "target_value": 5.2, "end_date": date(2026, 9, 1)},
        ],
    },
]


def generate_value(day_index: int, cfg: dict) -> float:
    value = cfg["base"] + cfg["trend"] * day_index + random.gauss(0, cfg["std"])
    return round(max(value, 1), 2)


async def seed():
    async with AsyncSessionLocal() as db:
        type_result = await db.execute(select(MeasurementType))
        types_by_key = {t.key: t for t in type_result.scalars().all()}

        for user_data in USERS:
            existing = await db.execute(select(User).where(User.email == user_data["email"]))
            if existing.scalar_one_or_none():
                print(f"  Пропуск {user_data['email']} — уже существует")
                continue

            user = User(
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                created_at=datetime.now(timezone.utc),
            )
            db.add(user)
            await db.flush()

            p = user_data["profile"]
            profile = Profile(
                user_id=user.id,
                name=p["name"],
                gender=p["gender"],
                birth_date=p["birth_date"],
                height_cm=p["height_cm"],
                updated_at=datetime.now(timezone.utc),
            )
            db.add(profile)

            days = (END_DATE - START_DATE).days + 1
            for day_index in range(days):
                current_date = START_DATE + timedelta(days=day_index)
                hour = random.randint(7, 21)
                minute = random.randint(0, 59)
                measured_at = datetime(
                    current_date.year, current_date.month, current_date.day,
                    hour, minute, tzinfo=timezone.utc
                )

                for type_key, cfg in user_data["metrics"].items():
                    if random.random() > cfg["freq"]:
                        continue

                    mtype = types_by_key.get(type_key)
                    if not mtype:
                        continue

                    value = generate_value(day_index, cfg)
                    secondary = None
                    if mtype.has_secondary and "base2" in cfg:
                        secondary = round(
                            cfg["base2"] + cfg["trend"] * day_index + random.gauss(0, cfg["std2"]),
                            2
                        )

                    db.add(Measurement(
                        user_id=user.id,
                        type_id=mtype.id,
                        value=value,
                        secondary_value=secondary,
                        measured_at=measured_at,
                        created_at=datetime.now(timezone.utc),
                    ))

            for g in user_data["goals"]:
                mtype = types_by_key.get(g["type_key"])
                if not mtype:
                    continue
                db.add(Goal(
                    user_id=user.id,
                    type_id=mtype.id,
                    start_value=g["start_value"],
                    target_value=g["target_value"],
                    start_date=START_DATE,
                    end_date=g["end_date"],
                    is_active=True,
                    created_at=datetime.now(timezone.utc),
                ))

            await db.commit()
            print(f"  Создан пользователь: {p['name']} ({user_data['email']})")

    print("\nSeeder завершён.")
    print("Логины: anna@example.com / mikhail@example.com / elena@example.com")
    print("Пароль для всех: password123")

if __name__ == "__main__":
    asyncio.run(seed())
