"""
This model represents the body measurements of a user, including:

- date of measurement
- height
- neck circumference
- neck to shoulder length
- sleeve length
- bust circumference (widest point)
- left arm circumference (widest point)
- right arm circumference (widest point)
- waist circumference (narrowest point)
- hip circumference (widest point)
- inseam to ankle length
- left leg circumference (widest point)
- right leg circumference (widest point)
- left_calf circumference (widest point)
- right_calf circumference (widest point)

This model is used to track the user's body measurements over time, which can be
useful for tracking fitness and health progress.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class BodyMeasurements(Base):
    __tablename__ = "body_measurements"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

    measure_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    height: Mapped[float] = mapped_column(Float)
    neck: Mapped[float] = mapped_column(Float)
    neck_to_shoulder: Mapped[float] = mapped_column(Float)
    sleeve: Mapped[float] = mapped_column(Float)
    bust: Mapped[float] = mapped_column(Float)
    left_arm: Mapped[float] = mapped_column(Float)
    right_arm: Mapped[float] = mapped_column(Float)
    waist: Mapped[float] = mapped_column(Float)
    hip: Mapped[float] = mapped_column(Float)
    inseam_to_ankle: Mapped[float] = mapped_column(Float)
    left_leg: Mapped[float] = mapped_column(Float)
    right_leg: Mapped[float] = mapped_column(Float)
    left_calf: Mapped[float] = mapped_column(Float)
    right_calf: Mapped[float] = mapped_column(Float)
