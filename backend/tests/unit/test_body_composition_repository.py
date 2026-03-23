from datetime import date, datetime, timezone

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.body_measurements import BodyMeasurements
from app.models.user import Gender, User
from app.repositories import body_composition as composition_repo
from app.schemas.body_composition import (
    BodyCompositionCreate,
    BodyCompositionUpdate,
)


@pytest_asyncio.fixture
async def setup_user_and_measurements(async_session: AsyncSession):
    # Create a user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword",
        date_of_birth=date(1990, 1, 1),
        gender=Gender.MALE,
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create measurements
    measurements = BodyMeasurements(
        id_user=user.id,
        measure_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        height=180,
        neck=40,
        neck_to_shoulder=30,
        sleeve=60,
        bust=100,
        left_arm=35,
        right_arm=36,
        waist=80,
        hip=90,
        inseam_to_ankle=80,
        left_leg=50,
        right_leg=51,
        left_calf=35,
        right_calf=36,
        shoulders=45,
        trunk=50,
        pelvis=30,
    )
    async_session.add(measurements)
    await async_session.commit()
    await async_session.refresh(measurements)

    return user, measurements


@pytest.mark.asyncio
async def test_repo_create_composition(
    async_session: AsyncSession, setup_user_and_measurements
):
    user, measurements = setup_user_and_measurements
    create_data = BodyCompositionCreate(
        id_user=user.id,
        id_measurements=measurements.id,
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )

    created_measurement = await composition_repo.create_body_composition(
        async_session, create_data, id_user=user.id
    )

    assert created_measurement.id is not None


@pytest.mark.asyncio
async def test_repo_get_all_compositions(
    async_session: AsyncSession, setup_user_and_measurements
):
    user, measurements = setup_user_and_measurements
    create_data = BodyCompositionCreate(
        id_user=user.id,
        id_measurements=measurements.id,
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )
    await composition_repo.create_body_composition(
        async_session, create_data, id_user=user.id
    )

    measurements = await composition_repo.get_body_compositions(async_session)

    assert len(measurements) == 1
    assert measurements[0].id_user == user.id


@pytest.mark.asyncio
async def test_repo_get_compositions_by_user_id(
    async_session: AsyncSession, setup_user_and_measurements
):
    user, measurements = setup_user_and_measurements
    create_data = BodyCompositionCreate(
        id_user=user.id,
        id_measurements=measurements.id,
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )
    await composition_repo.create_body_composition(
        async_session, create_data, id_user=user.id
    )
    measurements = await composition_repo.get_body_composition_by_user_id(
        async_session, id_user=user.id
    )

    assert len(measurements) == 1
    assert measurements[0].id_user == user.id


@pytest.mark.asyncio
async def test_repo_update_composition(
    async_session: AsyncSession, setup_user_and_measurements
):
    user, measurements = setup_user_and_measurements
    create_data = BodyCompositionCreate(
        id_user=user.id,
        id_measurements=measurements.id,
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )
    created_composition = await composition_repo.create_body_composition(
        async_session, create_data, id_user=user.id
    )
    update_data = BodyCompositionUpdate(
        weight=85,
        fat_percentage=0.22,
        muscle_percentage=0.38,
        bone_percentage=0.06,
        water_percentage=0.32,
    )

    updated_composition = await composition_repo.update_body_composition(
        async_session, id=created_composition.id, body_composition=update_data
    )

    assert updated_composition.weight == 85
    assert updated_composition.fat_percentage == 0.22
    assert updated_composition.muscle_percentage == 0.38
    assert updated_composition.bone_percentage == 0.06
    assert updated_composition.water_percentage == 0.32
