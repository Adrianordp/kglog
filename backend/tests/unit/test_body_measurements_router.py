import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.database import AsyncGenerator, AsyncSession, get_async_db
from app.models.body_measurements import BodyMeasurements
from app.models.user import User
from app.routers.body_measurements import router as user_router


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
async def test_create_body_measurements_endpoint(
    async_client: AsyncClient, setup_user: User
):
    user = setup_user
    body_measurements_data = {
        "id_user": user.id,
        "measure_date": "2023-01-01T00:00:00",
        "height": 175.0,
        "neck": 40.0,
        "neck_to_shoulder": 15.0,
        "sleeve": 60.0,
        "bust": 100.0,
        "left_arm": 35.0,
        "right_arm": 35.0,
        "waist": 80.0,
        "hip": 90.0,
        "inseam_to_ankle": 80.0,
        "left_leg": 50.0,
        "right_leg": 50.0,
        "left_calf": 35.0,
        "right_calf": 35.0,
        "shoulders": 50.0,
        "trunk": 50.0,
        "pelvis": 30.0,
    }
    response = await async_client.post(
        "/body_measurements/", json=body_measurements_data
    )
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] is not None
    assert response_data["id_user"] == body_measurements_data["id_user"]
    assert (
        response_data["measure_date"] == body_measurements_data["measure_date"]
    )
    assert response_data["height"] == body_measurements_data["height"]
    assert response_data["neck"] == body_measurements_data["neck"]
    assert (
        response_data["neck_to_shoulder"]
        == body_measurements_data["neck_to_shoulder"]
    )
    assert response_data["sleeve"] == body_measurements_data["sleeve"]
    assert response_data["bust"] == body_measurements_data["bust"]
    assert response_data["left_arm"] == body_measurements_data["left_arm"]
    assert response_data["right_arm"] == body_measurements_data["right_arm"]
    assert response_data["waist"] == body_measurements_data["waist"]
    assert response_data["hip"] == body_measurements_data["hip"]
    assert (
        response_data["inseam_to_ankle"]
        == body_measurements_data["inseam_to_ankle"]
    )
    assert response_data["left_leg"] == body_measurements_data["left_leg"]
    assert response_data["right_leg"] == body_measurements_data["right_leg"]
    assert response_data["left_calf"] == body_measurements_data["left_calf"]
    assert response_data["right_calf"] == body_measurements_data["right_calf"]
    assert response_data["shoulders"] == body_measurements_data["shoulders"]
    assert response_data["trunk"] == body_measurements_data["trunk"]
    assert response_data["pelvis"] == body_measurements_data["pelvis"]


@pytest.mark.asyncio
async def test_get_body_measurements_endpoint(
    async_client: AsyncClient, setup_measurements: tuple[User, BodyMeasurements]
):
    user, measurements = setup_measurements
    response = await async_client.get("/body_measurements/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    response_data = response.json()[0]
    assert response_data["id"] == measurements.id
    assert response_data["id_user"] == user.id


@pytest.mark.asyncio
async def test_get_body_measurements_by_id_endpoint(
    async_client: AsyncClient, setup_measurements: tuple[User, BodyMeasurements]
):
    user, measurements = setup_measurements
    measurement_id = measurements.id
    response = await async_client.get(f"/body_measurements/{measurement_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == measurement_id
    assert response_data["id_user"] == user.id


@pytest.mark.asyncio
async def test_get_body_measurements_by_user_id_endpoint(
    async_client: AsyncClient, setup_measurements: tuple[User, BodyMeasurements]
):
    user, measurements = setup_measurements
    user_id = user.id
    response = await async_client.get(f"/body_measurements/user/{user_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    response_data = response.json()[0]
    assert response_data["id"] == measurements.id
    assert response_data["id_user"] == user_id


@pytest.mark.asyncio
async def test_delete_body_measurements_endpoint(
    async_client: AsyncClient, setup_measurements: tuple[User, BodyMeasurements]
):
    _, measurements = setup_measurements
    measurement_id = measurements.id
    response = await async_client.delete(f"/body_measurements/{measurement_id}")
    assert response.status_code == 204
    response = await async_client.get(f"/body_measurements/{measurement_id}")
    assert response.status_code == 404
