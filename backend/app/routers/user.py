from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.repositories.user import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information.",
    response_description="Details of the created user",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input data"},
    },
)
async def create_user_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)], user: UserCreate
) -> UserRead:
    """
    Create a new user with the provided information.
    """
    return await create_user(db, user)


@router.get(
    "/",
    response_model=List[UserRead],
    summary="Get all users",
    description="Retrieve a list of all users in the system.",
    response_description="List of users",
)
async def get_users_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> List[UserRead]:
    """
    Retrieve a list of all users in the system.
    """
    return await get_users(db)


@router.get(
    "/{id}",
    response_model=UserRead,
    summary="Get a user by ID",
    description="Retrieve a user by their unique ID.",
    response_description="Details of the user",
    responses={
        200: {"description": "User retrieved successfully"},
        404: {"description": "User not found"},
    },
)
async def get_user_by_id_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)], id: int
) -> UserRead:
    """
    Retrieve a user by their unique ID.
    """
    user = await get_user_by_id(db, id)

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found"
        )

    return user


@router.put(
    "/{id}",
    response_model=UserRead,
    summary="Update an existing user",
    description="Update an existing user's information by their unique ID.",
    response_description="Details of the updated user",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Invalid input data"},
        404: {"description": "User not found"},
    },
)
async def update_user_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    id: int,
    user: UserUpdate,
) -> UserRead:
    """
    Update an existing user's information by their unique ID.

    - **username**: Unique username for the user
    - **email**: User's email address
    - **password**: User's password (will be hashed before storing)
    """
    return await update_user(db, id, user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Delete a user by their unique ID.",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
    },
)
async def delete_user_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)], id: int
) -> None:
    """
    Delete a user by their unique ID.
    """
    try:
        await delete_user(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
