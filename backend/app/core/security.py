import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    session_id: Optional[str] = None,
) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    if session_id:
        to_encode["sid"] = session_id
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: Union[str, Any], session_id: Optional[str] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    session_id = session_id or str(uuid.uuid4())
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "jti": session_id,
        "sid": session_id,
    }
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, secret_key: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.ALGORITHM],
            options={"require_exp": True},
        )
        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> Optional[dict]:
    for secret_key in [settings.SECRET_KEY, settings.SECRET_KEY_PREVIOUS]:
        if not secret_key:
            continue
        payload = verify_token(token, secret_key)
        if payload and payload.get("type") == "access":
            return payload
    return None


def verify_refresh_token(token: str) -> Optional[dict]:
    for secret_key in [settings.REFRESH_SECRET_KEY, settings.REFRESH_SECRET_KEY_PREVIOUS]:
        if not secret_key:
            continue
        payload = verify_token(token, secret_key)
        if payload and payload.get("type") == "refresh" and payload.get("jti"):
            return payload
    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
