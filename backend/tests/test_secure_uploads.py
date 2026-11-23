import pytest
from starlette.routing import Mount

from app.core.config import settings
from app.core.security import create_access_token
from app.main import app
from app.models.user import Role, User

UPLOAD_URL = "/api/v1/uploads/photos/avatar.png"


@pytest.fixture
def upload_root(tmp_path, monkeypatch):
    root = tmp_path / "uploads"
    (root / "photos").mkdir(parents=True)
    (root / "photos" / "avatar.png").write_bytes(b"fake-image")
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(root))
    return root


@pytest.fixture
def outside_file(upload_root):
    path = upload_root.parent / "secret.txt"
    path.write_text("do not serve")
    return path


def test_public_upload_mount_is_removed():
    assert not any(isinstance(route, Mount) and route.name == "uploads" for route in app.routes)


def test_download_requires_authentication(client, upload_root):
    response = client.get(UPLOAD_URL)
    assert response.status_code == 403


def test_legacy_public_upload_path_is_not_served(client, upload_root):
    response = client.get("/uploads/photos/avatar.png")
    assert response.status_code == 404


def test_authenticated_user_can_download(client, upload_root, superuser_headers):
    response = client.get(UPLOAD_URL, headers=superuser_headers)
    assert response.status_code == 200
    assert response.content == b"fake-image"


def test_token_query_parameter_supports_native_browser_requests(client, upload_root, superuser_token):
    response = client.get(f"{UPLOAD_URL}?token={superuser_token}")
    assert response.status_code == 200
    assert response.content == b"fake-image"


@pytest.mark.parametrize(
    "relative_path",
    [
        "../secret.txt",
        "..%2Fsecret.txt",
        "photos/../../secret.txt",
        "photos/..%2F..%2Fsecret.txt",
        "/etc/passwd",
    ],
)
def test_path_traversal_is_rejected(client, upload_root, outside_file, superuser_headers, relative_path):
    response = client.get(f"/api/v1/uploads/{relative_path}", headers=superuser_headers)
    assert response.status_code == 404


def test_symlinked_file_is_rejected(client, upload_root, outside_file, superuser_headers):
    link = upload_root / "photos" / "linked.txt"
    try:
        link.symlink_to(outside_file)
    except OSError as exc:
        pytest.skip(f"symlinks are unavailable in this environment: {exc}")

    response = client.get("/api/v1/uploads/photos/linked.txt", headers=superuser_headers)
    assert response.status_code == 404


def test_symlinked_parent_directory_is_rejected(client, upload_root, outside_file, superuser_headers):
    link = upload_root / "outside"
    try:
        link.symlink_to(upload_root.parent, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"symlinks are unavailable in this environment: {exc}")

    response = client.get("/api/v1/uploads/outside/secret.txt", headers=superuser_headers)
    assert response.status_code == 404


def test_inactive_user_cannot_download(client, upload_root, db):
    role = Role(name="employee", description="Employee", is_system=True)
    db.add(role)
    db.flush()
    user = User(
        email="inactive@example.com",
        hashed_password="unused",
        is_active=False,
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    token = create_access_token(user.id)

    response = client.get(UPLOAD_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_active_non_superuser_can_download(client, upload_root, db):
    role = Role(name="employee", description="Employee", is_system=True)
    db.add(role)
    db.flush()
    user = User(
        email="employee@example.com",
        hashed_password="unused",
        is_active=True,
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    token = create_access_token(user.id)

    response = client.get(UPLOAD_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
