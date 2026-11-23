"""Task 8: token storage, type enforcement and session revocation."""

from fastapi import Response, status
from jose import jwt

from app.api.v1.auth import (
    REFRESH_COOKIE_NAME,
    REFRESH_COOKIE_PATH,
    _create_mfa_token,
    _decode_mfa_token,
    _set_refresh_cookie,
)
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
)
from app.db.init_db import init_db
from app.models.user import User


def _set_cookie_header(response) -> str:
    headers = response.headers
    values = headers.get_list("set-cookie") if hasattr(headers, "get_list") else headers.getlist("set-cookie")
    return " ".join(values)


def _login(client, email: str = "admin@aihrms.com", password: str = "Admin@123456"):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def _seeded_admin_login(client, db):
    init_db(db)
    return _login(client)


def test_access_and_refresh_token_types_are_enforced():
    access = create_access_token("1")
    refresh = create_refresh_token("1")

    assert verify_access_token(access) is not None
    assert verify_access_token(refresh) is None
    assert verify_refresh_token(refresh) is not None
    assert verify_refresh_token(access) is None


def test_token_without_exp_is_rejected():
    no_exp = jwt.encode({"sub": "1", "type": "access"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    assert verify_access_token(no_exp) is None


def test_mfa_token_cannot_be_used_as_access_token(db):
    init_db(db)
    user = db.query(User).filter(User.email == "admin@aihrms.com").first()
    assert user is not None

    mfa_token = _create_mfa_token(user)
    assert _decode_mfa_token(mfa_token)["sub"] == str(user.id)

    try:
        _decode_mfa_token(create_access_token(user.id))
        raise AssertionError("access token was accepted as an MFA token")
    except Exception as exc:
        assert "Invalid MFA token" in str(exc)


def test_login_sets_hardened_refresh_cookie(client, db):
    response = _seeded_admin_login(client, db)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("refresh_token") is None

    cookie_header = _set_cookie_header(response)
    assert f"{REFRESH_COOKIE_NAME}=" in cookie_header
    assert "HttpOnly" in cookie_header
    assert "SameSite=strict" in cookie_header
    assert f"Path={REFRESH_COOKIE_PATH}" in cookie_header
    assert "Secure" in cookie_header  # Secure in every environment except development

    payload = verify_access_token(response.json()["access_token"])
    assert payload is not None
    assert payload["sid"]


def test_refresh_cookie_is_secure_in_production(monkeypatch):
    response = Response()
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    _set_refresh_cookie(response, "test-refresh-token")
    assert "Secure" in _set_cookie_header(response)


def test_refresh_token_rotation_revokes_previous_token(client, db):
    login = _seeded_admin_login(client, db)
    original_refresh = login.cookies.get(REFRESH_COOKIE_NAME)
    assert original_refresh

    first = client.post("/api/v1/auth/refresh", json={})
    assert first.status_code == status.HTTP_200_OK
    assert first.cookies.get(REFRESH_COOKIE_NAME) != original_refresh

    # Clear the jar so the replay cannot accidentally send the rotated cookie.
    client.cookies.clear()
    client.cookies.set(REFRESH_COOKIE_NAME, original_refresh, path=REFRESH_COOKIE_PATH)
    replay = client.post("/api/v1/auth/refresh", json={})
    assert replay.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_revokes_refresh_session(client, db):
    login = _seeded_admin_login(client, db)
    access_token = login.json()["access_token"]
    refresh_token = login.cookies.get(REFRESH_COOKIE_NAME)
    assert refresh_token

    logout = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert logout.status_code == status.HTTP_200_OK

    client.cookies.set(REFRESH_COOKIE_NAME, refresh_token, path=REFRESH_COOKIE_PATH)
    refresh = client.post("/api/v1/auth/refresh", json={})
    assert refresh.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_rejects_token_not_recorded_in_sessions(client, db):
    init_db(db)
    forged = create_refresh_token("999")
    client.cookies.set(REFRESH_COOKIE_NAME, forged, path=REFRESH_COOKIE_PATH)
    response = client.post("/api/v1/auth/refresh", json={})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
