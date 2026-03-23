from datetime import datetime, timezone

from app.models.body_composition import BodyComposition


def test_body_composition_model():
    data = {
        "id": 1,
        "id_user": 1,
        "measure_date": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "weight": 70.0,
        "fat_percentage": 0.15,
        "fat_kg": 10.5,
        "muscle_percentage": 0.40,
        "muscle_kg": 28.0,
        "bone_percentage": 0.05,
        "bone_kg": 3.5,
        "water_percentage": 0.60,
        "water_kg": 42.0,
        "visceral_fat": 10.0,
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    body_composition = BodyComposition(**data)

    assert body_composition.id == data["id"]
    assert body_composition.id_user == data["id_user"]
    assert body_composition.measure_date == data["measure_date"]
    assert body_composition.weight == data["weight"]
    assert body_composition.fat_percentage == data["fat_percentage"]
    assert body_composition.fat_kg == data["fat_kg"]
    assert body_composition.muscle_percentage == data["muscle_percentage"]
    assert body_composition.muscle_kg == data["muscle_kg"]
    assert body_composition.bone_percentage == data["bone_percentage"]
    assert body_composition.bone_kg == data["bone_kg"]
    assert body_composition.water_percentage == data["water_percentage"]
    assert body_composition.water_kg == data["water_kg"]
    assert body_composition.visceral_fat == data["visceral_fat"]
    assert body_composition.is_fat_estimated == data["is_fat_estimated"]
    assert body_composition.is_muscle_estimated == data["is_muscle_estimated"]
    assert body_composition.is_bone_estimated == data["is_bone_estimated"]
    assert body_composition.is_water_estimated == data["is_water_estimated"]
    assert (
        body_composition.is_visceral_fat_estimated
        == data["is_visceral_fat_estimated"]
    )
