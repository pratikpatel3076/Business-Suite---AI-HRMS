"""Authorization rules for stored upload URLs.

Stored URLs remain ``/uploads/<relative path>``. Every download is checked
against the prefix allowlist below; anything not explicitly mapped is denied
for every user, including HR and superusers. HR and superusers may read all
mapped assets. Employees may read only documents they own, while payroll,
recruiting, CRM, and report exports keep their own permission checks.
"""

from __future__ import annotations

import re
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.masking import user_has_permission
from app.models.user import User

FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access this file",
)

# Single source of truth for both enforcement and
# scripts/enumerate_upload_prefixes.py. Values are (internal rule, description).
# Longest matching prefix wins, so specific subfolders can refine a broad class.
PREFIX_RULES = {
    "employee_docs/": ("owner", "owner, HR, superuser"),
    "certificates/": ("owner", "owner, HR, superuser"),
    "documents/": ("owner", "owner, HR, superuser"),
    "payslips/": ("payroll_owner", "owner, payroll_view, HR, superuser"),
    "form16/": ("payroll_owner", "owner, payroll_view, HR, superuser"),
    "tax_proofs/": ("payroll_owner", "owner, payroll_view, HR, superuser"),
    "exports/payroll/": ("payroll", "payroll_view, HR, superuser"),
    "exports/payroll/payments/": ("payroll", "payroll_view, HR, superuser"),
    "exports/payroll/statutory_validations/": ("payroll", "payroll_view, HR, superuser"),
    "exports/payroll/bank_advice/": ("payroll", "payroll_view, HR, superuser"),
    "exports/statutory/": ("payroll", "payroll_view, HR, superuser"),
    "statutory/": ("payroll", "payroll_view, HR, superuser"),
    "statutory_validations/": ("payroll", "payroll_view, HR, superuser"),
    "fnf-settlements/": ("payroll", "payroll_view, HR, superuser"),
    "templates/": ("payroll", "payroll_view, HR, superuser"),
    "templates/statutory/": ("payroll", "payroll_view, HR, superuser"),
    "probation_letters/": ("hr_only", "HR, superuser"),
    "resumes/": ("recruiting", "recruitment_view/manage, HR, superuser"),
    "bgv/": ("recruiting", "recruitment_view/manage, HR, superuser"),
    "background_verification/": ("recruiting", "recruitment_view/manage, HR, superuser"),
    "certificate_imports/": ("recruiting", "recruitment_view/manage, HR, superuser"),
    "quotations/": ("quotation", "crm_view, HR, superuser"),
    "crm/quotations/": ("quotation", "crm_view, HR, superuser"),
    "photos/": ("authenticated", "any authenticated user"),
    "company_logos/": ("authenticated", "any authenticated user"),
    "reports/": ("permission:reports_view", "reports_view, HR, superuser"),
    "crm/": ("permission:crm_view", "crm_view, HR, superuser"),
    "pms/": ("permission:pms_view", "pms_view, HR, superuser"),
}

OWNER_PREFIXES = tuple(prefix for prefix, (rule, _) in PREFIX_RULES.items() if rule == "owner")
PAYROLL_OWNER_PREFIXES = tuple(
    prefix for prefix, (rule, _) in PREFIX_RULES.items() if rule == "payroll_owner"
)
PAYROLL_PREFIXES = tuple(
    prefix for prefix, (rule, _) in PREFIX_RULES.items() if rule in {"payroll", "payroll_owner"}
)
HR_ONLY_PREFIXES = tuple(prefix for prefix, (rule, _) in PREFIX_RULES.items() if rule == "hr_only")
RECRUITING_PREFIXES = tuple(
    prefix for prefix, (rule, _) in PREFIX_RULES.items() if rule == "recruiting"
)
QUOTATION_PREFIXES = tuple(
    prefix for prefix, (rule, _) in PREFIX_RULES.items() if rule == "quotation"
)
AUTHENTICATED_PREFIXES = tuple(
    prefix for prefix, (rule, _) in PREFIX_RULES.items() if rule == "authenticated"
)
PERMISSION_PREFIXES = {
    prefix: rule.split(":", 1)[1]
    for prefix, (rule, _) in PREFIX_RULES.items()
    if rule.startswith("permission:")
}

