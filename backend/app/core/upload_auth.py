"""Authorization rules for stored upload URLs.

Stored URLs remain ``/uploads/<relative path>``. Every download is checked
against a prefix allowlist; anything not explicitly mapped is denied. HR and
superusers may read all mapped assets; employees may read only documents whose
owning employee is linked to their own user account.
"""

from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.masking import user_has_permission
from app.models.user import User

FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access this file",
)

# Employee-owned documents: the owner, HR, and admins only.
OWNER_PREFIXES = ("employee_docs/", "certificates/", "documents/")
# Payroll, statutory, and full-and-final exports need payroll read access.
PAYROLL_PREFIXES = (
    "exports/payroll/",
    "exports/statutory/",
    "payslips/",
    "fnf-settlements/",
    "form16/",
    "tax_proofs/",
    "statutory/",
)
# Resumes and background-verification reports are recruiter/HR material.
RECRUITING_PREFIXES = ("resumes/", "bgv/", "background_verification/", "certificate_imports/")
# Low-sensitivity directory images are visible to any authenticated employee.
AUTHENTICATED_PREFIXES = ("photos/", "company_logos/")
# Remaining mapped prefixes require a named permission.
PERMISSION_PREFIXES = {
    "reports/": "reports_view",
    "crm/": "crm_view",
    "pms/": "pms_view",
}

# Prefixes whose first path segment is the owning employee's database id.
_IDENTIFIED_PREFIXES = ("employee_docs", "certificates", "form16", "tax_proofs", "documents")


def _owning_employee_id(db: Session, relative_path: str) -> Optional[int]:
    """Find the employee that owns a stored URL, by DB row then by path id."""
    stored_url = "/uploads/" + relative_path

    from app.models.document import EmployeeCertificate, GeneratedDocument
    from app.models.employee import Employee, EmployeeDocument, EmployeeEducation, EmployeeExperience

    for model, url_column, owner_column in (
        (EmployeeDocument, EmployeeDocument.file_url, EmployeeDocument.employee_id),
        (EmployeeCertificate, EmployeeCertificate.file_url, EmployeeCertificate.employee_id),
        (GeneratedDocument, GeneratedDocument.file_url, GeneratedDocument.employee_id),
        (EmployeeEducation, EmployeeEducation.document_url, EmployeeEducation.employee_id),
        (EmployeeExperience, EmployeeExperience.relieving_letter_url, EmployeeExperience.employee_id),
    ):
        row = db.query(owner_column).filter(url_column == stored_url).first()
        if row is not None:
            return row[0]

    row = db.query(Employee.id).filter(Employee.profile_photo_url == stored_url).first()
    if row is not None:
        return row[0]

    parts = relative_path.split("/")
    if len(parts) >= 2 and parts[0] in _IDENTIFIED_PREFIXES:
        try:
            return int(parts[1])
        except ValueError:
            return None
    return None


def _is_owner(db: Session, user: User, relative_path: str) -> bool:
    employee_id = _owning_employee_id(db, relative_path)
    if employee_id is None:
        return False
    from app.models.employee import Employee

    row = db.query(Employee.user_id).filter(Employee.id == employee_id).first()
    return bool(row and row[0] == user.id)


def authorize_upload_access(user: User, db: Session, relative_path: str) -> None:
    """Raise 403 unless ``user`` may read ``relative_path``. Deny by default."""
    relative_path = relative_path.lstrip("/")

    # An unmapped prefix is denied for everyone, including admins and HR.
    mapped = any(
        relative_path.startswith(prefix)
        for prefix in OWNER_PREFIXES + PAYROLL_PREFIXES + RECRUITING_PREFIXES + AUTHENTICATED_PREFIXES
    ) or any(relative_path.startswith(prefix) for prefix in PERMISSION_PREFIXES)
    if not mapped:
        raise FORBIDDEN

    # Admins and HR may read every mapped asset class.
    if user.is_superuser or user_has_permission(user, "employee_sensitive_view"):
        return

    if any(relative_path.startswith(prefix) for prefix in OWNER_PREFIXES):
        if _is_owner(db, user, relative_path):
            return
        raise FORBIDDEN

    if any(relative_path.startswith(prefix) for prefix in PAYROLL_PREFIXES):
        if user_has_permission(user, "payroll_view"):
            return
        raise FORBIDDEN

    if any(relative_path.startswith(prefix) for prefix in RECRUITING_PREFIXES):
        if user_has_permission(user, "recruitment_view") or user_has_permission(user, "recruitment_manage"):
            return
        raise FORBIDDEN

    if any(relative_path.startswith(prefix) for prefix in AUTHENTICATED_PREFIXES):
        return

    for prefix, permission in PERMISSION_PREFIXES.items():
        if relative_path.startswith(prefix) and user_has_permission(user, permission):
            return

    # Unmapped prefixes are never served.
    raise FORBIDDEN
