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


async def viceral_fat_formula(
    db: AsyncSession, id_user: int, body_comp: BodyCompositionCreate
) -> float:
    """
    Calculate visceral fat based on weight and fat percentage.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, you would retrieve this data from the
    database.

    Args:
        db: The database session to retrieve user data if needed for the
        calculation
        id_user: The ID of the user to retrieve measurements for
        body_comp: The body composition data to calculate visceral fat for
    Returns:
        The calculated visceral fat level in cm²
    """

    class MockMeasurement:
        def __init__(self, height: float, waist: float, hip: float):
            self.height = height
            self.waist = waist
            self.hip = hip

    class MockUser:
        def __init__(self, id: int, gender: str):
            self.id = id
            self.gender = gender

    msmnt = MockMeasurement(170, 80, 100)
    user = MockUser(id_user, "MALE")

    if user.gender not in ["MALE", "FEMALE"]:
        raise ValueError(
            "User gender must be either 'MALE' or 'FEMALE' for visceral fat"
            "calculation"
        )

    bmi = body_comp.weight / (msmnt.height / 100) ** 2
    whtr = msmnt.waist / msmnt.height
    whr = msmnt.waist / msmnt.hip

    if user.gender == "MALE":
        vfa = 2.5 * msmnt.waist + 120 * whtr + 80 * whr + 8 * bmi - 300
    else:
        vfa = 2 * msmnt.waist + 100 * whtr + 60 * whr + 6 * bmi - 250

    # limb_factor = (
    #     msmnt.left_leg + msmnt.right_leg + msmnt.left_arm + msmnt.right_arm
    # ) / (4 * msmnt.waist)

    # vfa = 180 * whtr + 40 * whr + 4 * bmi - 120 * limb_factor

    return max(vfa, 0)


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
    # Estimate visceral fat if not provided
    if body_composition.visceral_fat is None:
        body_composition.visceral_fat = await viceral_fat_formula(
            db, id_user, body_composition
        )

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

    new_body_composition = BodyComposition(
        id_user=id_user,
        **body_composition.model_dump(),
        **kg_data,
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

    for key, value in body_composition.model_dump(
        exclude_unset=True, exclude_none=True
    ).items():
        setattr(query_element, key, value)

    await db.commit()
    await db.refresh(query_element)

    return query_element
