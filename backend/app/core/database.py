"""
Database configuration and session management for the application.
"""

from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings

DATABASE_URL = settings.DATABASE_URL
DEBUG = settings.DEBUG

async_engine = create_async_engine(DATABASE_URL, echo=DEBUG, future=True)

sync_engine = create_engine(DATABASE_URL, echo=DEBUG, future=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
