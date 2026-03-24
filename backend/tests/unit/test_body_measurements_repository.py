import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import body_measurements as measurements_repo
from app.schemas.body_measurements import (
    BodyMeasurementCreate,
    BodyMeasurementUpdate,
)


@pytest.mark.asyncio
async def test_repo_create_measurements(async_session: AsyncSession):
    create_data = BodyMeasurementCreate(
        id_user=1,
        measure_date="2024-01-01T00:00:00",
        height=180.0,
        neck=40.0,
        neck_to_shoulder=20.0,
        sleeve=60.0,
        bust=100.0,
        left_arm=30.0,
        right_arm=30.0,
        waist=80.0,
        hip=90.0,
        inseam_to_ankle=80.0,
        left_leg=50.0,
        right_leg=50.0,
        left_calf=35.0,
        right_calf=35.0,
        shoulders=50.0,
        trunk=60.0,
        pelvis=40.0,
    )

    created_measurement = await measurements_repo.create_body_measurement(
        async_session, create_data
    )

    assert created_measurement.id is not None


@pytest.mark.asyncio
async def test_repo_get_all_measurements(async_session: AsyncSession):
    create_data = BodyMeasurementCreate(
        id_user=1,
        measure_date="2024-01-01T00:00:00",
        height=180.0,
        neck=40.0,
        neck_to_shoulder=20.0,
        sleeve=60.0,
        bust=100.0,
        left_arm=30.0,
        right_arm=30.0,
        waist=80.0,
        hip=90.0,
        inseam_to_ankle=80.0,
        left_leg=50.0,
        right_leg=50.0,
        left_calf=35.0,
        right_calf=35.0,
        shoulders=50.0,
        trunk=60.0,
        pelvis=40.0,
    )
    await measurements_repo.create_body_measurement(async_session, create_data)

    measurements = await measurements_repo.get_body_measurements(async_session)

    assert len(measurements) >= 1


@pytest.mark.asyncio
async def test_repo_get_measurements_by_user_id(async_session: AsyncSession):
    create_data = BodyMeasurementCreate(
        id_user=1,
        measure_date="2024-01-01T00:00:00",
        height=180.0,
        neck=40.0,
        neck_to_shoulder=20.0,
        sleeve=60.0,
        bust=100.0,
        left_arm=30.0,
        right_arm=30.0,
        waist=80.0,
        hip=90.0,
        inseam_to_ankle=80.0,
        left_leg=50.0,
        right_leg=50.0,
        left_calf=35.0,
        right_calf=35.0,
        shoulders=50.0,
        trunk=60.0,
        pelvis=40.0,
    )
    await measurements_repo.create_body_measurement(async_session, create_data)

    measurements = await measurements_repo.get_body_measurement_by_user_id(
        async_session, id_user=1
    )

    assert len(measurements) == 1
    assert measurements[0].id_user == 1


@pytest.mark.asyncio
async def test_repo_get_measurement_by_id(async_session: AsyncSession):
    create_data = BodyMeasurementCreate(
        id_user=1,
        measure_date="2024-01-01T00:00:00",
        height=180.0,
        neck=40.0,
        neck_to_shoulder=20.0,
        sleeve=60.0,
        bust=100.0,
        left_arm=30.0,
        right_arm=30.0,
        waist=80.0,
        hip=90.0,
        inseam_to_ankle=80.0,
        left_leg=50.0,
        right_leg=50.0,
        left_calf=35.0,
        right_calf=35.0,
        shoulders=50.0,
        trunk=60.0,
        pelvis=40.0,
    )
    created_measurement = await measurements_repo.create_body_measurement(
        async_session, create_data
    )

    measurement = await measurements_repo.get_body_measurement_by_id(
        async_session, id=created_measurement.id
    )

    assert measurement is not None
    assert measurement.id == created_measurement.id
    assert measurement.id_user == 1


@pytest.mark.asyncio
async def test_repo_update_measurement(async_session: AsyncSession):
    create_data = BodyMeasurementCreate(
        id_user=1,
        measure_date="2024-01-01T00:00:00",
        height=180.0,
        neck=40.0,
        neck_to_shoulder=20.0,
        sleeve=60.0,
        bust=100.0,
        left_arm=30.0,
        right_arm=30.0,
        waist=80.0,
        hip=90.0,
        inseam_to_ankle=80.0,
        left_leg=50.0,
        right_leg=50.0,
        left_calf=35.0,
        right_calf=35.0,
        shoulders=50.0,
        trunk=60.0,
        pelvis=40.0,
    )
    created_measurement = await measurements_repo.create_body_measurement(
        async_session, create_data
    )
    update_data = BodyMeasurementUpdate(height=185.0)

    updated_measurement = await measurements_repo.update_body_measurement(
        async_session, id=created_measurement.id, body_measurement=update_data
    )

    assert updated_measurement.height == 185.0
