"""
Repository for managing users in the database.
"""

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing.

    Args:
        password: The plain text password to hash

    Returns:
        The hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


async def get_users(db: AsyncSession) -> list[User]:
    """
    Get all users.
    """
    stmt = select(User)
    query = await db.execute(stmt)
    result = query.scalars().all()

    return result


async def get_user_by_id(db: AsyncSession, id: int) -> User | None:
    """
    Get a user by ID.
    """
    stmt = select(User).where(User.id == id)
    query = await db.execute(stmt)
    result = query.scalars().first()

    return result


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    Create a new user.
    """
    user_data = user.model_dump()
    user_data["password_hash"] = get_password_hash(user_data["password"])
    user_data.pop("password")
    new_user = User(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def update_user(db: AsyncSession, id: int, user: UserUpdate) -> User:
    """
    Update an existing user.
    """
    stmt = select(User).where(User.id == id)
    query = await db.execute(stmt)
    query_element = query.scalars().first()

    if not query_element:
        raise ValueError(f"User with id {id} not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        if key == "password":
            value = get_password_hash(value)
            key = "password_hash"
        setattr(query_element, key, value)

    await db.commit()
    await db.refresh(query_element)

    return query_element
