from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def create_qr_token(event_id: int, expires_minutes: int | None = None) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes or settings.qr_token_expire_minutes
    )
    payload: dict[str, Any] = {
        "event_id": event_id,
        "exp": expire,
        "type": "qr",
    }
    return jwt.encode(payload, settings.qr_secret_key, algorithm=settings.qr_algorithm)


def decode_qr_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.qr_secret_key, algorithms=[settings.qr_algorithm])


def is_jwt_error(exc: Exception) -> bool:
    return isinstance(exc, JWTError)
