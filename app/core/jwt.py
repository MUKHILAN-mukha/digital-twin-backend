from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


def create_access_token(data: dict, expires_minutes: int | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
