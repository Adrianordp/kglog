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
    height: float = Field(..., description="Height in centimeters")
    neck: float = Field(
        ..., description="Neck widest circumference in centimeters"
    )
    neck_to_shoulder: float = Field(
        ..., description="Neck to shoulder length in centimeters"
    )
    sleeve: float = Field(..., description="Sleeve length in centimeters")
    bust: float = Field(
        ..., description="Bust widest circumference in centimeters"
    )
    left_arm: float = Field(
        ..., description="Left arm widest circumference in centimeters"
    )
    right_arm: float = Field(
        ..., description="Right arm widest circumference in centimeters"
    )
    waist: float = Field(
        ..., description="Waist narrowest circumference in centimeters"
    )
    hip: float = Field(
        ..., description="Hip widest circumference in centimeters"
    )
    inseam_to_ankle: float = Field(
        ..., description="Inseam to ankle length in centimeters"
    )
    left_leg: float = Field(
        ..., description="Left leg widest circumference in centimeters"
    )
    right_leg: float = Field(
        ..., description="Right leg widest circumference in centimeters"
    )
    left_calf: float = Field(
        ..., description="Left calf widest circumference in centimeters"
    )
    right_calf: float = Field(
        ..., description="Right calf widest circumference in centimeters"
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

    measure_date: Optional[datetime] = None
    height: Optional[float] = None
    neck: Optional[float] = None
    neck_to_shoulder: Optional[float] = None
    sleeve: Optional[float] = None
    bust: Optional[float] = None
    left_arm: Optional[float] = None
    right_arm: Optional[float] = None
    waist: Optional[float] = None
    hip: Optional[float] = None
    inseam_to_ankle: Optional[float] = None
    left_leg: Optional[float] = None
    right_leg: Optional[float] = None
    left_calf: Optional[float] = None
    right_calf: Optional[float] = None


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
