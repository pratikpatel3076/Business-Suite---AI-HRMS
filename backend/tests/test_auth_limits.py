"""Task 5/6: auth rate limiting, Redis storage, and CORS hardening."""

import inspect
import json
from types import SimpleNamespace

from fastapi import FastAPI, Request, status
from fastapi.testclient import TestClient
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request as StarletteRequest

from app.api.v1.auth import _create_mfa_token, login, refresh_token, verify_mfa_login
from app.core.config import settings
from app.core.rate_limit import (
    LOGIN_RATE_LIMIT,
    MFA_RATE_LIMIT,
    REFRESH_RATE_LIMIT,
    get_email_key,
    get_mfa_subject_key,
    in_memory_fallback_enabled,
    limiter,
)


def _request_with_body(body: dict) -> StarletteRequest:
    request = StarletteRequest(
        {
            "type": "http",
            "method": "POST",
            "path": "/auth/login",
            "headers": [],
            "query_string": b"",
            "client": ("203.0.113.7", 50000),
        }
    )
    request._body = json.dumps(body).encode("utf-8")
    return request


def _memory_limiter() -> Limiter:
    """Isolated limiter so behavioral tests never touch the configured Redis."""
    return Limiter(key_func=get_remote_address, storage_uri="memory://", enabled=True)


def test_rate_limiting_is_disabled_in_tests():
    assert limiter.enabled is False


def test_rate_limit_constants_are_fixed():
    assert LOGIN_RATE_LIMIT == "5/minute"
    assert MFA_RATE_LIMIT == "5/minute"
    assert REFRESH_RATE_LIMIT == "30/minute"


def test_redis_storage_and_development_only_fallback(monkeypatch):
    assert limiter._storage_uri == settings.REDIS_URL
    assert in_memory_fallback_enabled() is False  # ENVIRONMENT=test

    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    assert in_memory_fallback_enabled() is True


def test_auth_routes_declare_expected_limits():
    login_source = inspect.getsource(login)
    assert "@limiter.limit(LOGIN_RATE_LIMIT)" in login_source
    assert "@limiter.limit(LOGIN_RATE_LIMIT, key_func=get_email_key)" in login_source

    mfa_source = inspect.getsource(verify_mfa_login)
    assert "@limiter.limit(MFA_RATE_LIMIT)" in mfa_source
    assert "@limiter.limit(MFA_RATE_LIMIT, key_func=get_mfa_subject_key)" in mfa_source

    assert "@limiter.limit(REFRESH_RATE_LIMIT)" in inspect.getsource(refresh_token)

    assert len(limiter._route_limits["app.api.v1.auth.login"]) == 2
    assert len(limiter._route_limits["app.api.v1.auth.verify_mfa_login"]) == 2
    assert len(limiter._route_limits["app.api.v1.auth.refresh_token"]) == 1


def test_email_key_normalizes_address():
    assert get_email_key(_request_with_body({"email": " User@Example.COM "})) == "email:user@example.com"
    assert get_email_key(_request_with_body({})) == "email:unknown"


def test_mfa_subject_key_uses_the_mfa_token_subject():
    token = _create_mfa_token(SimpleNamespace(id=42))
    assert get_mfa_subject_key(_request_with_body({"mfa_token": token})) == "mfa-user:42"
    assert get_mfa_subject_key(_request_with_body({"mfa_token": "invalid"})) == "mfa-user:unknown"


def test_rate_limiting_returns_429_when_enabled():
    local_limiter = _memory_limiter()

    app = FastAPI()
    app.state.limiter = local_limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.get("/limited")
    @local_limiter.limit("2/minute")
    def limited(request: Request):
        return {"ok": True}

    with TestClient(app) as client:
        statuses = [client.get("/limited").status_code for _ in range(5)]

    assert statuses == [200, 200, 429, 429, 429]


def test_login_is_limited_per_ip_and_per_email():
    local_limiter = _memory_limiter()

    app = FastAPI()
    app.state.limiter = local_limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.post("/login")
    @local_limiter.limit("2/minute")
    @local_limiter.limit("2/minute", key_func=get_email_key)
    def login_limited(request: Request, payload: dict):
        return {"ok": True}

    first_ip = TestClient(app, client=("203.0.113.7", 50000))
    second_ip = TestClient(app, client=("203.0.113.8", 50000))
    third_ip = TestClient(app, client=("203.0.113.9", 50000))

    same_account = [
        first_ip.post("/login", json={"email": "a@example.com"}).status_code for _ in range(3)
    ]
    assert same_account == [200, 200, 429]

    # Same IP, different account: the IP bucket is already exhausted.
    assert first_ip.post("/login", json={"email": "b@example.com"}).status_code == 429

    # Same account, different IP: the email bucket is already exhausted.
    assert second_ip.post("/login", json={"email": "a@example.com"}).status_code == 429

    # Fresh IP and account are still allowed.
    assert third_ip.post("/login", json={"email": "c@example.com"}).status_code == 200


def test_mfa_verify_is_limited_per_ip_and_per_subject():
    local_limiter = _memory_limiter()

    app = FastAPI()
    app.state.limiter = local_limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.post("/mfa/verify")
    @local_limiter.limit("2/minute")
    @local_limiter.limit("2/minute", key_func=get_mfa_subject_key)
    def mfa_limited(request: Request, payload: dict):
        return {"ok": True}

    token = _create_mfa_token(SimpleNamespace(id=42))
    other_token = _create_mfa_token(SimpleNamespace(id=43))
    fresh_token = _create_mfa_token(SimpleNamespace(id=44))

    first_ip = TestClient(app, client=("198.51.100.7", 50000))
    second_ip = TestClient(app, client=("198.51.100.8", 50000))
    third_ip = TestClient(app, client=("198.51.100.9", 50000))

    same_subject = [
        first_ip.post("/mfa/verify", json={"mfa_token": token}).status_code for _ in range(3)
    ]
    assert same_subject == [200, 200, 429]

    assert first_ip.post("/mfa/verify", json={"mfa_token": other_token}).status_code == 429
    assert second_ip.post("/mfa/verify", json={"mfa_token": token}).status_code == 429
    assert third_ip.post("/mfa/verify", json={"mfa_token": fresh_token}).status_code == 200


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
