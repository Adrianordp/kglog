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
