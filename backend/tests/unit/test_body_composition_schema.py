from datetime import datetime

from app.schemas.body_composition import (
    BodyCompositionCreate,
    BodyCompositionRead,
    BodyCompositionUpdate,
)


def test_body_composition_create():
    data = {
        "id_user": 1,
        "id_measurements": 1,
        "measure_date": "2024-01-01T00:00:00+00:00",
        "weight": 70.0,
        "fat_percentage": 0.15,
        "muscle_percentage": 0.40,
        "bone_percentage": 0.05,
        "water_percentage": 0.60,
        "visceral_fat": 100.0,
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    body_composition_create = BodyCompositionCreate(**data)

    assert body_composition_create.id_user == data["id_user"]
    assert body_composition_create.id_measurements == data["id_measurements"]
    assert body_composition_create.measure_date == datetime.fromisoformat(
        data["measure_date"]
    )
    assert body_composition_create.weight == data["weight"]
    assert body_composition_create.fat_percentage == data["fat_percentage"]
    assert (
        body_composition_create.muscle_percentage == data["muscle_percentage"]
    )
    assert body_composition_create.bone_percentage == data["bone_percentage"]
    assert body_composition_create.water_percentage == data["water_percentage"]
    assert body_composition_create.visceral_fat == data["visceral_fat"]
    assert body_composition_create.is_fat_estimated == data["is_fat_estimated"]
    assert (
        body_composition_create.is_muscle_estimated
        == data["is_muscle_estimated"]
    )
    assert (
        body_composition_create.is_bone_estimated == data["is_bone_estimated"]
    )
    assert (
        body_composition_create.is_water_estimated == data["is_water_estimated"]
    )
    assert (
        body_composition_create.is_visceral_fat_estimated
        == data["is_visceral_fat_estimated"]
    )


def test_body_composition_read():
    data = {
        "id": 1,
        "id_user": 1,
        "measure_date": "2024-01-01T00:00:00+00:00",
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

    body_composition_read = BodyCompositionRead(**data)

    assert body_composition_read.id == data["id"]
    assert body_composition_read.id_user == data["id_user"]
    assert body_composition_read.measure_date == datetime.fromisoformat(
        data["measure_date"]
    )
    assert body_composition_read.weight == data["weight"]
    assert body_composition_read.fat_percentage == data["fat_percentage"]
    assert body_composition_read.muscle_percentage == data["muscle_percentage"]
    assert body_composition_read.bone_percentage == data["bone_percentage"]
    assert body_composition_read.water_percentage == data["water_percentage"]
    assert body_composition_read.fat_kg == data["fat_kg"]
    assert body_composition_read.muscle_kg == data["muscle_kg"]
    assert body_composition_read.bone_kg == data["bone_kg"]
    assert body_composition_read.water_kg == data["water_kg"]
    assert body_composition_read.visceral_fat == data["visceral_fat"]
    assert body_composition_read.is_fat_estimated == data["is_fat_estimated"]
    assert (
        body_composition_read.is_muscle_estimated == data["is_muscle_estimated"]
    )
    assert body_composition_read.is_bone_estimated == data["is_bone_estimated"]
    assert (
        body_composition_read.is_water_estimated == data["is_water_estimated"]
    )
    assert (
        body_composition_read.is_visceral_fat_estimated
        == data["is_visceral_fat_estimated"]
    )


def test_body_composition_update():
    data = {
        "measure_date": "2024-01-02T00:00:00+00:00",
        "weight": 71.0,
        "fat_percentage": 0.14,
        "muscle_percentage": 0.41,
        "bone_percentage": 0.06,
        "water_percentage": 0.61,
        "visceral_fat": 9.0,
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    body_composition_update = BodyCompositionUpdate(**data)

    assert body_composition_update.measure_date == datetime.fromisoformat(
        data["measure_date"]
    )
    assert body_composition_update.weight == data["weight"]
    assert body_composition_update.fat_percentage == data["fat_percentage"]
    assert (
        body_composition_update.muscle_percentage == data["muscle_percentage"]
    )
    assert body_composition_update.bone_percentage == data["bone_percentage"]
    assert body_composition_update.water_percentage == data["water_percentage"]
    assert body_composition_update.visceral_fat == data["visceral_fat"]
    assert body_composition_update.is_fat_estimated == data["is_fat_estimated"]
    assert (
        body_composition_update.is_muscle_estimated
        == data["is_muscle_estimated"]
    )
    assert (
        body_composition_update.is_bone_estimated == data["is_bone_estimated"]
    )
    assert (
        body_composition_update.is_water_estimated == data["is_water_estimated"]
    )
    assert (
        body_composition_update.is_visceral_fat_estimated
        == data["is_visceral_fat_estimated"]
    )


def test_body_composition_create_invalid_measure_date():
    data = {
        "measure_date": "invalid_date",
        "weight": 70.0,
        "fat_percentage": 0.15,
        "muscle_percentage": 0.40,
        "bone_percentage": 0.05,
        "water_percentage": 0.60,
        "visceral_fat": 100.0,
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    try:
        BodyCompositionCreate(**data)
        assert False, "Expected ValueError for invalid measure_date"
    except ValueError as e:
        assert "Input should be a valid date" in str(e)


def test_body_composition_update_invalid_measure_date():
    data = {
        "measure_date": "invalid_date",
    }

    try:
        BodyCompositionUpdate(**data)
        assert False, "Expected ValueError for invalid measure_date"
    except ValueError as e:
        assert "Input should be a valid date" in str(e)


def test_body_composition_create_invalid_high_percentage():
    data = {
        "measure_date": "2024-01-01T00:00:00+00:00",
        "weight": 70.0,
        "fat_percentage": 1,  # Invalid percentage
        "muscle_percentage": 1,  # Invalid percentage
        "bone_percentage": 1,  # Invalid percentage
        "water_percentage": 1,  # Invalid percentage
        "visceral_fat": 100.0,
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    try:
        BodyCompositionCreate(**data)
        assert False, "Expected ValueError for invalid fat_percentage"
    except ValueError as e:
        assert str(e).count("Input should be less than 1") == 4


def test_body_composition_update_invalid_high_percentage():
    data = {
        "fat_percentage": 1,  # Invalid percentage
        "muscle_percentage": 1,  # Invalid percentage
        "bone_percentage": 1,  # Invalid percentage
        "water_percentage": 1,  # Invalid percentage
    }

    try:
        BodyCompositionUpdate(**data)
        assert False, "Expected ValueError for invalid fat_percentage"
    except ValueError as e:
        assert str(e).count("Input should be less than 1") == 4


def test_body_composition_create_invalid_low_percentage():
    data = {
        "measure_date": "2024-01-01T00:00:00+00:00",
        "weight": 70.0,
        "fat_percentage": 0,  # Invalid percentage
        "muscle_percentage": 0,  # Invalid percentage
        "bone_percentage": 0,  # Invalid percentage
        "water_percentage": 0,  # Invalid percentage
        "visceral_fat": 100.0,
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    try:
        BodyCompositionCreate(**data)
        assert False, "Expected ValueError for invalid fat_percentage"
    except ValueError as e:
        assert str(e).count("Input should be greater than 0") == 4


def test_body_composition_update_invalid_low_percentage():
    data = {
        "fat_percentage": 0,  # Invalid percentage
        "muscle_percentage": 0,  # Invalid percentage
        "bone_percentage": 0,  # Invalid percentage
        "water_percentage": 0,  # Invalid percentage
    }

    try:
        BodyCompositionUpdate(**data)
        assert False, "Expected ValueError for invalid fat_percentage"
    except ValueError as e:
        assert str(e).count("Input should be greater than 0") == 4


def test_body_composition_create_invalid_weight():
    data = {
        "measure_date": "2024-01-01T00:00:00+00:00",
        "weight": -1,  # Invalid weight
        "fat_percentage": 0.15,
        "muscle_percentage": 0.40,
        "bone_percentage": 0.05,
        "water_percentage": 0.60,
        "visceral_fat": 100.0,
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    try:
        BodyCompositionCreate(**data)
        assert False, "Expected ValueError for invalid weight"
    except ValueError as e:
        assert "Input should be greater than 0" in str(e)


def test_body_composition_update_invalid_weight():
    data = {
        "weight": -1,  # Invalid weight
    }

    try:
        BodyCompositionUpdate(**data)
        assert False, "Expected ValueError for invalid weight"
    except ValueError as e:
        assert "Input should be greater than 0" in str(e)


def test_body_composition_create_invalid_visceral_fat():
    data = {
        "measure_date": "2024-01-01T00:00:00+00:00",
        "weight": 70.0,
        "fat_percentage": 0.15,
        "muscle_percentage": 0.40,
        "bone_percentage": 0.05,
        "water_percentage": 0.60,
        "visceral_fat": -0.001,  # Invalid visceral fat
        "is_fat_estimated": True,
        "is_muscle_estimated": True,
        "is_bone_estimated": True,
        "is_water_estimated": True,
        "is_visceral_fat_estimated": True,
    }

    try:
        BodyCompositionCreate(**data)
        assert False, "Expected ValueError for invalid visceral_fat"
    except ValueError as e:
        assert "Input should be greater than or equal to 0" in str(e)


def test_body_composition_update_invalid_visceral_fat():
    data = {
        "visceral_fat": -0.001,  # Invalid visceral fat
    }

    try:
        BodyCompositionUpdate(**data)
        assert False, "Expected ValueError for invalid visceral_fat"
    except ValueError as e:
        assert "Input should be greater than or equal to 0" in str(e)
