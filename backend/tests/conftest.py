import os
from datetime import date

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.body_composition import BodyComposition
from app.models.body_measurements import BodyMeasurements
from app.models.user import Gender, User

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:"
)


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """Session-scoped engine. Uses PostgreSQL when TEST_DATABASE_URL is set, SQLite otherwise."""
    kwargs = {"echo": False, "future": True}

    engine = create_async_engine(TEST_DATABASE_URL, **kwargs)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(db_engine):
    """Provide a session and truncate all tables after each test for isolation."""
    async_session_factory = sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with async_session_factory() as session:
        yield session
    async with db_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def setup_user(async_session: AsyncSession) -> User:
    user = User(
        username="Test User",
        email="testuser@example.com",
        password_hash="hashedpassword",
        date_of_birth=date(1990, 1, 1),
        gender=Gender.MALE,
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def setup_measurements(
    async_session: AsyncSession, setup_user: User
) -> tuple[User, BodyMeasurements]:
    user = setup_user
    measurements = BodyMeasurements(
        id_user=user.id,
        measure_date=date(2023, 1, 1),
        height=175.0,
        neck=40.0,
        neck_to_shoulder=15.0,
        sleeve=60.0,
        bust=100.0,
        left_arm=35.0,
        right_arm=36.0,
        waist=80.0,
        hip=90.0,
        inseam_to_ankle=80.0,
        left_leg=50.0,
        right_leg=51.0,
        left_calf=35.0,
        right_calf=36.0,
        shoulders=45.0,
        trunk=50.0,
        pelvis=30.0,
    )
    async_session.add(measurements)
    await async_session.commit()
    await async_session.refresh(measurements)
    return user, measurements


@pytest_asyncio.fixture
async def setup_composition(
    async_session: AsyncSession, setup_user: User
) -> tuple[User, BodyComposition]:
    user = setup_user
    composition = BodyComposition(
        id_user=user.id,
        measure_date=date(2023, 1, 1),
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
    async_session.add(composition)
    await async_session.commit()
    await async_session.refresh(composition)
    return user, composition
