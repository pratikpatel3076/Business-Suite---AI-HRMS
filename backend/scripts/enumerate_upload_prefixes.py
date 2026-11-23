"""Enumerate every directory prefix written under ``UPLOAD_DIR``.

The scanner reads backend source only and combines two checks:

1. An AST scan of known producers: ``os.path.join(settings.UPLOAD_DIR, ...)``,
   ``_save_upload(file, folder)``, ``/uploads/`` literals/f-strings, and
   directory creation under the upload root.
2. A canonical inventory verified against source lines, so dynamic prefixes
   (employee id, run id, financial year, organisation id) are printed in full.

It prints the full prefix list, maps every prefix to the rule in
``app/core/upload_auth.py``, and exits non-zero if a producer is unmapped.
PMS attachments use the independent ``PMS_UPLOAD_ROOT`` setting, not
``settings.UPLOAD_DIR``, and are reported separately as out of scope.

Run from the repository root or ``backend/`` with Python 3.12:

    python backend/scripts/enumerate_upload_prefixes.py
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = sorted({*(BACKEND_ROOT / "app").rglob("*.py"), BACKEND_ROOT / "main.py", BACKEND_ROOT / "create_db.py"})

# (stable prefix, printed shape, required source file, required literal marker)
CANONICAL_INVENTORY = (
    ("employee_docs/", "employee_docs/<employee_id>/", "app/api/v1/employees.py", '"employee_docs", str(employee_id)'),
    ("certificates/", "certificates/<employee_id>/", "app/api/v1/documents.py", 'f"certificates/{employee_id}"'),
    ("certificate_imports/", "certificate_imports/", "app/api/v1/documents.py", '"certificate_imports"'),
    ("company_logos/", "company_logos/", "app/api/v1/company.py", '"company_logos"'),
    ("photos/", "photos/", "app/api/v1/employees.py", '"photos"'),
    ("resumes/", "resumes/", "app/api/v1/recruitment.py", '"resumes"'),
    ("tax_proofs/", "tax_proofs/<employee_id>/<financial_year>/", "app/api/v1/tax_declaration.py", '"tax_proofs", str(declaration.employee_id)'),
    ("form16/", "form16/<employee_id>/<financial_year>/", "app/api/v1/form16.py", '"form16", str(employee_id)'),
    ("fnf-settlements/", "fnf-settlements/", "app/api/v1/fnf.py", '"fnf-settlements"'),
    ("probation_letters/", "probation_letters/", "app/api/v1/probation.py", '"probation_letters"'),
    ("exports/payroll/", "exports/payroll/<run_id>/", "app/api/v1/payroll.py", '"exports", "payroll", str(run_id)'),
    ("exports/payroll/payments/", "exports/payroll/<run_id>/payments/", "app/api/v1/payroll.py", '"exports", "payroll", str(run.id), "payments"'),
    ("exports/payroll/statutory_validations/", "exports/payroll/statutory_validations/", "app/api/v1/payroll.py", '"exports", "payroll", "statutory_validations"'),
    ("exports/payroll/bank_advice/", "exports/payroll/<run_id>/bank_advice/", "app/api/v1/payroll_bank_advice.py", '"exports", "payroll", str(run.id), "bank_advice"'),
    ("exports/statutory/", "exports/statutory/", "app/api/v1/statutory.py", '"exports", "statutory"'),
    ("exports/statutory/", "exports/statutory/<run_id>/", "app/api/v1/hrms_compliance_exports.py", '"exports", "statutory", str(run.id)'),
    ("templates/statutory/", "templates/statutory/", "app/api/v1/payroll.py", '"templates", "statutory"'),
    ("payslips/", "payslips/<year>/<month>/", "app/api/v1/payroll.py", '"payslips", str(run.year), str(run.month)'),
    ("crm/quotations/", "crm/quotations/<organization_id|global>/", "app/apps/crm/api/router.py", '"crm", "quotations", str(quotation.organization_id or "global")'),
    ("reports/", "reports/", "app/api/v1/reports.py", 'f"/uploads/reports/'),
    ("documents/", "documents/", "app/main.py", '"documents"'),
)

# Legacy/alternate URL prefixes that are mapped for authorization even though
# current backend code does not write files with these exact roots.
MAPPED_ONLY_PREFIXES = (
    "statutory/",
    "statutory_validations/",
    "templates/",
    "quotations/",
    "bgv/",
    "background_verification/",
    "pms/",
)


def _rule_table() -> dict[str, tuple[str, str]]:
    source = (BACKEND_ROOT / "app" / "core" / "upload_auth.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "PREFIX_RULES" for target in node.targets
        ):
            return dict(ast.literal_eval(node.value))
    raise RuntimeError("PREFIX_RULES not found in app/core/upload_auth.py")


def _matched_rule(prefix: str, rules: dict[str, tuple[str, str]]) -> tuple[str, str] | None:
    matches = [rule_prefix for rule_prefix in rules if prefix.startswith(rule_prefix)]
    return rules[max(matches, key=len)] if matches else None


def _is_upload_dir(node: ast.AST) -> bool:
    return (isinstance(node, ast.Attribute) and node.attr == "UPLOAD_DIR") or (
        isinstance(node, ast.Name) and node.id == "UPLOAD_DIR"
    )


def _dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_dotted_name(node.value)}.{node.attr}"
    return ""


def _stable_segment(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.strip("/")
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            else:
                break
        text = "".join(parts).strip("/")
        return text or None
    return None


def _prefix_from_segments(segments: list[str]) -> str | None:
    stable: list[str] = []
    for segment in segments:
        if not segment or "/" in segment or segment in {".", ".."}:
            break
        stable.append(segment)
    return "/".join(stable) + "/" if stable else None


def _docstring_nodes(tree: ast.AST) -> set[int]:
    """Ignore module/function/class docstrings that mention /uploads/."""
    nodes: set[int] = set()
    for parent in ast.walk(tree):
        if not isinstance(parent, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        body = getattr(parent, "body", [])
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            nodes.add(id(body[0].value))
    return nodes


def _prefix_from_upload_url(node: ast.AST) -> str | None:
    text: str | None = None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        text = node.value
    elif isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            else:
                break
        text = "".join(parts)
    if not text or "/uploads/" not in text or "\n" in text or "`" in text:
        return None
    tail = text.split("/uploads/", 1)[1]
    if not re.match(r"^[A-Za-z0-9_.-]+/", tail):
        return None
    return _prefix_from_segments(tail.split("/"))


def _scan_producers() -> tuple[dict[str, list[str]], list[str]]:
    """Return discovered prefixes with source locations and out-of-scope notes."""
    discovered: dict[str, list[str]] = {}
    notes: list[str] = []

    for path in SOURCE_PATHS:
        source = path.read_text(encoding="utf-8")
        relative = path.relative_to(BACKEND_ROOT).as_posix()
        tree = ast.parse(source)
        docstrings = _docstring_nodes(tree)

        for node in ast.walk(tree):
            if id(node) in docstrings:
                continue
            if isinstance(node, ast.Constant) or isinstance(node, ast.JoinedStr):
                prefix = _prefix_from_upload_url(node)
                if prefix:
                    discovered.setdefault(prefix, []).append(f"{relative}:{node.lineno}")

            if not isinstance(node, ast.Call):
                continue

            call_name = _dotted_name(node.func)
            if call_name.endswith("join") and any(_is_upload_dir(arg) for arg in node.args):
                segments: list[str] = []
                for arg in node.args[1:]:
                    segment = _stable_segment(arg)
                    if segment is None:
                        break
                    segments.append(segment)
                prefix = _prefix_from_segments(segments)
                if prefix:
                    discovered.setdefault(prefix, []).append(f"{relative}:{node.lineno}")

            if call_name == "_save_upload" and len(node.args) >= 2:
                folder = _stable_segment(node.args[1])
                prefix = _prefix_from_segments(folder.split("/")) if folder else None
                if prefix:
                    discovered.setdefault(prefix, []).append(f"{relative}:{node.lineno}")

            if call_name.endswith(("mkdir", "makedirs")) and "PMS_UPLOAD_ROOT" in source:
                note = "PMS attachments use PMS_UPLOAD_ROOT (independent of settings.UPLOAD_DIR)"
                if note not in notes:
                    notes.append(note)

    return discovered, notes


def _verify_inventory(rules: dict[str, tuple[str, str]]) -> tuple[list[tuple[str, str, str, str]], list[str]]:
    verified: list[tuple[str, str, str, str]] = []
    missing: list[str] = []
    for prefix, printed, filename, marker in CANONICAL_INVENTORY:
        path = BACKEND_ROOT / filename
        lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
        line_number = next((number for number, line in enumerate(lines, 1) if marker in line), None)
        if line_number is None:
            missing.append(f"{prefix}: marker {marker!r} not found in {filename}")
            continue
        rule = _matched_rule(prefix, rules)
        if rule is None:
            missing.append(f"{prefix}: no rule in PREFIX_RULES")
            continue
        verified.append((prefix, printed, rule[1], f"{filename}:{line_number}"))
    return verified, missing


def main() -> None:
    rules = _rule_table()
    discovered, notes = _scan_producers()
    verified, problems = _verify_inventory(rules)

    canonical_prefixes = {prefix for prefix, _, _, _ in verified}
    all_prefixes = sorted(set(discovered) | canonical_prefixes | set(MAPPED_ONLY_PREFIXES))

    print("UPLOAD PREFIX INVENTORY")
    print(f"Scanned {len(SOURCE_PATHS)} backend Python files.\n")

    print("EVERY PREFIX WRITTEN UNDER UPLOAD_DIR -> RULE")
    for prefix, printed, description, evidence in verified:
        print(f"  {printed:<45} {description:<46} [{evidence}]")

    print("\nMAPPED-ONLY / LEGACY PREFIXES -> RULE")
    for prefix in MAPPED_ONLY_PREFIXES:
        rule = _matched_rule(prefix, rules)
        description = rule[1] if rule else "DENY (unmapped)"
        print(f"  {prefix:<45} {description}")

    print("\nAUTOMATICALLY DISCOVERED PRODUCER PREFIXES")
    for prefix in sorted(discovered):
        rule = _matched_rule(prefix, rules)
        description = rule[1] if rule else "DENY (unmapped)"
        locations = ", ".join(sorted(set(discovered[prefix]))[:5])
        print(f"  {prefix:<45} {description:<46} [{locations}]")

    unmapped = sorted(
        prefix for prefix in all_prefixes if _matched_rule(prefix, rules) is None
    )
    print("\nUNMAPPED PREFIXES (denied by default)")
    print("  none" if not unmapped else "\n".join(f"  {prefix}" for prefix in unmapped))

    print("\nNOTES")
    for note in notes:
        print(f"  {note}")
    print("  Bare /uploads/ paths with no literal prefix (e.g. /uploads/{rel}) are")
    print("  signed only after the resolved relative path passes the same rules.")

    if unmapped or problems:
        print("\nINVENTORY ERRORS")
        for problem in problems:
            print(f"  {problem}")
        for prefix in unmapped:
            print(f"  unmapped producer prefix: {prefix}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
