"""
This model represents a user, including:

- username
- email
- password hash
- date of birth
- gender
- created at
- updated at

This model is used to store and manage user information
"""

from datetime import date, datetime
from enum import Enum as PyEnum
from zoneinfo import ZoneInfo

from sqlalchemy import Date, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.body_composition import BodyComposition
from app.models.body_measurements import BodyMeasurements


class Gender(PyEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[Gender] = mapped_column(Enum(Gender))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=lambda: datetime.now(ZoneInfo("America/Manaus")),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=lambda: datetime.now(ZoneInfo("America/Manaus")),
        onupdate=lambda: datetime.now(ZoneInfo("America/Manaus")),
    )

    body_compositions: Mapped[list["BodyComposition"]] = relationship(
        "BodyComposition", back_populates="user", cascade="all, delete-orphan"
    )
    body_measurements: Mapped[list["BodyMeasurements"]] = relationship(
        "BodyMeasurements", back_populates="user", cascade="all, delete-orphan"
    )
