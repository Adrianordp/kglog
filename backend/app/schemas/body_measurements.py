"""
Schemas for body measurements in app.models.body_measurements.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BodyMeasurementBase(BaseModel):
    """
    Base schema for body measurements.
    """

    measure_date: datetime = Field(
        ..., description="Date of measurement in YYYY-MM-DDTHH:MM:SS format"
    )
    height: float = Field(..., description="Height in centimeters", gt=0)
    neck: float = Field(
        ..., description="Neck widest circumference in centimeters", gt=0
    )
    neck_to_shoulder: float = Field(
        ..., description="Neck to shoulder length in centimeters", gt=0
    )
    sleeve: float = Field(..., description="Sleeve length in centimeters", gt=0)
    bust: float = Field(
        ..., description="Bust widest circumference in centimeters", gt=0
    )
    left_arm: float = Field(
        ..., description="Left arm widest circumference in centimeters", gt=0
    )
    right_arm: float = Field(
        ..., description="Right arm widest circumference in centimeters", gt=0
    )
    waist: float = Field(
        ..., description="Waist narrowest circumference in centimeters", gt=0
    )
    hip: float = Field(
        ..., description="Hip widest circumference in centimeters", gt=0
    )
    inseam_to_ankle: float = Field(
        ..., description="Inseam to ankle length in centimeters", gt=0
    )
    left_leg: float = Field(
        ..., description="Left leg widest circumference in centimeters", gt=0
    )
    right_leg: float = Field(
        ..., description="Right leg widest circumference in centimeters", gt=0
    )
    left_calf: float = Field(
        ..., description="Left calf widest circumference in centimeters", gt=0
    )
    right_calf: float = Field(
        ..., description="Right calf widest circumference in centimeters", gt=0
    )


class BodyMeasurementCreate(BodyMeasurementBase):
    """
    Schema for creating a new body measurement.
    """

    model_config = {
        "json_schema_extra": {
            "example": {
                "measure_date": "2024-01-01T00:00:00",
                "height": 175.0,
                "neck": 40.0,
                "neck_to_shoulder": 15.0,
                "sleeve": 60.0,
                "bust": 100.0,
                "left_arm": 35.0,
                "right_arm": 35.0,
                "waist": 80.0,
                "hip": 95.0,
                "inseam_to_ankle": 80.0,
                "left_leg": 50.0,
                "right_leg": 50.0,
                "left_calf": 35.0,
                "right_calf": 35.0,
            }
        }
    }


class BodyMeasurementUpdate(BodyMeasurementBase):
    """
    Schema for updating an existing body measurement.
    """

    measure_date: Optional[datetime] = Field(
        None, description="Date of measurement in YYYY-MM-DDTHH:MM:SS format"
    )
    height: Optional[float] = Field(
        None, description="Height in centimeters", gt=0
    )
    neck: Optional[float] = Field(
        None, description="Neck widest circumference in centimeters", gt=0
    )
    neck_to_shoulder: Optional[float] = Field(
        None, description="Neck to shoulder length in centimeters", gt=0
    )
    sleeve: Optional[float] = Field(
        None, description="Sleeve length in centimeters", gt=0
    )
    bust: Optional[float] = Field(
        None, description="Bust widest circumference in centimeters", gt=0
    )
    left_arm: Optional[float] = Field(
        None, description="Left arm widest circumference in centimeters", gt=0
    )
    right_arm: Optional[float] = Field(
        None, description="Right arm widest circumference in centimeters", gt=0
    )
    waist: Optional[float] = Field(
        None, description="Waist narrowest circumference in centimeters", gt=0
    )
    hip: Optional[float] = Field(
        None, description="Hip widest circumference in centimeters", gt=0
    )
    inseam_to_ankle: Optional[float] = Field(
        None, description="Inseam to ankle length in centimeters", gt=0
    )
    left_leg: Optional[float] = Field(
        None, description="Left leg widest circumference in centimeters", gt=0
    )
    right_leg: Optional[float] = Field(
        None, description="Right leg widest circumference in centimeters", gt=0
    )
    left_calf: Optional[float] = Field(
        None, description="Left calf widest circumference in centimeters", gt=0
    )
    right_calf: Optional[float] = Field(
        None, description="Right calf widest circumference in centimeters", gt=0
    )


class BodyMeasurementRead(BodyMeasurementBase):
    """
    Schema for reading a body measurement.
    """

    id: int = Field(
        ..., description="Unique identifier of the body measurement"
    )
    id_user: int = Field(
        ...,
        description="Identifier of the user to whom the measurement belongs",
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "id_user": 1,
                "measure_date": "2024-01-01T00:00:00",
                "height": 175.0,
                "neck": 40.0,
                "neck_to_shoulder": 15.0,
                "sleeve": 60.0,
                "bust": 100.0,
                "left_arm": 35.0,
                "right_arm": 35.0,
                "waist": 80.0,
                "hip": 95.0,
                "inseam_to_ankle": 80.0,
                "left_leg": 50.0,
                "right_leg": 50.0,
                "left_calf": 35.0,
                "right_calf": 35.0,
            }
        },
    }
