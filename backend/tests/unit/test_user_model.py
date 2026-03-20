from datetime import date, datetime, timezone

from app.models.user import Gender, User


def test_user_model():
    data = {
        "id": 1,
        "username": "john_doe",
        "email": "john_doe@example.com",
        "password_hash": "securepassword123",
        "date_of_birth": date(1990, 1, 1),
        "gender": Gender.MALE,
        "created_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        "updated_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    }

    user = User(**data)

    assert user.id == data["id"]
    assert user.username == data["username"]
    assert user.email == data["email"]
    assert user.password_hash == data["password_hash"]
    assert user.date_of_birth == data["date_of_birth"]
    assert user.gender == data["gender"]
    assert user.created_at == data["created_at"]
    assert user.updated_at == data["updated_at"]
