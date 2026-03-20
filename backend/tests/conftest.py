import os

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:"
)
_IS_SQLITE = TEST_DATABASE_URL.startswith("sqlite")


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """Session-scoped engine. Uses PostgreSQL when TEST_DATABASE_URL is set, SQLite otherwise."""
    kwargs = {"echo": False, "future": True}

    engine = create_async_engine(TEST_DATABASE_URL, **kwargs)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        if _IS_SQLITE:
            await conn.run_sync(Base.metadata.drop_all)
        else:
            await conn.execute(
                __import__("sqlalchemy").text("DROP SCHEMA public CASCADE")
            )
            await conn.execute(
                __import__("sqlalchemy").text("CREATE SCHEMA public")
            )
            await conn.execute(
                __import__("sqlalchemy").text(
                    "GRANT ALL ON SCHEMA public TO PUBLIC"
                )
            )

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
        if _IS_SQLITE:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())
        else:
            table_names = ", ".join(
                f'"{t.name}"' for t in reversed(Base.metadata.sorted_tables)
            )
            await conn.execute(
                __import__("sqlalchemy").text(
                    f"TRUNCATE {table_names} RESTART IDENTITY CASCADE"
                )
            )
