"""
Repository for managing body composition in the database.
"""

from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.body_composition import BodyComposition
from app.models.body_measurements import BodyMeasurements
from app.models.user import User
from app.repositories.body_measurements import (
    get_body_measurement_by_id,
)
from app.repositories.user import get_user_by_id
from app.schemas.body_composition import (
    BodyCompositionCreate,
    BodyCompositionRead,
    BodyCompositionUpdate,
)


async def calculate_age(date_of_birth: date, measure_date: datetime) -> int:
    """
    Calculate age based on date of birth and measurement date.

    Args:
        date_of_birth: The user's date of birth
        measure_date: The date when the measurements were taken
    Returns:
        The calculated age in years
    """
    age = measure_date.year - date_of_birth.year

    if (measure_date.month, measure_date.day) < (
        date_of_birth.month,
        date_of_birth.day,
    ):
        age -= 1

    return age


async def viceral_fat_formula(
    user: User,
    msmnt: BodyMeasurements,
    age: int,
) -> float:
    """
    Calculate visceral fat area (VFA).

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    [1](https://doi.org/10.3389/fendo.2022.916124)
    > Liu H, Yang D, Li S, Xiao Y, Tu Y, Peng D, Bao Y, Han J and Yu H
    > A Reliable Estimate of Visceral Fat Area From Simple Anthropometric
    > Measurements in Chinese Overweight and Obese Individuals.
    >
    > Front.
    > Endocrinol.
    > 13:916124.
    > 2022

    Args:
        user: The user object containing necessary information for the calculation
        msmnt: The body measurements object containing necessary measurements
        age: The age of the user at the time of measurement
    Returns:
        The calculated visceral fat area (VFA) in cm²
    """

    if user.gender not in ["MALE", "FEMALE"]:
        raise ValueError("Gender must be 'MALE' or 'FEMALE' for estimation.")

    if user.gender == "MALE":
        vfa_liu = 3.7 * age + 2.4 * msmnt.waist + 5.5 * msmnt.neck - 443.6
    else:
        vfa_liu = 2.8 * age + 1.7 * msmnt.waist + 6.5 * msmnt.neck - 367.3

    return max(vfa_liu, 0)


async def fat_percentage_formula(user: User, msmnt: BodyMeasurements) -> float:
    """
    Calculate fat percentage based on weight and other measurements.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    [1](https://doi.org/10.1038/s41598-018-29362-1)
    > Woolcott, Orison O. and Bergman, Richard N.
    >
    > Relative fat mass (RFM) as a new estimator of whole-body fat percentage ─
    > A cross-sectional study in American adult individuals
    >
    > Scientific Reports
    > 2018

    Args:
        user: The user object containing necessary information for the calculation
        msmnt: The body measurements object containing necessary measurements
    Returns:
        The calculated fat percentage as a decimal (e.g., 0.15 for 15%)
    """

    if user.gender not in ["MALE", "FEMALE"]:
        raise ValueError("Gender must be 'MALE' or 'FEMALE' for estimation.")

    if user.gender == "MALE":
        bf_woolcott = 76 - 20 * (msmnt.height / msmnt.waist)
    else:
        bf_woolcott = 64 - 20 * (msmnt.height / msmnt.waist)

    return max(min(bf_woolcott, 1.0), 0.0)


async def water_percentage_formula(
    user: User, msmnt: BodyMeasurements, age: int, weight: float
) -> float:
    """
    Calculate water percentage based on Watson formula.

    This implementation mocks the necessary user and measurement data for the
    calculation. In a real implementation, data would be retrieved from the
    database.

    > [1](https://doi.org/10.1093/ajcn/33.1.27)
    > Watson PE, Watson ID, Batt RD
    >
    > Total body water volumes for adult males and females estimated from simple anthropometric measurements.
    >
    > Am J Clin Nutrition
    > 1980

    Args:
        user: The user object containing necessary information for the calculation
        msmnt: The body measurements object containing necessary measurements
        age: The age of the user at the time of measurement
        weight: The weight of the user to calculate water percentage for
    Returns:
        The calculated water percentage as a decimal (e.g., 0.60 for 60%)
    """

    if user.gender not in ["MALE", "FEMALE"]:
        raise ValueError("Gender must be 'MALE' or 'FEMALE' for estimation.")

    if user.gender == "MALE":
        water_watson = (
            2.447 - 0.09156 * age + 0.1074 * msmnt.height + 0.3362 * weight
        )
    else:
        water_watson = -2.097 + 0.1069 * msmnt.height + 0.2466 * weight

    water_perc = water_watson / weight

    return max(min(water_perc, 1.0), 0.0)


async def bone_percentage_formula(
    user: User,
    msmnt: BodyMeasurements,
    age: int,
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
        user: The user object containing necessary information for the calculation
        msmnt: The body measurements object containing necessary measurements
        age: The age of the user at the time of measurement
        weight: The weight of the user to calculate bone percentage for
        body_fat_percentage: The body fat percentage of the user
    Returns:
        The calculated bone mass percentage as a decimal (e.g., 0.05 for 5%)
    """

    if user.gender not in ["MALE", "FEMALE"]:
        raise ValueError("Gender must be 'MALE' or 'FEMALE' for estimation.")

    bmc_kg_aflatooni = (
        0.0158 * msmnt.height
        - 0.0024 * age
        + 0.1712 * (user.gender == "MALE")
        + 0.0314 * weight * (1 - body_fat_percentage)
        + 0.001 * weight * body_fat_percentage
        + 0.0089 * msmnt.shoulders
        - 0.0145 * msmnt.trunk
        - 0.0278 * msmnt.pelvis
        - 0.507
    )

    bone_perc = bmc_kg_aflatooni / weight

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

    if user.gender not in ["MALE", "FEMALE"]:
        raise ValueError("Gender must be 'MALE' or 'FEMALE' for estimation.")

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
    body_composition.is_bone_estimated = False
    body_composition.is_fat_estimated = False
    body_composition.is_muscle_estimated = False
    body_composition.is_visceral_fat_estimated = False
    body_composition.is_water_estimated = False

    # Collect measurements for estimation if provided
    if body_composition.id_measurements is not None:
        measurement_record = await get_body_measurement_by_id(
            db, body_composition.id_measurements
        )

        if measurement_record is None:
            raise ValueError(
                f"Measurements with ID {body_composition.id_measurements} not found"
            )

        # Collect user information for estimation
        user_record = await get_user_by_id(db, id_user)

        age = await calculate_age(
            user_record.date_of_birth, measurement_record.measure_date
        )

        if body_composition.visceral_fat is None:
            body_composition.visceral_fat = await viceral_fat_formula(
                user_record,
                measurement_record,
                body_composition.weight,
                age,
            )
            body_composition.is_visceral_fat_estimated = True

        if body_composition.fat_percentage is None:
            body_composition.fat_percentage = await fat_percentage_formula(
                user_record, measurement_record
            )
            body_composition.is_fat_estimated = True

        if body_composition.water_percentage is None:
            body_composition.water_percentage = await water_percentage_formula(
                user_record, measurement_record, age, body_composition.weight
            )
            body_composition.is_water_estimated = True

        if body_composition.bone_percentage is None:
            body_composition.bone_percentage = await bone_percentage_formula(
                user_record,
                measurement_record,
                age,
                body_composition.weight,
                body_composition.fat_percentage,
            )
            body_composition.is_bone_estimated = True

    if body_composition.muscle_percentage is None:
        body_composition.muscle_percentage = await muscle_percentage_formula(
            db, id_user, body_composition.weight
        )
        body_composition.is_muscle_estimated = True

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
