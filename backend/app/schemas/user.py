"""
Schemas for users in app.models.user.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import Gender


class UserBase(BaseModel):
    """
    Base schema for user.
    """

    username: str = Field(..., description="Unique username for the user")
    email: EmailStr = Field(
        ..., description="Unique email address for the user"
    )
    date_of_birth: date = Field(
        ..., description="Date of birth in YYYY-MM-DD format"
    )
    gender: Gender = Field(
        ..., description="Gender of the user (e.g., MALE, FEMALE, OTHER)"
    )


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """

    password: str = Field(
        ..., description="Password for the user", min_length=6
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "email": "john_doe@example.com",
                "date_of_birth": "1990-01-01",
                "gender": "MALE",
                "password": "securepassword123",
            }
        }
    }


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.
    """

    username: Optional[str] = Field(
        None, description="Unique username for the user"
    )
    email: Optional[EmailStr] = Field(
        None, description="Unique email address for the user"
    )
    date_of_birth: Optional[date] = Field(
        None, description="Date of birth in YYYY-MM-DD format"
    )
    gender: Optional[Gender] = Field(
        None, description="Gender of the user (e.g., MALE, FEMALE, OTHER)"
    )
    password: Optional[str] = Field(
        None, description="Password for the user", min_length=6
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe_updated",
                "email": "john_doe_updated@example.com",
                "date_of_birth": "1990-01-01",
                "gender": "MALE",
                "password": "newsecurepassword123",
            }
        }
    }


class UserRead(UserBase):
    """
    Schema for reading a user.
    """

    id: int = Field(..., description="Unique identifier of the user")
    created_at: datetime = Field(
        ..., description="Timestamp with timezone when the user was created"
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp with timezone when the user was last updated",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john_doe@example.com",
                "date_of_birth": "1990-01-01",
                "gender": "MALE",
                "created_at": "2023-01-01 00:00:00+00:00",
                "updated_at": "2023-01-01 00:00:00+00:00",
            }
        }
    }
