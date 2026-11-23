"""Signed, single-path asset URLs replace the query-string access token."""

import time
from datetime import date, datetime, timezone
from urllib.parse import parse_qs, urlparse

import pytest
from jose import jwt

from app.core.asset_urls import ASSET_URL_TTL_SECONDS, create_signed_asset_url
from app.core.config import settings
from app.core.security import create_access_token, verify_access_token
from app.models.employee import Employee, EmployeeDocument
from app.models.user import Permission, Role, User


@pytest.fixture
def upload_root(tmp_path, monkeypatch):
    root = tmp_path / "uploads"
    (root / "employee_docs" / "2").mkdir(parents=True)
    (root / "photos").mkdir(parents=True)
    (root / "employee_docs" / "2" / "other.pdf").write_bytes(b"other")
    (root / "photos" / "avatar.png").write_bytes(b"photo")
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(root))
    return root


def _user(db, email, permissions=(), document_owner=False):
    perms = []
    for name in permissions:
        perm = db.query(Permission).filter(Permission.name == name).first()
        if perm is None:
            perm = Permission(name=name, description=name, module="test")
            db.add(perm)
            db.flush()
        perms.append(perm)
    role = Role(name=f"role_{email}", description="Test", permissions=perms)
    db.add(role)
    db.flush()
    user = User(email=email, hashed_password="unused", is_active=True, role_id=role.id)
    db.add(user)
    db.flush()
    if document_owner:
        employee = Employee(
            employee_id=f"EMP-{email}",
            first_name="Test",
            last_name="Employee",
            date_of_joining=date(2020, 1, 1),
            user_id=user.id,
        )
        db.add(employee)
        db.flush()
        db.add(
            EmployeeDocument(
                employee_id=employee.id,
                document_type="ID Proof",
                file_url="/uploads/employee_docs/2/other.pdf",
            )
        )
        db.commit()
    return user


def _headers(user):
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def test_sign_requires_authentication(client, upload_root):
    response = client.post("/api/v1/uploads/sign", json={"path": "/uploads/employee_docs/2/other.pdf"})
    assert response.status_code == 403


def test_sign_runs_the_same_authorization_as_download(client, db, upload_root):
    viewer = _user(db, "viewer@example.com")
    response = client.post(
        "/api/v1/uploads/sign",
        json={"path": "/uploads/employee_docs/2/other.pdf"},
        headers=_headers(viewer),
    )
    assert response.status_code == 403

    owner = _user(db, "owner@example.com", document_owner=True)
    response = client.post(
        "/api/v1/uploads/sign",
        json={"path": "/uploads/employee_docs/2/other.pdf"},
        headers=_headers(owner),
    )
    assert response.status_code == 200

    hr = _user(db, "hr@example.com", permissions=("employee_sensitive_view",))
    response = client.post(
        "/api/v1/uploads/sign",
        json={"path": "/uploads/employee_docs/2/other.pdf"},
        headers=_headers(hr),
    )
    assert response.status_code == 200
    assert response.json()["expires_in"] == ASSET_URL_TTL_SECONDS


def test_signed_url_downloads_without_bearer_token(client, db, upload_root):
    hr = _user(db, "hr2@example.com", permissions=("employee_sensitive_view",))
    signed = client.post(
        "/api/v1/uploads/sign",
        json={"path": "/uploads/employee_docs/2/other.pdf"},
        headers=_headers(hr),
    ).json()["url"]

    response = client.get(f"{settings.API_V1_STR}{signed}")
    assert response.status_code == 200
    assert response.content == b"other"


def test_signed_url_is_bound_to_one_path(client, db, upload_root):
    hr = _user(db, "hr3@example.com", permissions=("employee_sensitive_view",))
    signed = client.post(
        "/api/v1/uploads/sign",
        json={"path": "/uploads/employee_docs/2/other.pdf"},
        headers=_headers(hr),
    ).json()["url"]
    query = parse_qs(urlparse(signed).query)

    # The same signature cannot be replayed against a different stored path.
    response = client.get(
        "/api/v1/uploads/photos/avatar.png",
        params={"expires": query["expires"][0], "sig": query["sig"][0]},
    )
    assert response.status_code == 403

    tampered = client.get(
        "/api/v1/uploads/employee_docs/2/other.pdf",
        params={"expires": query["expires"][0], "sig": "0" * len(query["sig"][0])},
    )
    assert tampered.status_code == 403


def test_expired_signature_is_rejected(client, upload_root):
    relative = "employee_docs/2/other.pdf"
    expires = str(int(time.time()) - 1)
    from app.core.asset_urls import _signature

    response = client.get(
        f"/api/v1/uploads/{relative}",
        params={"expires": expires, "sig": _signature(f"{relative}|{expires}")},
    )
    assert response.status_code == 403


def test_query_access_token_is_not_accepted(client, db, upload_root):
    hr = _user(db, "hr4@example.com", permissions=("employee_sensitive_view",))
    token = create_access_token(hr.id)

    response = client.get("/api/v1/uploads/employee_docs/2/other.pdf", params={"token": token})
    assert response.status_code == 403


def test_access_token_default_lifetime_is_15_minutes():
    token = create_access_token(1)
    payload = verify_access_token(token)
    assert payload is not None
    remaining = payload["exp"] - datetime.now(timezone.utc).timestamp()
    assert 890 <= remaining <= 900

    now = int(time.time())
    expected = jwt.encode(
        {"exp": now + 900, "sub": "1", "type": "access"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    assert verify_access_token(expected) is not None


def test_signed_url_helper_uses_sixty_second_window():
    url = create_signed_asset_url("employee_docs/2/other.pdf")
    query = parse_qs(urlparse(url).query)
    remaining = int(query["expires"][0]) - int(time.time())
    assert 0 < remaining <= ASSET_URL_TTL_SECONDS
