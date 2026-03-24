from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.repositories.body_measurements import (
    create_body_measurement,
    get_body_measurement_by_id,
    get_body_measurements,
    update_body_measurement,
)
from app.schemas.body_measurements import (
    BodyMeasurementCreate,
    BodyMeasurementRead,
    BodyMeasurementUpdate,
)

router = APIRouter(prefix="/body_measurements", tags=["body_measurements"])


@router.post(
    "/",
    response_model=BodyMeasurementRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new body measurement",
    description="Create a new body measurement with the provided information.",
    response_description="Details of the created body measurement",
    responses={
        201: {"description": "Body measurement created successfully"},
        400: {"description": "Invalid input data"},
    },
)
async def create_body_measurement_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    body_measurement: BodyMeasurementCreate,
) -> BodyMeasurementRead:
    """
    Create a new body measurement with the provided information.
    """
    return await create_body_measurement(db, body_measurement)


@router.get(
    "/",
    response_model=List[BodyMeasurementRead],
    summary="Get all body measurements",
    description="Retrieve a list of all body measurements.",
    response_description="List of body measurements",
    responses={
        200: {
            "description": "List of body measurements retrieved successfully"
        },
    },
)
async def get_body_measurements_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> List[BodyMeasurementRead]:
    """
    Retrieve a list of all body measurements.
    """
    return await get_body_measurements(db)


@router.get(
    "/{id}",
    response_model=BodyMeasurementRead,
    summary="Get a body measurement by ID",
    description="Retrieve details of a body measurement by its unique ID.",
    response_description="Details of the body measurement",
    responses={
        200: {"description": "Body measurement retrieved successfully"},
        404: {"description": "Body measurement not found"},
    },
)
async def get_body_measurement_by_id_endpoint(
    id: int,
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> BodyMeasurementRead:
    """
    Retrieve details of a body measurement by its unique ID.
    """
    body_measurement = await get_body_measurement_by_id(db, id)

    if not body_measurement:
        raise HTTPException(
            status_code=404, detail="Body measurement not found"
        )

    return body_measurement


@router.put(
    "/{id}",
    response_model=BodyMeasurementRead,
    summary="Update an existing body measurement",
    description="Update the details of an existing body measurement by its unique ID.",
    response_description="Details of the updated body measurement",
    responses={
        200: {"description": "Body measurement updated successfully"},
        400: {"description": "Invalid input data"},
        404: {"description": "Body measurement not found"},
    },
)
async def update_body_measurement_endpoint(
    id: int,
    body_measurement: BodyMeasurementUpdate,
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> BodyMeasurementRead:
    """
    Update the details of an existing body measurement by its unique ID.
    """
    try:
        updated_body_measurement = await update_body_measurement(
            db, id, body_measurement
        )
        return updated_body_measurement
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
