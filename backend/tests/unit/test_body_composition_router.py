from datetime import date, datetime

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.database import AsyncGenerator, AsyncSession, get_async_db
from app.models.body_composition import BodyComposition
from app.models.body_measurements import BodyMeasurements
from app.models.user import Gender, User
from app.routers.body_composition import router as user_router


@pytest_asyncio.fixture
async def app() -> FastAPI:
    test_app = FastAPI()
    test_app.include_router(user_router)
    return test_app


@pytest_asyncio.fixture
async def async_client(
    app: FastAPI, async_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def setup_data(
    async_session: AsyncSession,
) -> tuple[User, BodyMeasurements, BodyComposition]:

    user = User(
        username="Test User",
        email="test@example.com",
        password_hash="hashedpassword",
        date_of_birth=date(1990, 1, 1),
        gender=Gender.MALE,
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    measurements = BodyMeasurements(
        id_user=user.id,
        measure_date=datetime(2023, 1, 1),
        height=175.0,
        neck=40.0,
        neck_to_shoulder=15.0,
        sleeve=60.0,
        bust=100.0,
        left_arm=35.0,
        right_arm=35.0,
        waist=80.0,
        hip=90.0,
        inseam_to_ankle=80.0,
        left_leg=50.0,
        right_leg=50.0,
        left_calf=35.0,
        right_calf=35.0,
        shoulders=50.0,
        trunk=50.0,
        pelvis=30.0,
    )
    async_session.add(measurements)
    await async_session.commit()
    await async_session.refresh(measurements)

    body_composition = BodyComposition(
        id_user=user.id,
        measure_date=datetime(2023, 1, 1),
        weight=100.0,
        fat_percentage=0.2,
        fat_kg=20.0,
        water_percentage=0.6,
        water_kg=60.0,
        muscle_percentage=0.4,
        muscle_kg=40.0,
        bone_percentage=0.5,
        bone_kg=50.0,
        visceral_fat=100.0,
    )
    async_session.add(body_composition)
    await async_session.commit()
    await async_session.refresh(body_composition)

    return user, measurements, body_composition


@pytest.mark.asyncio
async def test_create_body_composition_endpoint(
    async_client: AsyncClient, setup_data
):
    user, measurements, _ = setup_data
    body_composition_data = {
        "id_user": user.id,
        "measure_date": "2023-01-01T00:00:00",
        "id_measurements": measurements.id,
        "weight": 70.0,
    }
    response = await async_client.post(
        "/body_composition/", json=body_composition_data
    )
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] is not None
    assert response_data["id_user"] == body_composition_data["id_user"]
    assert (
        response_data["measure_date"] == body_composition_data["measure_date"]
    )
    assert (
        response_data["id_measurements"]
        == body_composition_data["id_measurements"]
    )
    assert response_data["weight"] == body_composition_data["weight"]


@pytest.mark.asyncio
async def test_get_body_composition_endpoint(
    async_client: AsyncClient, setup_data
):
    user, measurements, body_composition = setup_data
    response = await async_client.get(
        f"/body_composition/{body_composition.id}"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == body_composition.id
    assert response_data["id_user"] == body_composition.id_user
    assert (
        response_data["measure_date"]
        == body_composition.measure_date.isoformat()
    )
    assert response_data["id_measurements"] == body_composition.id_measurements
    assert response_data["weight"] == body_composition.weight
    assert response_data["fat_percentage"] == body_composition.fat_percentage
    assert response_data["fat_kg"] == body_composition.fat_kg
    assert (
        response_data["muscle_percentage"] == body_composition.muscle_percentage
    )
    assert response_data["muscle_kg"] == body_composition.muscle_kg
    assert response_data["bone_percentage"] == body_composition.bone_percentage
    assert response_data["bone_kg"] == body_composition.bone_kg
    assert (
        response_data["water_percentage"] == body_composition.water_percentage
    )
    assert response_data["water_kg"] == body_composition.water_kg
    assert response_data["visceral_fat"] == body_composition.visceral_fat


@pytest.mark.asyncio
async def test_get_body_compositions_by_user_id_endpoint(
    async_client: AsyncClient, setup_data
):
    user, _, body_composition = setup_data
    response = await async_client.get(f"/body_composition/user/{user.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    assert response_data[0]["id"] == body_composition.id
    assert response_data[0]["id_user"] == body_composition.id_user
    assert (
        response_data[0]["measure_date"]
        == body_composition.measure_date.isoformat()
    )
    assert (
        response_data[0]["id_measurements"] == body_composition.id_measurements
    )
    assert response_data[0]["weight"] == body_composition.weight
    assert response_data[0]["fat_percentage"] == body_composition.fat_percentage
    assert response_data[0]["fat_kg"] == body_composition.fat_kg
    assert (
        response_data[0]["muscle_percentage"]
        == body_composition.muscle_percentage
    )
    assert response_data[0]["muscle_kg"] == body_composition.muscle_kg
    assert (
        response_data[0]["bone_percentage"] == body_composition.bone_percentage
    )
    assert response_data[0]["bone_kg"] == body_composition.bone_kg
    assert (
        response_data[0]["water_percentage"]
        == body_composition.water_percentage
    )
    assert response_data[0]["water_kg"] == body_composition.water_kg
    assert response_data[0]["visceral_fat"] == body_composition.visceral_fat


@pytest.mark.asyncio
async def test_update_body_composition_endpoint(
    async_client: AsyncClient, setup_data
):
    _, _, body_composition = setup_data
    updated_body_composition_data = {
        "weight": 75.0,
    }
    response = await async_client.put(
        f"/body_composition/{body_composition.id}",
        json=updated_body_composition_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["weight"] == updated_body_composition_data["weight"]


@pytest.mark.asyncio
async def test_delete_body_composition_endpoint(
    async_client: AsyncClient, setup_data
):
    _, _, body_composition = setup_data
    response = await async_client.delete(
        f"/body_composition/{body_composition.id}"
    )
    assert response.status_code == 204
    response = await async_client.get(
        f"/body_composition/{body_composition.id}"
    )
    assert response.status_code == 404
