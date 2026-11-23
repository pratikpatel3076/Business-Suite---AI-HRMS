"""Shared rate limiter for authentication endpoints.

Kept in its own module so both ``main`` (exception handler / app state) and the
auth router (endpoint decorators) can import the same instance without a
circular import. Rate limiting is disabled in the test environment: the suite
performs hundreds of logins from the same client address.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.ENVIRONMENT.lower() != "test",
)

AUTH_RATE_LIMIT = f"{settings.RATE_LIMIT_PER_MINUTE}/minute"
