"""
Repository for managing body measurements in the database.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.body_measurements import BodyMeasurements
from app.schemas.body_measurements import (
    BodyMeasurementCreate,
    BodyMeasurementUpdate,
)


async def get_body_measurements(db: AsyncSession) -> list[BodyMeasurements]:
    """
    Get all body measurements.
    """
    stmt = select(BodyMeasurements)
    query = await db.execute(stmt)
    result = query.scalars().all()

    return result


async def get_body_measurement_by_id(
    db: AsyncSession, id: int
) -> BodyMeasurements | None:
    """
    Get a body measurement by ID.
    """
    stmt = select(BodyMeasurements).where(BodyMeasurements.id == id)
    query = await db.execute(stmt)
    result = query.scalar_one_or_none()

    return result


async def get_body_measurement_by_user_id(
    db: AsyncSession, id_user: int
) -> list[BodyMeasurements]:
    """
    Get body measurements by user ID.
    """
    stmt = select(BodyMeasurements).where(BodyMeasurements.id_user == id_user)
    query = await db.execute(stmt)
    result = query.scalars().all()

    return result


async def create_body_measurement(
    db: AsyncSession, body_measurement: BodyMeasurementCreate
) -> BodyMeasurements:
    """
    Create a new body measurement.
    """
    new_body_measurement = BodyMeasurements(
        **body_measurement.model_dump(),
    )
    db.add(new_body_measurement)
    await db.commit()
    await db.refresh(new_body_measurement)

    return new_body_measurement


async def update_body_measurement(
    db: AsyncSession, id: int, body_measurement: BodyMeasurementUpdate
) -> BodyMeasurements:
    """
    Update an existing body measurement.
    """
    stmt = select(BodyMeasurements).where(BodyMeasurements.id == id)
    query_result = await db.execute(stmt)
    query_element = query_result.scalar_one_or_none()

    if not query_element:
        raise ValueError(f"Body measurement with id {id} not found")

    for key, value in body_measurement.model_dump(
        exclude_unset=True, exclude_none=True
    ).items():
        setattr(query_element, key, value)

    await db.commit()
    await db.refresh(query_element)

    return query_element


async def delete_body_measurement(db: AsyncSession, id: int) -> None:
    """
    Delete a body measurement by ID.
    """
    stmt = select(BodyMeasurements).where(BodyMeasurements.id == id)
    query_result = await db.execute(stmt)
    query_element = query_result.scalar_one_or_none()

    if not query_element:
        raise ValueError(f"Body measurement with id {id} not found")

    await db.delete(query_element)
    await db.commit()
