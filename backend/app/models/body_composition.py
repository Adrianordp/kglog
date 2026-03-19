"""
This model represents the body composition of a user, including:

- date of measurement
- weight [kg]
- body fat [%]
- body fat [kg]
- muscle [%]
- muscle [kg]
- bone [%]
- bone [kg]
- water [%]
- water [kg]
- visceral fat [cm2]

This model is used to track the user's body composition over time, which can be
useful for tracking fitness and health progress.
"""

from datetime import date

from sqlalchemy import Date, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class BodyComposition(Base):
    __tablename__ = "body_compositions"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    measure_date: Mapped[date] = mapped_column(Date)
    weight: Mapped[float] = mapped_column(Float)
    fat_percentage: Mapped[float] = mapped_column(Float)
    fat_kg: Mapped[float] = mapped_column(Float)
    muscle_percentage: Mapped[float] = mapped_column(Float)
    muscle_kg: Mapped[float] = mapped_column(Float)
    bone_percentage: Mapped[float] = mapped_column(Float)
    bone_kg: Mapped[float] = mapped_column(Float)
    water_percentage: Mapped[float] = mapped_column(Float)
    water_kg: Mapped[float] = mapped_column(Float)
    visceral_fat_level: Mapped[float] = mapped_column(Float)
