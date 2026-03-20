"""
Repository for managing body composition in the database.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.body_composition import BodyComposition
from app.schemas.body_composition import (
    BodyCompositionCreate,
    BodyCompositionRead,
    BodyCompositionUpdate,
)


async def get_body_compositions(db: AsyncSession) -> list[BodyCompositionRead]:
    """
    Get all body compositions.
    """
    stmt = select(BodyComposition)
    query = await db.execute(stmt)
    result = query.scalars().all()

    return result


async def get_body_composition_by_user_id(
    db: AsyncSession, id_user: int
) -> list[BodyComposition]:
    """
    Get body compositions by user ID.
    """
    stmt = select(BodyComposition).where(BodyComposition.id_user == id_user)
    query = await db.execute(stmt)
    result = query.scalars().all()

    return result


async def create_body_composition(
    db: AsyncSession, body_composition: BodyCompositionCreate, id_user: int
) -> BodyComposition:
    """
    Create a new body composition.
    """
    # Fill the kg data based on the percentage data
    kg_data = {}
    kg_data["fat_kg"] = (
        body_composition.weight * body_composition.fat_percentage
    )
    kg_data["muscle_kg"] = (
        body_composition.weight * body_composition.muscle_percentage
    )
    kg_data["bone_kg"] = (
        body_composition.weight * body_composition.bone_percentage
    )
    kg_data["water_kg"] = (
        body_composition.weight * body_composition.water_percentage
    )

    # Calculate visceral fat based on weight and fat percentage (this is a simplified formula for demonstration purposes)
    # This is a placeholder formula and should be replaced with a more
    visceral_fat = (
        body_composition.weight * body_composition.fat_percentage * 0.1
    )

    new_body_composition = BodyComposition(
        id_user=id_user,
        **body_composition.model_dump(),
        **kg_data,
        visceral_fat=visceral_fat,
    )
    print(new_body_composition.__dict__)
    db.add(new_body_composition)
    await db.commit()
    await db.refresh(new_body_composition)

    return new_body_composition


async def update_body_composition(
    db: AsyncSession, id: int, body_composition: BodyCompositionUpdate
) -> BodyComposition:
    """
    Update an existing body composition.
    """
    stmt = select(BodyComposition).where(BodyComposition.id == id)
    query_result = await db.execute(stmt)
    query_element = query_result.scalar_one_or_none()

    if query_element is None:
        raise ValueError(f"Body composition with ID {id} not found")

    for key, value in body_composition.model_dump(exclude_unset=True).items():
        setattr(query_element, key, value)

    await db.commit()
    await db.refresh(query_element)

    return query_element