# Prefixes whose first path segment is the owning employee's database id.
_IDENTIFIED_PREFIXES = ("employee_docs", "certificates", "form16", "tax_proofs", "documents")
# Payslips use a year/month directory and put the employee id in the filename.
_PAYSLIP_FILENAME = re.compile(r"^payslip_(\d+)_")


def _matched_rule(relative_path: str) -> tuple[str, str] | None:
    """Return the most specific rule for ``relative_path``, or ``None``."""
    matches = [prefix for prefix in PREFIX_RULES if relative_path.startswith(prefix)]
    return PREFIX_RULES[max(matches, key=len)] if matches else None


def _owning_employee_id(db: Session, relative_path: str) -> Optional[int]:
    """Find the employee that owns a stored URL, by DB row then by path id."""
    stored_url = "/uploads/" + relative_path

    from app.models.document import EmployeeCertificate, GeneratedDocument
    from app.models.employee import Employee, EmployeeDocument, EmployeeEducation, EmployeeExperience
    from app.models.payroll import EmployeeTaxDeclaration, EmployeeTaxDeclarationItem, EmployeeTaxProof, PayrollRecord
    from app.models.statutory_compliance import Form16Record

    # Employee-linked documents.
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

    # Payroll documents. The DB row is authoritative; the path is only a
    # fallback for legacy files whose URL was never persisted.
    row = db.query(PayrollRecord.employee_id).filter(PayrollRecord.payslip_pdf_url == stored_url).first()
    if row is not None:
        return row[0]

    row = db.query(Form16Record.employee_id).filter(
        or_(
            Form16Record.part_a_file_path == stored_url,
            Form16Record.part_b_file_path == stored_url,
            Form16Record.combined_file_path == stored_url,
        )
    ).first()
    if row is not None:
        return row[0]

    row = (
        db.query(EmployeeTaxDeclaration.employee_id)
        .join(
            EmployeeTaxDeclarationItem,
            EmployeeTaxDeclarationItem.declaration_id == EmployeeTaxDeclaration.id,
        )
        .join(EmployeeTaxProof, EmployeeTaxProof.declaration_item_id == EmployeeTaxDeclarationItem.id)
        .filter(EmployeeTaxProof.file_path == stored_url)
        .first()
    )
    if row is not None:
        return row[0]

    parts = relative_path.split("/")
    if len(parts) >= 2 and parts[0] in _IDENTIFIED_PREFIXES:
        try:
            return int(parts[1])
        except ValueError:
            return None

    if len(parts) >= 2 and parts[0] == "payslips":
        match = _PAYSLIP_FILENAME.match(parts[-1])
        if match:
            return int(match.group(1))
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
    matched = _matched_rule(relative_path)
    if matched is None:
        raise FORBIDDEN
    rule, _ = matched

    # HR and superusers may read every mapped asset class, but never an
    # unmapped prefix (handled above).
    if user.is_superuser or user_has_permission(user, "employee_sensitive_view"):
        return

    if rule == "owner":
        if _is_owner(db, user, relative_path):
            return
        raise FORBIDDEN

    if rule == "payroll_owner":
        if _is_owner(db, user, relative_path) or user_has_permission(user, "payroll_view"):
            return
        raise FORBIDDEN

    if rule == "payroll":
        if user_has_permission(user, "payroll_view"):
            return
        raise FORBIDDEN

    # Probation letters are HR-only; the employee id in the filename does not
    # grant the employee access.
    if rule == "hr_only":
        raise FORBIDDEN

    if rule == "recruiting":
        if user_has_permission(user, "recruitment_view") or user_has_permission(user, "recruitment_manage"):
            return
        raise FORBIDDEN

    if rule == "quotation":
        if user_has_permission(user, "crm_view"):
            return
        raise FORBIDDEN

    if rule == "authenticated":
        return

    if rule.startswith("permission:") and user_has_permission(user, rule.split(":", 1)[1]):
        return

    raise FORBIDDEN
