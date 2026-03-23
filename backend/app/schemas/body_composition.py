"""
Schemas for body composition in app.models.body_composition.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BodyCompositionBase(BaseModel):
    """
    Base schema for body composition.
    """

    measure_date: datetime = Field(
        ..., description="Date of measurement in YYYY-MM-DDTHH:MM:SS format"
    )
    weight: float = Field(..., description="Weight in kilograms", gt=0.0)
    is_fat_estimated: Optional[bool] = Field(
        True,
        description="Indicates if the fat percentage is estimated (true) or measured (false)",
    )
    is_muscle_estimated: Optional[bool] = Field(
        True,
        description="Indicates if the muscle percentage is estimated (true) or measured (false)",
    )
    is_bone_estimated: Optional[bool] = Field(
        True,
        description="Indicates if the bone percentage is estimated (true) or measured (false)",
    )
    is_water_estimated: Optional[bool] = Field(
        True,
        description="Indicates if the water percentage is estimated (true) or measured (false)",
    )
    is_visceral_fat_estimated: Optional[bool] = Field(
        True,
        description="Indicates if the visceral fat level is estimated (true) or measured (false)",
    )


class BodyCompositionCreate(BodyCompositionBase):
    """
    Schema for creating a new body composition record.
    """

    fat_percentage: Optional[float] = Field(
        ...,
        description="Body fat percentage as a decimal (e.g., 0.15 for 15%)",
        gt=0.0,
        lt=1.0,
    )
    muscle_percentage: Optional[float] = Field(
        ...,
        description="Muscle mass percentage as a decimal (e.g., 0.40 for 40%)",
        gt=0.0,
        lt=1.0,
    )
    bone_percentage: Optional[float] = Field(
        ...,
        description="Bone mass percentage as a decimal (e.g., 0.05 for 5%)",
        gt=0.0,
        lt=1.0,
    )
    water_percentage: Optional[float] = Field(
        ...,
        description="Water percentage as a decimal (e.g., 0.60 for 60%)",
        gt=0.0,
        lt=1.0,
    )
    visceral_fat: Optional[float] = Field(
        None,
        description="Visceral fat level in cm² (calculated based on weight and fat percentage)",
        ge=0.0,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "measure_date": "2024-01-01T08:00:00",
                "weight": 70.0,
                "fat_percentage": 0.15,
                "muscle_percentage": 0.40,
                "bone_percentage": 0.05,
                "water_percentage": 0.60,
                "visceral_fat": 100.0,
                "is_fat_estimated": True,
                "is_muscle_estimated": True,
                "is_bone_estimated": True,
                "is_water_estimated": True,
                "is_visceral_fat_estimated": True,
            }
        }
    }


class BodyCompositionUpdate(BaseModel):
    """
    Schema for updating an existing body composition record.
    """

    measure_date: Optional[datetime] = Field(
        None, description="Date of measurement in YYYY-MM-DDTHH:MM:SS format"
    )
    weight: Optional[float] = Field(
        None, description="Weight in kilograms", gt=0.0
    )
    fat_percentage: Optional[float] = Field(
        None,
        description="Body fat percentage as a decimal (e.g., 0.15 for 15%)",
        gt=0.0,
        lt=1.0,
    )
    muscle_percentage: Optional[float] = Field(
        None,
        description="Muscle mass percentage as a decimal (e.g., 0.40 for 40%)",
        gt=0.0,
        lt=1.0,
    )
    bone_percentage: Optional[float] = Field(
        None,
        description="Bone mass percentage as a decimal (e.g., 0.05 for 5%)",
        gt=0.0,
        lt=1.0,
    )
    water_percentage: Optional[float] = Field(
        None,
        description="Water percentage as a decimal (e.g., 0.60 for 60%)",
        gt=0.0,
        lt=1.0,
    )
    visceral_fat: Optional[float] = Field(
        None,
        description="Visceral fat level in cm² (calculated based on weight and fat percentage)",
        ge=0.0,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "measure_date": "2024-01-01T08:00:00",
                "weight": 70.0,
                "fat_percentage": 0.15,
                "muscle_percentage": 0.40,
                "bone_percentage": 0.05,
                "water_percentage": 0.60,
                "visceral_fat": 100.0,
                "is_fat_estimated": True,
                "is_muscle_estimated": True,
                "is_bone_estimated": True,
                "is_water_estimated": True,
                "is_visceral_fat_estimated": True,
            }
        }
    }


class BodyCompositionRead(BodyCompositionBase):
    """
    Schema for reading a body composition record.
    """

    id: int = Field(
        ..., description="Unique identifier for the body composition record"
    )
    id_user: int = Field(
        ...,
        description="Identifier of the user to whom the body composition record belongs",
    )
    fat_percentage: float = Field(
        ...,
        description="Body fat percentage as a decimal (e.g., 0.15 for 15%)",
    )
    fat_kg: float = Field(
        ...,
        description="Calculated fat mass in kilograms (weight * fat_percentage)",
    )
    muscle_percentage: float = Field(
        ...,
        description="Muscle mass percentage as a decimal (e.g., 0.40 for 40%)",
    )
    muscle_kg: float = Field(
        ...,
        description="Calculated muscle mass in kilograms (weight * muscle_percentage)",
    )
    bone_percentage: float = Field(
        ...,
        description="Bone mass percentage as a decimal (e.g., 0.05 for 5%)",
    )
    bone_kg: float = Field(
        ...,
        description="Calculated bone mass in kilograms (weight * bone_percentage)",
    )
    water_percentage: float = Field(
        ...,
        description="Water percentage as a decimal (e.g., 0.60 for 60%)",
    )
    water_kg: float = Field(
        ...,
        description="Calculated water mass in kilograms (weight * water_percentage)",
    )
    visceral_fat: float = Field(
        ...,
        description="Visceral fat level in cm² (calculated based on weight and fat percentage)",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "id_user": 1,
                "measure_date": "2024-01-01T08:00:00",
                "weight": 70.0,
                "fat_percentage": 0.15,
                "fat_kg": 10.5,
                "muscle_percentage": 0.40,
                "muscle_kg": 28.0,
                "bone_percentage": 0.05,
                "bone_kg": 3.5,
                "water_percentage": 0.60,
                "water_kg": 42.0,
                "visceral_fat": 100.0,
                "is_fat_estimated": True,
                "is_muscle_estimated": True,
                "is_bone_estimated": True,
                "is_water_estimated": True,
                "is_visceral_fat_estimated": True,
            }
        }
    }
