"""Environment allowlist, cookie Secure flag, and audit error logging."""

import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi import Response
from pydantic import ValidationError
from starlette.requests import Request

from app.api.v1.auth import _set_refresh_cookie
from app.core.config import Settings, settings
from app.core.middleware.audit import AuditLogMiddleware

SECRETS = {
    "SECRET_KEY": "a-unique-production-secret-with-32-chars",
    "REFRESH_SECRET_KEY": "a-different-refresh-secret-with-32-chars",
    "ENCRYPTION_KEY": "a-different-encryption-key-with-32-chars",
}


def test_default_environment_is_production(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    config = Settings(_env_file=None, **SECRETS)
    assert config.ENVIRONMENT == "production"


@pytest.mark.parametrize("environment", ["staging", "prod", ""])
def test_unknown_environment_is_rejected(environment):
    with pytest.raises(ValidationError, match="ENVIRONMENT must be one of"):
        Settings(_env_file=None, ENVIRONMENT=environment, **SECRETS)


def test_test_environment_is_refused_outside_pytest(monkeypatch):
    monkeypatch.delitem(sys.modules, "pytest", raising=False)
    with pytest.raises(ValidationError, match="only permitted when pytest is loaded"):
        Settings(_env_file=None, ENVIRONMENT="test", **SECRETS)


@pytest.mark.parametrize(
    "environment,secure_expected",
    [("development", False), ("test", True), ("production", True)],
)
def test_refresh_cookie_secure_flag(environment, secure_expected, monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", environment)
    response = Response()
    _set_refresh_cookie(response, "refresh-token-value")

    cookie_header = response.headers["set-cookie"]
    assert ("Secure" in cookie_header) is secure_expected
    assert "HttpOnly" in cookie_header
    assert "SameSite=strict" in cookie_header


async def test_audit_persistence_errors_are_logged(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    fake_db = MagicMock()
    fake_db.commit.side_effect = RuntimeError("database unavailable")
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/v1/example",
            "headers": [],
            "query_string": b"sig=redacted",
        }
    )
    middleware = AuditLogMiddleware(app=MagicMock())

    with (
        patch("app.db.session.SessionLocal", return_value=fake_db),
        patch("app.core.middleware.audit.logger.exception") as log_exception,
    ):
        await middleware._log_request(request, 200, 1)

    log_exception.assert_called_once()
    assert "audit" in log_exception.call_args.args[0].lower()
    fake_db.rollback.assert_called_once()
