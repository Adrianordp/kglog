from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user as user_repo
from app.schemas.user import Gender, UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_repo_create_user(async_session: AsyncSession):
    create_data = UserCreate(
        username="Test User",
        email="testuser@example.com",
        password="a_secure_password",
        date_of_birth="1990-01-01",
        gender="MALE",
    )

    created_user = await user_repo.create_user(async_session, create_data)

    assert created_user.id is not None
    assert created_user.username == "Test User"
    assert created_user.email == "testuser@example.com"
    assert created_user.password_hash is not None
    assert created_user.password_hash != "a_secure_password"
    assert created_user.date_of_birth == date.fromisoformat("1990-01-01")
    assert created_user.gender == Gender.MALE


@pytest.mark.asyncio
async def test_repo_get_all_users(async_session: AsyncSession):
    create_data = UserCreate(
        username="Test User",
        email="testuser@example.com",
        password="a_secure_password",
        date_of_birth="1990-01-01",
        gender="MALE",
    )
    await user_repo.create_user(async_session, create_data)

    users = await user_repo.get_users(async_session)

    assert len(users) == 1


@pytest.mark.asyncio
async def test_repo_get_user_by_id(async_session: AsyncSession):
    create_data = UserCreate(
        username="Test User",
        email="testuser@example.com",
        password="a_secure_password",
        date_of_birth="1990-01-01",
        gender="MALE",
    )
    created_user = await user_repo.create_user(async_session, create_data)

    user = await user_repo.get_user_by_id(async_session, created_user.id)

    assert user is not None
    assert user.id == created_user.id


@pytest.mark.asyncio
async def test_repo_update_user(async_session: AsyncSession):
    create_data = UserCreate(
        username="Test User",
        email="testuser@example.com",
        password="a_secure_password",
        date_of_birth="1990-01-01",
        gender="MALE",
    )
    created_user = await user_repo.create_user(async_session, create_data)
    old_password_hash = created_user.password_hash

    update_data = UserUpdate(
        username="Updated User",
        email="updateduser@example.com",
        password="a_new_secure_password",
        date_of_birth="1991-01-01",
        gender="FEMALE",
    )

    updated_user = await user_repo.update_user(
        async_session, id=created_user.id, user=update_data
    )

    assert updated_user.id == created_user.id
    assert updated_user.username == "Updated User"
    assert updated_user.email == "updateduser@example.com"
    assert updated_user.password_hash is not None
    assert updated_user.password_hash != "a_new_secure_password"
    assert old_password_hash != updated_user.password_hash
    assert updated_user.date_of_birth == date.fromisoformat("1991-01-01")
    assert updated_user.gender == Gender.FEMALE


@pytest.mark.asyncio
async def test_repo_delete_user(async_session: AsyncSession):
    create_data = UserCreate(
        username="Test User",
        email="testuser@example.com",
        password="a_secure_password",
        date_of_birth="1990-01-01",
        gender="MALE",
    )
    created_user = await user_repo.create_user(async_session, create_data)

    await user_repo.delete_user(async_session, created_user.id)

    user = await user_repo.get_user_by_id(async_session, created_user.id)
    assert user is None
