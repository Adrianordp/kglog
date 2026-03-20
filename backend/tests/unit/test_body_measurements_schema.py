from datetime import datetime

from app.schemas.body_measurements import (
    BodyMeasurementCreate,
    BodyMeasurementRead,
    BodyMeasurementUpdate,
)


def test_body_measurement_create():
    data = {
        "measure_date": "2024-01-01T00:00:00+00:00",
        "height": 180.0,
        "neck": 40.0,
        "neck_to_shoulder": 50.0,
        "sleeve": 60.0,
        "bust": 100.0,
        "left_arm": 30.0,
        "right_arm": 30.0,
        "waist": 80.0,
        "hip": 90.0,
        "inseam_to_ankle": 70.0,
        "left_leg": 50.0,
        "right_leg": 50.0,
        "left_calf": 35.0,
        "right_calf": 35.0,
        "shoulders": 50.0,
        "trunk": 60.0,
        "pelvis": 40.0,
    }

    body_measurement_create = BodyMeasurementCreate(**data)

    assert body_measurement_create.measure_date == datetime.fromisoformat(
        data["measure_date"]
    )
    assert body_measurement_create.height == data["height"]
    assert body_measurement_create.neck == data["neck"]
    assert body_measurement_create.neck_to_shoulder == data["neck_to_shoulder"]
    assert body_measurement_create.sleeve == data["sleeve"]
    assert body_measurement_create.bust == data["bust"]
    assert body_measurement_create.left_arm == data["left_arm"]
    assert body_measurement_create.right_arm == data["right_arm"]
    assert body_measurement_create.waist == data["waist"]
    assert body_measurement_create.hip == data["hip"]
    assert body_measurement_create.inseam_to_ankle == data["inseam_to_ankle"]
    assert body_measurement_create.left_leg == data["left_leg"]
    assert body_measurement_create.right_leg == data["right_leg"]
    assert body_measurement_create.left_calf == data["left_calf"]
    assert body_measurement_create.right_calf == data["right_calf"]
    assert body_measurement_create.shoulders == data["shoulders"]
    assert body_measurement_create.trunk == data["trunk"]
    assert body_measurement_create.pelvis == data["pelvis"]


def test_body_measurement_read():
    data = {
        "id": 1,
        "id_user": 1,
        "measure_date": "2024-01-01T00:00:00+00:00",
        "height": 180.0,
        "neck": 40.0,
        "neck_to_shoulder": 50.0,
        "sleeve": 60.0,
        "bust": 100.0,
        "left_arm": 30.0,
        "right_arm": 30.0,
        "waist": 80.0,
        "hip": 90.0,
        "inseam_to_ankle": 70.0,
        "left_leg": 50.0,
        "right_leg": 50.0,
        "left_calf": 35.0,
        "right_calf": 35.0,
        "shoulders": 50.0,
        "trunk": 60.0,
        "pelvis": 40.0,
    }

    body_measurement_read = BodyMeasurementRead(**data)

    assert body_measurement_read.id == data["id"]
    assert body_measurement_read.id_user == data["id_user"]
    assert body_measurement_read.measure_date == datetime.fromisoformat(
        data["measure_date"]
    )
    assert body_measurement_read.height == data["height"]
    assert body_measurement_read.neck == data["neck"]
    assert body_measurement_read.neck_to_shoulder == data["neck_to_shoulder"]
    assert body_measurement_read.sleeve == data["sleeve"]
    assert body_measurement_read.bust == data["bust"]
    assert body_measurement_read.left_arm == data["left_arm"]
    assert body_measurement_read.right_arm == data["right_arm"]
    assert body_measurement_read.waist == data["waist"]
    assert body_measurement_read.hip == data["hip"]
    assert body_measurement_read.inseam_to_ankle == data["inseam_to_ankle"]
    assert body_measurement_read.left_leg == data["left_leg"]
    assert body_measurement_read.right_leg == data["right_leg"]
    assert body_measurement_read.left_calf == data["left_calf"]
    assert body_measurement_read.right_calf == data["right_calf"]
    assert body_measurement_read.shoulders == data["shoulders"]
    assert body_measurement_read.trunk == data["trunk"]
    assert body_measurement_read.pelvis == data["pelvis"]


