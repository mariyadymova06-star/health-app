"""init: create tables and seed measurement types

Revision ID: 0001
Revises:
Create Date: 2026-06-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "measurement_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("unit", sa.String(20), nullable=False),
        sa.Column("has_secondary", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("secondary_unit", sa.String(20), nullable=True),
        sa.Column("category", sa.String(50), nullable=False, server_default="general"),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )

    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("gender", sa.Enum("male", "female", "other", name="genderenum"), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("secondary_value", sa.Float(), nullable=True),
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["type_id"], ["measurement_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_measurements_user_id", "measurements", ["user_id"])

    op.create_table(
        "goals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("target_value", sa.Float(), nullable=False),
        sa.Column("start_value", sa.Float(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["type_id"], ["measurement_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_goals_user_id", "goals", ["user_id"])

    op.bulk_insert(
        sa.table(
            "measurement_types",
            sa.column("key", sa.String),
            sa.column("name", sa.String),
            sa.column("unit", sa.String),
            sa.column("has_secondary", sa.Boolean),
            sa.column("secondary_unit", sa.String),
            sa.column("category", sa.String),
            sa.column("icon", sa.String),
        ),
        [
            {"key": "weight", "name": "Вес", "unit": "кг", "has_secondary": False, "secondary_unit": None, "category": "body", "icon": "weight-scale"},
            {"key": "blood_pressure", "name": "Давление", "unit": "мм рт. ст.", "has_secondary": True, "secondary_unit": "мм рт. ст.", "category": "cardiovascular", "icon": "heart-pulse"},
            {"key": "heart_rate", "name": "Пульс", "unit": "уд/мин", "has_secondary": False, "secondary_unit": None, "category": "cardiovascular", "icon": "activity"},
            {"key": "sleep", "name": "Сон", "unit": "ч", "has_secondary": False, "secondary_unit": None, "category": "lifestyle", "icon": "moon"},
            {"key": "steps", "name": "Шаги", "unit": "шт", "has_secondary": False, "secondary_unit": None, "category": "lifestyle", "icon": "footprints"},
            {"key": "temperature", "name": "Температура", "unit": "°C", "has_secondary": False, "secondary_unit": None, "category": "general", "icon": "thermometer"},
            {"key": "blood_glucose", "name": "Сахар крови", "unit": "ммоль/л", "has_secondary": False, "secondary_unit": None, "category": "general", "icon": "droplet"},
            {"key": "spo2", "name": "SpO2", "unit": "%", "has_secondary": False, "secondary_unit": None, "category": "cardiovascular", "icon": "lungs"},
        ],
    )


def downgrade() -> None:
    op.drop_table("goals")
    op.drop_table("measurements")
    op.drop_table("profiles")
    op.drop_table("measurement_types")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS genderenum")
