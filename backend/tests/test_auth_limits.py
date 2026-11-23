"""Tasks 5 and 6: auth rate limiting and CORS hardening."""

import inspect

from fastapi import FastAPI, Request, status
from fastapi.testclient import TestClient
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.auth import login, refresh_token, verify_mfa_login
from app.core.config import settings
from app.core.rate_limit import limiter


def test_rate_limiting_is_disabled_in_tests():
    assert limiter.enabled is False


def test_auth_routes_declare_rate_limits():
    for endpoint in (login, verify_mfa_login, refresh_token):
        assert "@limiter.limit" in inspect.getsource(endpoint)


def test_rate_limiting_returns_429_when_enabled(monkeypatch):
    monkeypatch.setattr(limiter, "enabled", True)
    limiter.reset()

    app = FastAPI()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.get("/limited")
    @limiter.limit("2/minute")
    def limited(request: Request):
        return {"ok": True}

    with TestClient(app) as client:
        statuses = [client.get("/limited").status_code for _ in range(5)]

    assert statuses == [200, 200, 429, 429, 429]


def test_auth_rate_limit_uses_configured_limit():
    configured = limiter._route_limits["app.api.v1.auth.login"][0].limit
    assert str(configured).startswith(str(settings.RATE_LIMIT_PER_MINUTE))


def test_cors_uses_explicit_methods_and_headers(client):
    response = client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    allow_methods = response.headers["access-control-allow-methods"]
    assert "*" not in allow_methods
    assert "POST" in allow_methods
    allow_headers = response.headers["access-control-allow-headers"]
    assert "*" not in allow_headers
    assert "authorization" in allow_headers.lower()


def test_cors_rejects_unlisted_method(client):
    response = client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "TRACE",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
