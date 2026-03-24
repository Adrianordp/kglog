from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.repositories.body_composition import (
    create_body_composition,
    get_body_composition_by_id,
    get_body_composition_by_user_id,
    get_body_compositions,
    get_user_by_id,
    update_body_composition,
)
from app.schemas.body_composition import (
    BodyCompositionCreate,
    BodyCompositionRead,
    BodyCompositionUpdate,
)

router = APIRouter(prefix="/body_composition", tags=["body_composition"])


@router.post(
    "/",
    response_model=BodyCompositionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new body composition",
    description="Create a new body composition with the provided information.",
    response_description="Details of the created body composition",
    responses={
        201: {"description": "Body composition created successfully"},
        400: {"description": "Invalid input data"},
    },
)
async def create_body_composition_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    body_composition: BodyCompositionCreate,
) -> BodyCompositionRead:
    """
    Create a new body composition with the provided information.
    """
    return await create_body_composition(db, body_composition)


@router.get(
    "/",
    response_model=List[BodyCompositionRead],
    summary="Get all body compositions",
    description="Retrieve a list of all body compositions.",
    response_description="List of body compositions",
)
async def get_body_compositions_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> List[BodyCompositionRead]:
    """
    Retrieve a list of all body compositions.
    """
    return await get_body_compositions(db)


@router.get(
    "/{id}",
    response_model=BodyCompositionRead,
    summary="Get body composition by ID",
    description="Retrieve details of a specific body composition by its ID.",
    response_description="Details of the specified body composition",
    responses={
        200: {"description": "Body composition retrieved successfully"},
        404: {"description": "Body composition not found"},
    },
)
async def get_body_composition_by_id_endpoint(
    id: int,
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> BodyCompositionRead:
    """
    Retrieve details of a specific body composition by its ID.
    """
    body_composition = await get_body_composition_by_id(db, id)

    if not body_composition:
        raise HTTPException(
            status_code=404, detail="Body composition not found"
        )

    return body_composition


@router.get(
    "/user/{id_user}",
    response_model=List[BodyCompositionRead],
    summary="Get body compositions by user ID",
    description="Retrieve a list of body compositions for a specific user.",
    response_description="List of body compositions for the specified user",
    responses={
        200: {"description": "Body compositions retrieved successfully"},
        404: {"description": "User not found"},
    },
)
async def get_body_compositions_by_user_id_endpoint(
    id_user: int,
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> List[BodyCompositionRead]:
    """
    Retrieve a list of body compositions for a specific user.
    """
    user = await get_user_by_id(db, id_user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await get_body_composition_by_user_id(db, id_user)


@router.put(
    "/{id}",
    response_model=BodyCompositionRead,
    summary="Update body composition",
    description="Update an existing body composition with the provided information.",
    response_description="Details of the updated body composition",
    responses={
        200: {"description": "Body composition updated successfully"},
        400: {"description": "Invalid input data"},
        404: {"description": "Body composition not found"},
    },
)
async def update_body_composition_endpoint(
    id: int,
    body_composition: BodyCompositionUpdate,
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> BodyCompositionRead:
    """
    Update an existing body composition with the provided information.
    """
    existing_body_composition = await get_body_composition_by_id(db, id)

    if not existing_body_composition:
        raise HTTPException(
            status_code=404, detail="Body composition not found"
        )

    return await update_body_composition(db, id, body_composition)
