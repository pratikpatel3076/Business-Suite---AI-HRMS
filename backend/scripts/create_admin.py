"""Create the first administrator in a hardened (production) deployment.

Usage (from the backend directory):
    ADMIN_EMAIL=ops@example.com ADMIN_PASSWORD='...' python scripts/create_admin.py

If either variable is missing the script prompts securely. The password is
never printed. Reference/role data is seeded without demo users or passwords.
"""

from __future__ import annotations

import getpass
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session  # noqa: E402

from app.core.security import get_password_hash  # noqa: E402
from app.models.user import Role, User  # noqa: E402


MIN_PASSWORD_LENGTH = 12


def validate_admin_password(password: str, email: str | None = None) -> None:
    """Enforce the default password policy for a privileged bootstrap account."""
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain an uppercase letter")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain a lowercase letter")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain a number")
    if email and password.lower() == email.lower():
        raise ValueError("Password must not match the email address")


def create_admin(db: Session, email: str, password: str) -> User:
    """Create a single superuser. Refuses to modify an existing account."""
    email = email.strip().lower()
    if not email or "@" not in email:
        raise ValueError("A valid admin email is required")
    validate_admin_password(password, email)

    if db.query(User).filter(User.email == email).first():
        raise ValueError(f"User {email} already exists; use the normal password reset flow")

    # Seed permissions/roles only. Demo data is disabled in production.
    from app.db.init_common_db import init_common_db
    from app.db.init_db import init_db
    from app.module_registry import is_app_enabled

    (init_db if is_app_enabled("hrms") else init_common_db)(db)

    role = db.query(Role).filter(Role.name == "super_admin").first()
    if not role:
        raise RuntimeError("super_admin role could not be initialised")

    admin = User(
        email=email,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_superuser=True,
        role_id=role.id,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def main() -> None:
    email = os.environ.get("ADMIN_EMAIL", "").strip()
    if not email:
        email = input("Admin email: ").strip()
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not password:
        password = getpass.getpass("Admin password: ")

    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        admin = create_admin(db, email, password)
    except (ValueError, RuntimeError) as exc:
        print(f"Failed to create admin: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    finally:
        db.close()
    print(f"Created superuser {admin.email}. Store the password in your secret manager.")


if __name__ == "__main__":
    main()
