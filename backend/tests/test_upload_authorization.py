"""Per-prefix authorization for stored upload URLs (deny by default)."""

from datetime import date

import pytest

from app.core.config import settings
from app.core.security import create_access_token
from app.models.employee import Employee, EmployeeDocument
from app.models.user import Permission, Role, User


@pytest.fixture
def upload_root(tmp_path, monkeypatch):
    root = tmp_path / "uploads"
    for folder in (
        "employee_docs/1",
        "employee_docs/2",
        "certificates/2",
        "exports/payroll/9",
        "resumes",
        "photos",
        "mystery",
        "brand-new-folder",
    ):
        (root / folder).mkdir(parents=True)
    (root / "employee_docs" / "1" / "own.pdf").write_bytes(b"own")
    (root / "employee_docs" / "2" / "other.pdf").write_bytes(b"other")
    (root / "certificates" / "2" / "cert.pdf").write_bytes(b"cert")
    (root / "exports" / "payroll" / "9" / "run.csv").write_bytes(b"payroll")
    (root / "resumes" / "cv.pdf").write_bytes(b"resume")
    (root / "photos" / "avatar.png").write_bytes(b"photo")
    (root / "mystery" / "secret.bin").write_bytes(b"secret")
    (root / "brand-new-folder" / "file.txt").write_bytes(b"new")
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(root))
    return root


def _user(db, email, permissions=(), is_superuser=False, employee_id=None):
    perms = []
    for name in permissions:
        perm = db.query(Permission).filter(Permission.name == name).first()
        if perm is None:
            perm = Permission(name=name, description=name, module="test")
            db.add(perm)
            db.flush()
        perms.append(perm)

    role = Role(name=f"role_{email}", description="Test role", is_system=False, permissions=perms)
    db.add(role)
    db.flush()

    user = User(
        email=email,
        hashed_password="unused",
        is_active=True,
        is_superuser=is_superuser,
        role_id=role.id,
    )
    db.add(user)
    db.flush()

    if employee_id is not None:
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if employee is None:
            employee = Employee(
                id=employee_id,
                employee_id=f"EMP-{employee_id}",
                first_name="Test",
                last_name="Employee",
                date_of_joining=date(2020, 1, 1),
                user_id=user.id,
            )
            db.add(employee)
        else:
            employee.user_id = user.id

    db.commit()
    return user


def _headers(user):
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def test_employee_cannot_fetch_another_employees_document(client, db, upload_root):
    other = _user(db, "other@example.com", employee_id=2)
    db.add(
        EmployeeDocument(
            employee_id=other.employee.id,
            document_type="ID Proof",
            file_url="/uploads/employee_docs/2/other.pdf",
        )
    )
    db.commit()
    viewer = _user(db, "viewer@example.com")

    response = client.get("/api/v1/uploads/employee_docs/2/other.pdf", headers=_headers(viewer))
    assert response.status_code == 403


def test_owner_can_fetch_own_document(client, db, upload_root):
    owner = _user(db, "owner@example.com", employee_id=2)
    db.add(
        EmployeeDocument(
            employee_id=owner.employee.id,
            document_type="ID Proof",
            file_url="/uploads/employee_docs/2/other.pdf",
        )
    )
    db.commit()

    response = client.get("/api/v1/uploads/employee_docs/2/other.pdf", headers=_headers(owner))
    assert response.status_code == 200
    assert response.content == b"other"


def test_hr_can_fetch_another_employees_document(client, db, upload_root):
    _user(db, "owner2@example.com", employee_id=2)
    hr = _user(db, "hr@example.com", permissions=("employee_sensitive_view",))

    response = client.get("/api/v1/uploads/employee_docs/2/other.pdf", headers=_headers(hr))
    assert response.status_code == 200
    assert response.content == b"other"


def test_superuser_can_fetch_documents(client, db, upload_root):
    admin = _user(db, "admin@example.com", is_superuser=True)

    response = client.get("/api/v1/uploads/employee_docs/2/other.pdf", headers=_headers(admin))
    assert response.status_code == 200


@pytest.mark.parametrize("relative_path", ["mystery/secret.bin", "brand-new-folder/file.txt"])
def test_unmapped_prefix_is_denied_even_for_hr(client, db, upload_root, relative_path):
    hr = _user(db, "hr2@example.com", permissions=("employee_sensitive_view",))

    response = client.get(f"/api/v1/uploads/{relative_path}", headers=_headers(hr))
    assert response.status_code == 403


@pytest.mark.parametrize(
    "relative_path,permissions",
    [
        ("exports/payroll/9/run.csv", ("payroll_view",)),
        ("certificates/2/cert.pdf", ("employee_sensitive_view",)),
        ("resumes/cv.pdf", ("recruitment_view",)),
        ("photos/avatar.png", ()),
    ],
)
def test_mapped_prefixes_allow_expected_users(client, db, upload_root, relative_path, permissions):
    user = _user(db, f"allowed_{relative_path.replace('/', '_')}@example.com", permissions=permissions)

    response = client.get(f"/api/v1/uploads/{relative_path}", headers=_headers(user))
    assert response.status_code == 200


def test_payroll_export_denied_without_payroll_permission(client, db, upload_root):
    employee = _user(db, "nopayroll@example.com")

    response = client.get("/api/v1/uploads/exports/payroll/9/run.csv", headers=_headers(employee))
    assert response.status_code == 403
