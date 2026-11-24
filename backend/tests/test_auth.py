import pytest
from fastapi.testclient import TestClient
from app.api.v1.auth import CSRF_HEADER_NAME, CSRF_HEADER_VALUE
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, Role
from app.db.init_db import init_db


def _cookie_auth_headers() -> dict:
    return {"Origin": settings.BACKEND_CORS_ORIGINS[0], CSRF_HEADER_NAME: CSRF_HEADER_VALUE}


def test_login_success(client, db):
    role = Role(name="employee_role", description="Employee", is_system=False)
    db.add(role)
    db.flush()
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("Test@123456"),
        is_active=True,
        role_id=role.id,
    )
    db.add(user)
    db.commit()

    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "Test@123456",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    # The refresh token must never be readable by JavaScript.
    assert data.get("refresh_token") is None
    cookie_header = " ".join(response.headers.get_list("set-cookie"))
    assert "refresh_token=" in cookie_header
    assert "HttpOnly" in cookie_header
    assert "SameSite=strict" in cookie_header
    assert data["email"] == "test@example.com"


def test_login_wrong_password(client, db):
    role = Role(name="employee_role2", description="Employee", is_system=False)
    db.add(role)
    db.flush()
    user = User(
        email="test2@example.com",
        hashed_password=get_password_hash("Test@123456"),
        is_active=True,
        role_id=role.id,
    )
    db.add(user)
    db.commit()

    response = client.post("/api/v1/auth/login", json={
        "email": "test2@example.com",
        "password": "WrongPassword",
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "nobody@example.com",
        "password": "Test@123456",
    })
    assert response.status_code == 401


def test_get_me(client, superuser_headers):
    response = client.get("/api/v1/auth/me", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["is_superuser"] is True


def test_get_me_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403  # Missing bearer token


def test_refresh_token(client, db):
    role = Role(name="refresh_role", description="Role", is_system=False)
    db.add(role)
    db.flush()
    user = User(
        email="refresh@example.com",
        hashed_password=get_password_hash("Refresh@123"),
        is_active=True,
        role_id=role.id,
    )
    db.add(user)
    db.commit()

    login_response = client.post("/api/v1/auth/login", json={
        "email": "refresh@example.com",
        "password": "Refresh@123",
    })
    # Refresh uses the HttpOnly cookie automatically stored by TestClient.
    assert any(c.name == "refresh_token" for c in client.cookies.jar)
    refresh_response = client.post("/api/v1/auth/refresh", json={}, headers=_cookie_auth_headers())
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()


def test_change_password(client, db):
    role = Role(name="change_pw_role", description="Role", is_system=False)
    db.add(role)
    db.flush()
    user = User(
        email="changepw@example.com",
        hashed_password=get_password_hash("OldPass@123"),
        is_active=True,
        role_id=role.id,
    )
    db.add(user)
    db.commit()

    login_response = client.post("/api/v1/auth/login", json={
        "email": "changepw@example.com",
        "password": "OldPass@123",
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/auth/change-password", json={
        "current_password": "OldPass@123",
        "new_password": "NewPass@456",
    }, headers=headers)
    assert response.status_code == 200

    # Old password should no longer work
    response2 = client.post("/api/v1/auth/login", json={
        "email": "changepw@example.com",
        "password": "OldPass@123",
    })
    assert response2.status_code == 401


def test_seeded_role_logins_have_expected_permissions(client, db):
    init_db(db)

    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin@gemeinsam.example",
        "password": "Admin@123456",
    })
    assert admin_login.status_code == 200
    assert admin_login.json()["role"] == "super_admin"
    assert admin_login.json()["is_superuser"] is True

    hr_login = client.post("/api/v1/auth/login", json={
        "email": "hr@gemeinsam.example",
        "password": "HR@123456",
    })
    assert hr_login.status_code == 200
    assert hr_login.json()["role"] == "hr_manager"
    hr_headers = {"Authorization": f"Bearer {hr_login.json()['access_token']}"}
    assert client.get("/api/v1/employees/", headers=hr_headers).status_code == 200

    employee_login = client.post("/api/v1/auth/login", json={
        "email": "employee@gemeinsam.example",
        "password": "Employee@123456",
    })
    assert employee_login.status_code == 200
    assert employee_login.json()["role"] == "employee"
    employee_headers = {"Authorization": f"Bearer {employee_login.json()['access_token']}"}
    assert client.get("/api/v1/employees/", headers=employee_headers).status_code == 403
    assert client.get("/api/v1/leave/balance", headers=employee_headers).status_code == 200


def test_only_admin_can_create_login_users(client, db):
    init_db(db)

    hr_login = client.post("/api/v1/auth/login", json={
        "email": "hr@gemeinsam.example",
        "password": "HR@123456",
    })
    hr_headers = {"Authorization": f"Bearer {hr_login.json()['access_token']}"}
    denied = client.post("/api/v1/auth/users", json={
        "email": "notallowed@gemeinsam.example",
        "password": "User@123456",
    }, headers=hr_headers)
    assert denied.status_code == 403

    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin@gemeinsam.example",
        "password": "Admin@123456",
    })
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
    created = client.post("/api/v1/auth/users", json={
        "email": "newuser@gemeinsam.example",
        "password": "User@123456",
    }, headers=admin_headers)
    assert created.status_code == 201
    assert created.json()["email"] == "newuser@gemeinsam.example"
