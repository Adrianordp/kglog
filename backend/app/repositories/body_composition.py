"""
Repository for managing body composition in the database.
"""

from math import log10

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.body_composition import BodyComposition
from app.schemas.body_composition import (
    BodyCompositionCreate,
    BodyCompositionRead,
    BodyCompositionUpdate,
)


async def viceral_fat_formula(
    db: AsyncSession, id_user: int, weight: float
) -> float:
    """
    Calculate visceral fat based on weight and fat percentage.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    Args:
        db: The database session to retrieve data needed for the calculation
        id_user: The ID of the user to retrieve measurements for
        weight: The weight of the user to calculate visceral fat for
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
            "User gender must be either 'MALE' or 'FEMALE' for visceral fat "
            "estimation. Please provide true values of body composition to "
            "avoid estimation."
        )

    bmi = weight / (msmnt.height / 100) ** 2
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


async def fat_percentage_formula(
    db: AsyncSession, id_user: int, weight: float
) -> float:
    """
    Calculate fat percentage based on weight and other measurements.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    Args:
        db: The database session to retrieve data needed for the calculation
        id_user: The ID of the user to retrieve measurements for
        weight: The weight of the user to calculate fat percentage for
    Returns:
        The calculated fat percentage as a decimal (e.g., 0.15 for 15%)
    """

    # Mock user and measurement data for the calculation
    class MockMeasurement:
        def __init__(
            self, height: float, waist: float, hip: float, neck: float
        ):
            self.height = height
            self.waist = waist
            self.hip = hip
            self.neck = neck

    class MockUser:
        def __init__(self, id: int, gender: str):
            self.id = id
            self.gender = gender

    msmnt = MockMeasurement(170, 80, 100, 40)
    user = MockUser(id_user, "MALE")

    if user.gender not in ["MALE", "FEMALE"]:
        raise ValueError(
            "User gender must be either 'MALE' or 'FEMALE' for fat percentage "
            "estimation"
        )

    log10height = log10(msmnt.height)

    if user.gender == "MALE":
        log10waistneck = log10(msmnt.waist - msmnt.neck)
        fat_percentage = 86.010 * log10waistneck - 70.041 * log10height + 36.76
    else:
        log10waisthipneck = log10(msmnt.waist + msmnt.hip - msmnt.neck)
        fat_percentage = (
            163.205 * log10waisthipneck - 97.684 * log10height - 78.387
        )

    return max(min(fat_percentage, 1.0), 0.0)


async def water_percentage_formula(
    db: AsyncSession, id_user: int, weight: float
) -> float:
    """
    Calculate water percentage based on Watson formula.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    Args:
        db: The database session to retrieve data needed for the calculation
        id_user: The ID of the user to retrieve measurements for
        weight: The weight of the user to calculate water percentage for
    Returns:
        The calculated water percentage as a decimal (e.g., 0.60 for 60%)
    """

    # Mock user and measurement data for the calculation
    class MockMeasurement:
        def __init__(
            self, height: float, waist: float, hip: float, neck: float
        ):
            self.height = height
            self.waist = waist
            self.hip = hip
            self.neck = neck

    class MockUser:
        def __init__(self, id: int, gender: str, age: int):
            self.id = id
            self.gender = gender
            self.age = age

    mst = MockMeasurement(170, 80, 100, 40)
    usr = MockUser(id_user, "MALE", 30)

    if usr.gender not in ["MALE", "FEMALE"]:
        raise ValueError(
            "User gender must be either 'MALE' or 'FEMALE' for water "
            "percentage estimation"
        )

    if usr.gender == "MALE":
        lit = 2.447 - 0.09156 * usr.age + 0.1074 * mst.height + 0.3362 * weight
    else:
        lit = -2.097 + 0.1069 * mst.height + 0.2466 * weight

    water_perc = lit / weight

    return max(min(water_perc, 1.0), 0.0)


async def bone_percentage_formula(
    db: AsyncSession,
    id_user: int,
    weight: float,
    body_fat_percentage: float = 0.15,
) -> float:
    """
    Calculate[1] bone mineral compositon percentage.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    [1] (https://doi.org/10.1016/j.smhs.2023.09.003)
    > Justin Aflatooni, Steven Martin, Adib Edilbi, Pranav Gadangi,
    > William Singer, Robert Loving, Shreya Domakonda, Nandini Solanki, Patrick
    > C. McCulloch, Bradley Lambert
    >
    > A novel non-invasive method for predicting bone mineral density and
    > fracture risk using demographic and anthropometric measures,
    >
    > Sports Medicine and Health Science,
    > Volume 5, Issue 4,
    > 2023,
    > Pages 308-313,
    > ISSN 2666-3376,

    Args:
        db: The database session to retrieve data needed for the calculation
        id_user: The ID of the user to retrieve measurements for
        weight: The weight of the user to calculate bone percentage for
        body_fat_percentage: The body fat percentage of the user
    Returns:
        The calculated bone mass percentage as a decimal (e.g., 0.05 for 5%)
    """

    # Mock user and measurement data for the calculation
    class MockMeasurement:
        def __init__(
            self,
            height: float,
            shoulder_width: float,
            trunk_length: float,
            pelvis_width: float,
        ):
            self.height = height
            # measured between the widest point of each shoulder
            self.shoulder_width = shoulder_width
            # measured from the top of the widest point on the pelvis (iliac
            # crest) to the vertical level of the bottom of the jaw bone
            self.trunk_length = trunk_length
            # measured between the iliac spines of the pelvis
            self.pelvis_width = pelvis_width

    class MockUser:
        def __init__(self, id: int, gender: str, age: int):
            self.id = id
            self.gender = gender
            self.age = age

    msmnt = MockMeasurement(170, 40, 50, 30)
    user = MockUser(id_user, "MALE", 30)

    # general_estimation = 0.128 * msmnt.height + 0.245 * weight - 2.95
    # lean_mass = weight * (1 - body_fat_percentage)
    # estimation_by_lean_mass = 0.05 * lean_mass

    # if user.gender == "MALE":
    #     estimation_by_gender_1 = 0.055 * weight
    #     estimation_by_gender_2 = 0.0025 * weight * msmnt.height
    # else:
    #     estimation_by_gender_1 = 0.045 * weight
    #     estimation_by_gender_2 = 0.0022 * weight * msmnt.height

    bmc_kg = (
        0.0158 * msmnt.height
        - 0.0024 * user.age
        + 0.1712 * (user.gender == "MALE")
        + 0.0314 * weight * (1 - body_fat_percentage)
        + 0.001 * weight * body_fat_percentage
        + 0.0089 * msmnt.shoulder_width
        - 0.0145 * msmnt.trunk_length
        - 0.0278 * msmnt.pelvis_width
        - 0.507
    )

    bone_perc = bmc_kg / weight

    return max(min(bone_perc, 1.0), 0.0)


async def muscle_percentage_formula(
    db: AsyncSession, id_user: int, weight: float
) -> float:
    """
    Calculate appendicular skeletal muscle mass percentage.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    [1] (https://doi.org/10.1249/01.mss.0000152804.93039.ce)
    > POORTMANS, JACQUES R.1; BOISSEAU, NATHALIE4; MORAINE, JEAN-JACQUES2;
    >   MORENO-REYES, RODRIGO3; GOLDMAN, SERGE3.
    >
    > Estimation of Total-Body Skeletal Muscle Mass in Children and Adolescents.
    >
    > Medicine & Science in Sports & Exercise 37(2):p 316-322, February 2005.

    Args:
        db: The database session to retrieve data needed for the calculation
        id_user: The ID of the user to retrieve measurements for
        weight: The weight of the user to calculate muscle percentage for
    Returns:
        The calculated muscle mass percentage as a decimal (e.g., 0.40 for 40%)
    """

    # Mock user and measurement data for the calculation
    class MockMeasurement:
        def __init__(self):
            self.height = 170
            self.waist = 80
            self.hip = 100
            self.neck = 40
            self.left_arm = 30
            self.right_arm = 30
            self.left_leg = 50
            self.right_leg = 50
            self.left_calf = 35
            self.right_calf = 35

    class MockUser:
        def __init__(self, id: int):
            self.id = id
            self.gender = "MALE"
            self.age = 30

    msmnt = MockMeasurement()
    user = MockUser(id_user)

    poortmans_asm_kg = (
        msmnt.height
        * (
            0.0064 * msmnt.left_arm * msmnt.right_arm
            + 0.0032 * msmnt.left_leg * msmnt.right_leg
            + 0.0015 * msmnt.left_calf * msmnt.right_calf
        )
        + 2.56 * (user.gender == "MALE")
        + 0.136 * user.age
    )

    poortmans_asm_perc = poortmans_asm_kg / weight

    return max(min(poortmans_asm_perc, 1.0), 0.0)


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
            db, id_user, body_composition.weight
        )

    # Estimate fat mass if not provided
    if body_composition.fat_percentage is None:
        body_composition.fat_percentage = await fat_percentage_formula(
            db, id_user, body_composition.weight
        )

    # Estimate water percentage if not provided
    if body_composition.water_percentage is None:
        body_composition.water_percentage = await water_percentage_formula(
            db, id_user, body_composition.weight
        )

    # Estimate bone mass percentage if not provided
    if body_composition.bone_percentage is None:
        body_composition.bone_percentage = await bone_percentage_formula(
            db,
            id_user,
            body_composition.weight,
            body_composition.fat_percentage,
        )

    # Estimate muscle mass percentage if not provided
    if body_composition.muscle_percentage is None:
        body_composition.muscle_percentage = await muscle_percentage_formula(
            db, id_user, body_composition.weight
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
