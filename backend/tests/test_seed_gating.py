import pytest

from app.apps.crm.models import CRMLead
from app.core.config import settings
from app.core.security import verify_password
from app.db.init_db import DEMO_USERS, init_db
from app.models.user import Role, User
from scripts.create_admin import create_admin, validate_admin_password


DEMO_EMAIL = DEMO_USERS[0]["email"]


def _configure(monkeypatch, environment="development", seed_demo=False):
    monkeypatch.setattr(settings, "ENVIRONMENT", environment)
    monkeypatch.setattr(settings, "SEED_DEMO_DATA", seed_demo)


def test_demo_users_require_explicit_opt_in(monkeypatch, db):
    _configure(monkeypatch, seed_demo=False)
    init_db(db)

    assert db.query(User).filter(User.email == DEMO_EMAIL).first() is None
    assert db.query(Role).filter(Role.name == "super_admin").first() is not None


def test_demo_users_are_never_seeded_in_production(monkeypatch, db):
    _configure(monkeypatch, environment="production", seed_demo=True)
    init_db(db)

    assert db.query(User).filter(User.email == DEMO_EMAIL).first() is None


def test_repeated_seeding_does_not_change_existing_user_privileges(monkeypatch, db):
    _configure(monkeypatch, seed_demo=True)
    init_db(db)

    user = db.query(User).filter(User.email == DEMO_EMAIL).first()
    employee_role = db.query(Role).filter(Role.name == "employee").first()
    original_hash = user.hashed_password
    user.role_id = employee_role.id
    user.is_superuser = False
    user.is_active = False
    db.commit()

    init_db(db)
    db.refresh(user)

    assert user.role_id == employee_role.id
    assert user.is_superuser is False
    assert user.is_active is False
    assert user.hashed_password == original_hash


def test_crm_demo_seed_respects_gating(monkeypatch, db):
    from app.apps.crm.seed import seed_crm_demo_data

    _configure(monkeypatch, environment="production", seed_demo=True)
    seed_crm_demo_data(db, organization_id=1)
    assert db.query(CRMLead).count() == 0

    _configure(monkeypatch, environment="development", seed_demo=True)
    seed_crm_demo_data(db, organization_id=1)
    assert db.query(CRMLead).count() > 0


def test_create_admin_enforces_password_policy(monkeypatch, db):
    _configure(monkeypatch, environment="production", seed_demo=False)

    for weak in ("short", "alllowercase1", "ALLUPPERCASE1", "NoNumbersHere"):
        with pytest.raises(ValueError):
            validate_admin_password(weak, "ops@example.com")

    admin = create_admin(db, "Ops@Example.com", "StrongAdmin#2026")
    assert admin.email == "ops@example.com"
    assert admin.is_superuser is True
    assert admin.is_active is True
    assert verify_password("StrongAdmin#2026", admin.hashed_password)

    with pytest.raises(ValueError, match="already exists"):
        create_admin(db, "ops@example.com", "AnotherStrong#2026")
