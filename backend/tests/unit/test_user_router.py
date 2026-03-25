import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.database import AsyncGenerator, AsyncSession, get_async_db
from app.models.user import User
from app.routers.user import router as user_router


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
async def test_create_user_endpoint(async_client: AsyncClient):
    user_data = {
        "username": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
        "date_of_birth": "1990-01-01",
        "gender": "MALE",
    }
    response = await async_client.post("/users/", json=user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] is not None
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert "password_hash" not in response_data
    assert response_data["date_of_birth"] == user_data["date_of_birth"]
    assert response_data["gender"] == user_data["gender"]
    assert response_data["created_at"] is not None
    assert response_data["updated_at"] is not None


@pytest.mark.asyncio
async def test_get_users_endpoint(async_client: AsyncClient, setup_user: User):
    user = setup_user
    response = await async_client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    response_data = response.json()[0]
    assert response_data["id"] == user.id


@pytest.mark.asyncio
async def test_get_user_by_id_endpoint(
    async_client: AsyncClient, setup_user: User
):
    user = setup_user
    response = await async_client.get(f"/users/{user.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user.id


@pytest.mark.asyncio
async def test_update_user_endpoint(
    async_client: AsyncClient, setup_user: User
):
    user = setup_user
    update_data = {
        "username": "Updated User",
        "email": "updateduser@example.com",
        "password": "newpassword123",
        "date_of_birth": "1991-01-01",
        "gender": "FEMALE",
    }
    response = await async_client.put(f"/users/{user.id}", json=update_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user.id


@pytest.mark.asyncio
async def test_delete_user_endpoint(
    async_client: AsyncClient, setup_user: User
):
    user = setup_user
    response = await async_client.delete(f"/users/{user.id}")
    assert response.status_code == 204
    response = await async_client.get(f"/users/{user.id}")
    assert response.status_code == 404
