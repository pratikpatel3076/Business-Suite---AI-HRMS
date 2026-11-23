"""Generate docs/security/route-matrix.md from the running FastAPI app.

Run with all installable apps enabled:
    INSTALLED_APPS=hrms,crm,project_management python generate_route_matrix.py
"""

from __future__ import annotations

import inspect
import re
from pathlib import Path

from app.core.config import settings
from app.main import app

AUTH_DEPENDENCIES = {
    "get_current_user",
    "get_current_active_superuser",
    "get_current_user_for_asset",
    "RequirePermission",
    "require_roles",
    "checker",
}

SENSITIVE_PATTERNS = {
    "payroll": re.compile(r"(payroll|payslip|salary|/tax|statutory|reimbursement|/loans?|settlement|form16|bank.advice|/fnf)", re.I),
    "employee PII": re.compile(r"(employees?|profiles?|directory|personal|candidates?|onboarding|/ess|profile.card|exit/)", re.I),
    "documents": re.compile(r"(documents?|uploads?|attachments?|resumes?|certificates?|/download|/export|/files)", re.I),
    "AI cost/usage": re.compile(r"(ai/[^\s]*(usage|cost|spend)|usage.events|usage.limits|ai.agents)", re.I),
}

INTENTIONAL_PUBLIC = {
    f"{settings.API_V1_STR}/auth/login",
    f"{settings.API_V1_STR}/auth/refresh",
    f"{settings.API_V1_STR}/auth/mfa/verify",
}


def walk_dependencies(dependant, seen=None) -> list[object]:
    """Return every FastAPI dependency (including nested) for a route."""
    if dependant is None:
        return []
    seen = seen or set()
    if id(dependant) in seen:
        return []
    seen.add(id(dependant))

    found = []
    for dependency in dependant.dependencies:
        found.append(dependency)
        found.extend(walk_dependencies(dependency, seen))
    return found


def dependency_info(route) -> tuple[list[str], list[str], bool]:
    """Return (auth dependency names, required permissions/roles, has_auth)."""
    names: list[str] = []
    permissions: list[str] = []
    has_auth = False

    for dependency in walk_dependencies(getattr(route, "dependant", None)):
        call = dependency.call
        name = getattr(call, "__name__", type(call).__name__)

        if name == "RequirePermission":
            has_auth = True
            names.append("RequirePermission")
            permissions.extend(sorted(getattr(call, "permissions", set()) or []))
            continue

        if name == "checker" and "require_roles" in (getattr(call, "__module__", "") or ""):
            has_auth = True
            names.append("require_roles")
            roles = []
            closure = getattr(call, "__closure__", None) or ()
            for cell in closure:
                try:
                    value = cell.cell_contents
                except ValueError:
                    continue
                if isinstance(value, (tuple, list, set)) and all(isinstance(v, str) for v in value):
                    roles.extend(value)
            permissions.extend(f"role:{role}" for role in roles)
            continue

        if name in AUTH_DEPENDENCIES:
            has_auth = True
            names.append(name)
            if name == "get_current_active_superuser":
                permissions.append("superuser")
            continue

        # Catch any custom auth dependency not in the known set.
        lowered = name.lower()
        if any(token in lowered for token in ("auth", "current_user", "permission", "role", "tenant")):
            has_auth = True
            names.append(name)

    # De-duplicate while preserving order.
    names = list(dict.fromkeys(names))
    permissions = list(dict.fromkeys(permissions))
    return names, permissions, has_auth


IN_HANDLER_CHECKS = (
    "_require_",
    "_enforce_",
    "_can_view",
    "_can_access",
    "_can_manage",
    "_can_view_contact",
    "_ensure_manager_or_hr",
    "_query_accessible_requests",
    "_perform_action",
    "_rate_limit_directory_search",
    "_to_directory_item",
    "_review_request",
    "_report_task_query",
    "current_user.employee",
    "_safe_upload_path",
    "accessible_project",
    "get_project_for_action",
    "get_task_project_for_action",
    "report_task_distribution",
    "report_cycle_time",
    "report_team_performance",
    "_get_file_for_action",
    "user_has_permission",
    "is_self",
    "current_user.id",
    "current_user.employee.id",
)


