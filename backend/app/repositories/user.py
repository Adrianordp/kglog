"""
Repository for managing users in the database.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


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
    user_data = user.model_dump(exclude={"password"})
    user_data["password_hash"] = get_password_hash(
        user.password.get_secret_value()
    )
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

    update_data = user.model_dump(
        exclude={"password"}, exclude_unset=True, exclude_none=True
    )
    if user.password is not None:
        update_data["password_hash"] = get_password_hash(
            user.password.get_secret_value()
        )
    for key, value in update_data.items():
        setattr(query_element, key, value)

    await db.commit()
    await db.refresh(query_element)

    return query_element


async def delete_user(db: AsyncSession, id: int) -> None:
    """
    Delete a user by ID.
    """
    stmt = select(User).where(User.id == id)
    query = await db.execute(stmt)
    query_element = query.scalars().first()

    if not query_element:
        raise ValueError(f"User with id {id} not found")

    await db.delete(query_element)
    await db.commit()
