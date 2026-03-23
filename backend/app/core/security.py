from datetime import UTC, datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.settings import settings

EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    passwd_encoded = password.encode("utf-8")
    hashed_encoded = hashed_password.encode("utf-8")

    return bcrypt.checkpw(passwd_encoded, hashed_encoded)


def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    passwd_encoded = password.encode("utf-8")

    return bcrypt.hashpw(passwd_encoded, salt).decode("utf-8")


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token.

    Args:
        data: The data to include in the token payload.
        expires_delta: The time duration for which the token is valid.

    Returns:
        str: The generated JWT access token.
    """
    to_encode = data.copy()

    expires_delta = expires_delta or timedelta(minutes=EXPIRE_MINUTES)
    expire = datetime.now(UTC) + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode a JWT access token.

    Args:
        token: The JWT access token to decode.

    Returns:
        dict: The decoded token payload if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except JWTError:
        return None
