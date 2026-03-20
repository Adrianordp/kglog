from datetime import datetime, timezone

from app.models.body_measurements import BodyMeasurements


def test_body_measurement_model():
    data = {
        "id": 1,
        "id_user": 1,
        "measure_date": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
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
    }

    body_measurement = BodyMeasurements(**data)

    assert body_measurement.id == data["id"]
    assert body_measurement.id_user == data["id_user"]
    assert body_measurement.measure_date == data["measure_date"]
    assert body_measurement.height == data["height"]
    assert body_measurement.neck == data["neck"]
    assert body_measurement.neck_to_shoulder == data["neck_to_shoulder"]
    assert body_measurement.sleeve == data["sleeve"]
    assert body_measurement.bust == data["bust"]
    assert body_measurement.left_arm == data["left_arm"]
    assert body_measurement.right_arm == data["right_arm"]
    assert body_measurement.waist == data["waist"]
    assert body_measurement.hip == data["hip"]
    assert body_measurement.inseam_to_ankle == data["inseam_to_ankle"]
    assert body_measurement.left_leg == data["left_leg"]
    assert body_measurement.right_leg == data["right_leg"]
    assert body_measurement.left_calf == data["left_calf"]
    assert body_measurement.right_calf == data["right_calf"]
