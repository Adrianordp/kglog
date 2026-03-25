import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.database import AsyncGenerator, AsyncSession, get_async_db
from app.models.body_composition import BodyComposition
from app.models.body_measurements import BodyMeasurements
from app.models.user import User
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


@pytest.mark.asyncio
async def test_create_body_composition_endpoint_with_measurements(
    async_client: AsyncClient, setup_measurements: tuple[User, BodyMeasurements]
):
    user, measurements = setup_measurements
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
    assert response_data["id_user"] == user.id
    assert response_data["id_measurements"] == measurements.id
    assert response_data["weight"] == body_composition_data["weight"]
    assert (
        response_data["measure_date"] == body_composition_data["measure_date"]
    )
    assert response_data["fat_percentage"] is not None
    assert response_data["muscle_percentage"] is not None
    assert response_data["bone_percentage"] is not None
    assert response_data["water_percentage"] is not None
    assert response_data["visceral_fat"] is not None
    assert response_data["fat_kg"] is not None
    assert response_data["muscle_kg"] is not None
    assert response_data["bone_kg"] is not None
    assert response_data["water_kg"] is not None


@pytest.mark.asyncio
async def test_create_body_composition_endpoint_without_measurements(
    async_client: AsyncClient, setup_user: User
):
    user = setup_user
    body_composition_data = {
        "id_user": user.id,
        "measure_date": "2023-01-01T00:00:00",
        "weight": 70.0,
        "fat_percentage": 0.20,
        "muscle_percentage": 0.40,
        "bone_percentage": 0.05,
        "water_percentage": 0.35,
        "visceral_fat": 10.0,
    }
    response = await async_client.post(
        "/body_composition/", json=body_composition_data
    )
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] is not None
    assert response_data["id_user"] == user.id
    assert response_data["weight"] == body_composition_data["weight"]
    assert (
        response_data["measure_date"] == body_composition_data["measure_date"]
    )
    assert (
        response_data["fat_percentage"]
        == body_composition_data["fat_percentage"]
    )
    assert (
        response_data["muscle_percentage"]
        == body_composition_data["muscle_percentage"]
    )
    assert (
        response_data["bone_percentage"]
        == body_composition_data["bone_percentage"]
    )
    assert (
        response_data["water_percentage"]
        == body_composition_data["water_percentage"]
    )
    assert (
        response_data["visceral_fat"] == body_composition_data["visceral_fat"]
    )
    assert response_data["fat_kg"] is not None
    assert response_data["muscle_kg"] is not None
    assert response_data["bone_kg"] is not None
    assert response_data["water_kg"] is not None


@pytest.mark.asyncio
async def test_get_body_composition_endpoint(
    async_client: AsyncClient,
    setup_composition: tuple[User, BodyComposition],
):
    user, body_composition = setup_composition
    response = await async_client.get(
        f"/body_composition/{body_composition.id}"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == body_composition.id
    assert response_data["id_user"] == user.id


@pytest.mark.asyncio
async def test_get_body_compositions_by_id_endpoint(
    async_client: AsyncClient,
    setup_composition: tuple[User, BodyComposition],
):
    user, body_composition = setup_composition
    response = await async_client.get(
        f"/body_composition/{body_composition.id}"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == body_composition.id
    assert response_data["id_user"] == user.id


@pytest.mark.asyncio
async def test_get_body_compositions_by_user_id_endpoint(
    async_client: AsyncClient,
    setup_composition: tuple[User, BodyComposition],
):
    user, body_composition = setup_composition
    response = await async_client.get(f"/body_composition/user/{user.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    assert response_data[0]["id"] == body_composition.id
    assert response_data[0]["id_user"] == user.id


@pytest.mark.asyncio
async def test_update_body_composition_endpoint(
    async_client: AsyncClient,
    setup_composition: tuple[User, BodyComposition],
):
    _, body_composition = setup_composition
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
    async_client: AsyncClient,
    setup_composition: tuple[User, BodyComposition],
):
    _, body_composition = setup_composition
    response = await async_client.delete(
        f"/body_composition/{body_composition.id}"
    )
    assert response.status_code == 204
    response = await async_client.get(
        f"/body_composition/{body_composition.id}"
    )
    assert response.status_code == 404
