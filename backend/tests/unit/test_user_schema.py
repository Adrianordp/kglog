from datetime import datetime

from app.schemas.user import Gender, UserCreate, UserRead, UserUpdate


def test_user_create():
    data = {
        "username": "john_doe",
        "email": "john_doe@example.com",
        "password": "123456",
        "date_of_birth": "1990-01-01",
        "gender": "MALE",
    }

    user_create = UserCreate(**data)

    assert user_create.username == data["username"]
    assert user_create.email == data["email"]
    assert user_create.password == data["password"]
    assert (
        user_create.date_of_birth
        == datetime.fromisoformat(data["date_of_birth"]).date()
    )
    assert user_create.gender == Gender.MALE


def test_user_read():
    data = {
        "id": 1,
        "username": "john_doe",
        "email": "john_doe@example.com",
        "date_of_birth": "1990-01-01",
        "gender": "MALE",
        "created_at": "2024-01-01T00:00:00+00:00",
        "updated_at": "2024-01-01T00:00:00+00:00",
    }

    user_read = UserRead(**data)

    assert user_read.id == data["id"]
    assert user_read.username == data["username"]
    assert user_read.email == data["email"]
    assert (
        user_read.date_of_birth
        == datetime.fromisoformat(data["date_of_birth"]).date()
    )
    assert user_read.gender == Gender.MALE
    assert user_read.created_at == datetime.fromisoformat(data["created_at"])
    assert user_read.updated_at == datetime.fromisoformat(data["updated_at"])


def test_user_update():
    data = {
        "username": "john_doe_updated",
        "email": "john_doe_updated@example.com",
        "password": "654321",
        "date_of_birth": "1990-01-01",
        "gender": "MALE",
    }

    user_update = UserUpdate(**data)

    assert user_update.username == data["username"]
    assert user_update.email == data["email"]
    assert user_update.password == data["password"]
    assert (
        user_update.date_of_birth
        == datetime.fromisoformat(data["date_of_birth"]).date()
    )
    assert user_update.gender == Gender.MALE


def test_user_create_invalid_email():
    data = {
        "username": "john_doe",
        "email": "invalid_email",
        "password": "123456",
        "date_of_birth": "1990-01-01",
        "gender": "MALE",
    }

    try:
        UserCreate(**data)
        assert False, "Expected ValueError for invalid email"
    except ValueError as e:
        assert "value is not a valid email address" in str(e)


def test_user_update_invalid_email():
    data = {
        "email": "invalid_email",
    }

    try:
        UserUpdate(**data)
        assert False, "Expected ValueError for invalid email"
    except ValueError as e:
        assert "value is not a valid email address" in str(e)


def test_user_create_invalid_gender():
    data = {
        "username": "john_doe_updated",
        "email": "john_doe_updated@example.com",
        "password": "123456",
        "date_of_birth": "1990-01-01",
        "gender": "INVALID_GENDER",
    }

    try:
        UserCreate(**data)
        assert False, "Expected ValueError for invalid gender"
    except ValueError as e:
        assert "Input should be 'MALE', 'FEMALE' or 'OTHER'" in str(e)


def test_user_update_invalid_gender():
    data = {
        "gender": "INVALID_GENDER",
    }

    try:
        UserUpdate(**data)
        assert False, "Expected ValueError for invalid gender"
    except ValueError as e:
        assert "Input should be 'MALE', 'FEMALE' or 'OTHER'" in str(e)


def test_user_create_invalid_date_of_birth():
    data = {
        "username": "john_doe_updated",
        "email": "john_doe_updated@example.com",
        "password": "123456",
        "date_of_birth": "invalid_date",
        "gender": "MALE",
    }

    try:
        UserCreate(**data)
        assert False, "Expected ValueError for invalid date format"
    except ValueError as e:
        assert "Input should be a valid date" in str(e)


def test_user_update_invalid_date_of_birth():
    data = {
        "date_of_birth": "invalid_date",
    }

    try:
        UserUpdate(**data)
        assert False, "Expected ValueError for invalid date format"
    except ValueError as e:
        assert "Input should be a valid date" in str(e)


def test_user_create_invalid_password():
    data = {
        "username": "john_doe",
        "email": "john_doe@example.com",
        "password": "12345",  # Invalid password (too short)
        "date_of_birth": "1990-01-01",
        "gender": "MALE",
    }

    try:
        UserCreate(**data)
        assert False, "Expected ValueError for invalid password"
    except ValueError as e:
        assert "String should have at least 6 characters" in str(e)


def test_user_update_invalid_password():
    data = {
        "password": "12345",  # Invalid password (too short)
    }

    try:
        UserUpdate(**data)
        assert False, "Expected ValueError for invalid password"
    except ValueError as e:
        assert "String should have at least 6 characters" in str(e)