def review_outcome(endpoint, risk: str) -> str:
    """Flag whether a route flagged at dependency level scopes access in-handler."""
    if risk == "-":
        return "-"
    try:
        source = inspect.getsource(endpoint) or ""
    except (OSError, TypeError):
        return "REVIEW"
    found = [token for token in IN_HANDLER_CHECKS if token in source]
    return f"handler-scoped ({', '.join(found[:2])})" if found else "REVIEW"


def first_line(value: str | None) -> str:
    if not value:
        return "-"
    line = value.strip().splitlines()[0].strip()
    return line.replace("|", "\\|") if line else "-"


REFERENCE_DATA = re.compile(r"/(filters|categories|cycles)$", re.I)


def risk_level(path: str, auth_names: list[str], has_auth: bool) -> str:
    if REFERENCE_DATA.search(path):
        return "-"
    matched = [label for label, pattern in SENSITIVE_PATTERNS.items() if pattern.search(path)]
    if not matched:
        return "-"
    category = ", ".join(matched)
    if not has_auth:
        return f"HIGH - no auth ({category})"
    if set(auth_names) <= {"get_current_user", "get_current_user_for_asset"}:
        return f"MEDIUM - user-only ({category})"
    return "-"


rows = []
for route in app.routes:
    path = getattr(route, "path", None)
    methods = sorted(getattr(route, "methods", None) or [])
    if not path or not methods:
        continue

    auth_names, permissions, has_auth = dependency_info(route)
    if path in INTENTIONAL_PUBLIC or not path.startswith(settings.API_V1_STR):
        auth_label = "public"
    elif has_auth:
        auth_label = ", ".join(auth_names) or "custom"
    else:
        auth_label = "NONE"

    risk = "-" if auth_label == "public" else risk_level(path, auth_names, has_auth)

    tags = ", ".join(getattr(route, "tags", None) or []) or "-"
    endpoint = getattr(route, "endpoint", None)
    outcome = review_outcome(endpoint, risk)
    summary = first_line(
        getattr(route, "summary", None)
        or getattr(endpoint, "__doc__", None)
        or getattr(endpoint, "__name__", None)
    )

    for method in methods:
        rows.append(
            (method, path, auth_label, ", ".join(permissions) or "-", risk, outcome, tags.replace("|", "\\|"), summary)
        )

rows.sort(key=lambda row: (row[1], row[0]))
flagged = [row for row in rows if row[4] != "-"]
unreviewed = [row for row in flagged if row[5] == "REVIEW"]
lines = [
    "# Route matrix",
    "",
    "Generated from the FastAPI application with all installable apps enabled "
    "(`INSTALLED_APPS=hrms,crm,project_management`) using `app.routes`.",
    "",
    "| Column | Meaning |",
    "| --- | --- |",
    "| Auth dependency | Authentication dependency detected on the route (`NONE` = no auth). |",
    "| Permission required | Permissions or roles required by the dependency; `superuser` for admin-only routes. |",
    "| Risk | Flagged when a route with no auth or only `get_current_user` touches payroll, employee PII, documents, or AI cost/usage data. |",
    "| Review outcome | `handler-scoped` means the endpoint source contains an explicit ownership/permission check; `REVIEW` needs manual confirmation. This is a heuristic, not a proof. |",
    "",
    f"{len(flagged)} of {len(rows)} routes are flagged at dependency level; {len(unreviewed)} still need manual review after source inspection.",
    "",
    "| Method | Path | Auth dependency | Permission required | Risk | Review outcome | Tags | Summary |",
    "| --- | --- | --- | --- | --- | --- | --- | --- |",
]
lines.extend(
    f"| {method} | `{path}` | {auth} | {permissions} | {risk} | {outcome} | {tags} | {summary} |"
    for method, path, auth, permissions, risk, outcome, tags, summary in rows
)

output = Path(__file__).resolve().parents[1] / "docs" / "security" / "route-matrix.md"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {len(rows)} routes ({len(flagged)} flagged, {len(unreviewed)} unreviewed) to {output}")
