"""Shared rate limiter for authentication endpoints.

Limits are stored in Redis via ``REDIS_URL``. Only local development may fall
back to in-memory storage when Redis is unavailable; test and production fail
closed. Rate limiting is disabled in the test environment because the suite
performs hundreds of logins from the same client address.

Login and MFA verification are limited both per source IP and per account
(email for login, MFA token subject for verification) so credential-stuffing
from many addresses against one account is also throttled.
"""

import json
from typing import Any

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.security import verify_token

LOGIN_RATE_LIMIT = "5/minute"
MFA_RATE_LIMIT = "5/minute"
REFRESH_RATE_LIMIT = "30/minute"


def in_memory_fallback_enabled() -> bool:
    """Only local development tolerates losing Redis counters on restart."""
    return settings.ENVIRONMENT.lower() == "development"


def _request_body(request: Request) -> dict[str, Any]:
    """FastAPI has already parsed the body when the limiter key function runs."""
    body = getattr(request, "_body", b"") or b""
    try:
        parsed = json.loads(body)
    except (TypeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def get_email_key(request: Request) -> str:
    email = str(_request_body(request).get("email") or "").strip().lower()
    return f"email:{email or 'unknown'}"


def get_mfa_subject_key(request: Request) -> str:
    token = str(_request_body(request).get("mfa_token") or "")
    payload = verify_token(token, settings.SECRET_KEY) if token else None
    subject = str(payload.get("sub") or "") if payload else ""
    return f"mfa-user:{subject or 'unknown'}"


limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.ENVIRONMENT.lower() != "test",
    storage_uri=settings.REDIS_URL,
    # Redis is mandatory in production; memory is a development-only fallback.
    in_memory_fallback_enabled=in_memory_fallback_enabled(),
)
