"""
Repository for managing body measurements in the database.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.body_measurements import BodyMeasurements
from app.schemas.body_measurements import (
    BodyMeasurementCreate,
    BodyMeasurementRead,
    BodyMeasurementUpdate,
)


async def get_body_measurements(db: AsyncSession) -> list[BodyMeasurementRead]:
    """
    Get all body measurements.
    """
    stmt = select(BodyMeasurements)
    query_result = await db.execute(stmt)
    query_list = query_result.scalars().all()
    result = [BodyMeasurementRead.model_validate(bm) for bm in query_list]

    return result


async def get_body_measurement_by_user_id(
    db: AsyncSession, id_user: int
) -> list[BodyMeasurementRead]:
    """
    Get body measurements by user ID.
    """
    stmt = select(BodyMeasurements).where(BodyMeasurements.id_user == id_user)
    query_result = await db.execute(stmt)
    query_list = query_result.scalars().all()
    result = [BodyMeasurementRead.model_validate(bm) for bm in query_list]

    return result


async def create_body_measurement(
    db: AsyncSession, body_measurement: BodyMeasurementCreate, id_user: int
) -> BodyMeasurementRead:
    """
    Create a new body measurement.
    """
    new_body_measurement = BodyMeasurements(
        id_user=id_user,
        **body_measurement.model_dump(),
    )
    db.add(new_body_measurement)
    await db.commit()
    await db.refresh(new_body_measurement)

    return BodyMeasurementRead.model_validate(new_body_measurement)


async def update_body_measurement(
    db: AsyncSession, id: int, body_measurement: BodyMeasurementUpdate
) -> BodyMeasurementRead:
    """
    Update an existing body measurement.
    """
    stmt = select(BodyMeasurements).where(BodyMeasurements.id == id)
    query = await db.execute(stmt)
    existing_body_measurement = query.scalar_one_or_none()

    if not existing_body_measurement:
        raise ValueError(f"Body measurement with id {id} not found")

    for key, value in body_measurement.model_dump(exclude_unset=True).items():
        setattr(existing_body_measurement, key, value)

    await db.commit()
    await db.refresh(existing_body_measurement)

    return BodyMeasurementRead.model_validate(existing_body_measurement)
