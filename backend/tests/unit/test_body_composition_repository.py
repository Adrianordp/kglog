import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import body_composition as composition_repo
from app.schemas.body_composition import (
    BodyCompositionCreate,
    BodyCompositionUpdate,
)


@pytest.mark.asyncio
async def test_repo_create_composition(async_session: AsyncSession):
    create_data = BodyCompositionCreate(
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )

    created_measurement = await composition_repo.create_body_composition(
        async_session, create_data, id_user=1
    )

    assert created_measurement.id is not None


@pytest.mark.asyncio
async def test_repo_get_all_compositions(async_session: AsyncSession):
    create_data = BodyCompositionCreate(
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )
    await composition_repo.create_body_composition(
        async_session, create_data, id_user=1
    )

    measurements = await composition_repo.get_body_compositions(async_session)

    assert len(measurements) == 1
    assert measurements[0].id_user == 1


@pytest.mark.asyncio
async def test_repo_get_compositions_by_user_id(async_session: AsyncSession):
    create_data = BodyCompositionCreate(
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )
    await composition_repo.create_body_composition(
        async_session, create_data, id_user=1
    )
    measurements = await composition_repo.get_body_composition_by_user_id(
        async_session, id_user=1
    )

    assert len(measurements) == 1
    assert measurements[0].id_user == 1


@pytest.mark.asyncio
async def test_repo_update_composition(async_session: AsyncSession):
    create_data = BodyCompositionCreate(
        measure_date="2024-01-01T00:00:00",
        weight=80,
        fat_percentage=0.20,
        muscle_percentage=0.40,
        bone_percentage=0.05,
        water_percentage=0.35,
    )
    created_composition = await composition_repo.create_body_composition(
        async_session, create_data, id_user=1
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