def test_body_measurement_update():
    data = {
        "measure_date": "2024-01-02T00:00:00+00:00",
        "height": 181.0,
        "neck": 41.0,
        "neck_to_shoulder": 51.0,
        "sleeve": 61.0,
        "bust": 101.0,
        "left_arm": 31.0,
        "right_arm": 31.0,
        "waist": 81.0,
        "hip": 91.0,
        "inseam_to_ankle": 71.0,
        "left_leg": 51.0,
        "right_leg": 51.0,
        "left_calf": 36.0,
        "right_calf": 36.0,
        "shoulders": 51.0,
        "trunk": 61.0,
        "pelvis": 41.0,
    }

    body_measurement_update = BodyMeasurementUpdate(**data)

    assert body_measurement_update.measure_date == datetime.fromisoformat(
        data["measure_date"]
    )
    assert body_measurement_update.height == data["height"]
    assert body_measurement_update.neck == data["neck"]
    assert body_measurement_update.neck_to_shoulder == data["neck_to_shoulder"]
    assert body_measurement_update.sleeve == data["sleeve"]
    assert body_measurement_update.bust == data["bust"]
    assert body_measurement_update.left_arm == data["left_arm"]
    assert body_measurement_update.right_arm == data["right_arm"]
    assert body_measurement_update.waist == data["waist"]
    assert body_measurement_update.hip == data["hip"]
    assert body_measurement_update.inseam_to_ankle == data["inseam_to_ankle"]
    assert body_measurement_update.left_leg == data["left_leg"]
    assert body_measurement_update.right_leg == data["right_leg"]
    assert body_measurement_update.left_calf == data["left_calf"]
    assert body_measurement_update.right_calf == data["right_calf"]
    assert body_measurement_update.shoulders == data["shoulders"]
    assert body_measurement_update.trunk == data["trunk"]
    assert body_measurement_update.pelvis == data["pelvis"]


def test_body_measurement_create_invalid_measure_date():
    data = {
        "measure_date": "invalid_date",
        "height": 180.0,
        "neck": 40.0,
        "neck_to_shoulder": 50.0,
        "sleeve": 60.0,
        "bust": 100.0,
        "left_arm": 30.0,
        "right_arm": 30.0,
        "waist": 80.0,
        "hip": 90.0,
        "inseam_to_ankle": 70.0,
        "left_leg": 50.0,
        "right_leg": 50.0,
        "left_calf": 35.0,
        "right_calf": 35.0,
        "shoulders": 50.0,
        "trunk": 60.0,
        "pelvis": 40.0,
    }

    try:
        BodyMeasurementCreate(**data)
        assert False, "Expected ValueError for invalid date format"
    except ValueError as e:
        assert "Input should be a valid date" in str(e)


def test_body_measurement_update_invalid_measure_date():
    data = {
        "measure_date": "invalid_date",
    }

    try:
        BodyMeasurementUpdate(**data)
        assert False, "Expected ValueError for invalid date format"
    except ValueError as e:
        assert "Input should be a valid date" in str(e)


def test_body_measurement_create_invalid_height():
    data = {
        "measure_date": "2024-01-01T00:00:00+00:00",
        "height": -180.0,  # Invalid height
        "neck": -40.0,
        "neck_to_shoulder": -50.0,
        "sleeve": -60.0,
        "bust": -100.0,
        "left_arm": -30.0,
        "right_arm": -30.0,
        "waist": -80.0,
        "hip": -90.0,
        "inseam_to_ankle": -70.0,
        "left_leg": -50.0,
        "right_leg": -50.0,
        "left_calf": -35.0,
        "right_calf": -35.0,
        "shoulders": -50.0,
        "trunk": -60.0,
        "pelvis": -40.0,
    }

    try:
        BodyMeasurementCreate(**data)
        assert False, "Expected ValueError for invalid height"
    except ValueError as e:
        assert str(e).count("Input should be greater than 0") == 17


def test_body_measurement_update_invalid_height():
    data = {
        "height": -180.0,  # Invalid height
        "neck": -40.0,
        "neck_to_shoulder": -50.0,
        "sleeve": -60.0,
        "bust": -100.0,
        "left_arm": -30.0,
        "right_arm": -30.0,
        "waist": -80.0,
        "hip": -90.0,
        "inseam_to_ankle": -70.0,
        "left_leg": -50.0,
        "right_leg": -50.0,
        "left_calf": -35.0,
        "right_calf": -35.0,
        "shoulders": -50.0,
        "trunk": -60.0,
        "pelvis": -40.0,
    }

    try:
        BodyMeasurementUpdate(**data)
        assert False, "Expected ValueError for invalid height"
    except ValueError as e:
        assert str(e).count("Input should be greater than 0") == 17
