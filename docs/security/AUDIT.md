# Security audit

This document records the security review of the FastAPI backend and React frontend on branch `chore/security-hardening`.

Status values:

- **Fixed (targeted tests pass; full suite not run on final tree)** — code and targeted tests are committed, but the complete backend suite has not completed against the final tree. This is not a claim of full-suite validation.
- **Unverified** — the control or claim was not confirmed by a reproducible check; it is recorded as open, not closed.
- **Verified** — the control already exists and was confirmed by tests or reproducible checks.
- **Verified (residual risk)** — upgrades were applied; remaining advisories have no applicable upstream fix or are not reachable in this application. These are accepted risks, not claims of a fix.
- **Deferred** — intentionally postponed until the user supplies the required input.

## Findings

| # | Finding | Severity | Status | Evidence / remediation | Commit |
| --- | --- | --- | --- | --- | --- |
| 1 | Demo users, well-known admin credentials, and sample CRM data were created by default and existing users were reset on every startup | Critical | Fixed (targeted tests pass; full suite not run on final tree) | Demo seeding is opt-in via `SEED_DEMO_DATA`, blocked in production, existing user privileges/password hashes are preserved, and production bootstrap uses `scripts/create_admin.py`. Added `tests/test_seed_gating.py` (targeted: 14 passed). | 6004e37 |
| 2 | Uploaded files were served by an unauthenticated `StaticFiles` mount at `/uploads/*` | High | Fixed (targeted tests pass; full suite not run on final tree) | Mount removed. Files served from `/api/v1/uploads/*` behind `get_current_user_for_asset`, with absolute-path, traversal, and symlink checks. Native browser requests pass a token in the query string; values are redacted from audit logs. Added `tests/test_secure_uploads.py` (targeted: 14 passed). | 22fa128 |
| 3 | `ingest_vendor_webhook` and the CRM calendar webhook were unauthenticated | High | Fixed (targeted tests pass; full suite not run on final tree) | Shared HMAC-SHA256 verifier over raw body with a `<timestamp>.<body>` signed message, `hmac.compare_digest`, 5-minute replay window, and 401 on failure. BGV secrets are encrypted at rest and never returned by the API. CRM calendar webhook is disabled by default and signature-verified when enabled. Added `tests/test_webhook_signatures.py` (targeted: 10 passed). Vendor-algorithm compatibility is **not** verified — see verification gaps. | 3b3cae4, bd2da92 |
| 4 | `SECRET_KEY`/`REFRESH_SECRET_KEY` were per-process random values; CRM/PM encryption keys were derived from `SECRET_KEY` | High | Fixed (targeted tests pass; full suite not run on final tree) | Production requires explicit, >=32 char, distinct, non-placeholder `SECRET_KEY`, `REFRESH_SECRET_KEY`, and `ENCRYPTION_KEY`; startup raises on violation. Shared `app.core.encryption` derives Fernet keys from `ENCRYPTION_KEY` with `ENCRYPTION_KEY_PREVIOUS` rotation. Documented in `docs/security/SECRETS.md`. Added `tests/test_secret_configuration.py` (targeted: 7 passed). | e078a89 |
| 5 | Authentication endpoints had no request rate limiting despite `slowapi` and `RATE_LIMIT_PER_MINUTE` being configured | High | Fixed (targeted tests pass; full suite not run on final tree) | Shared `app.core.rate_limit` limiter, disabled in tests; login, MFA verify, and refresh use `@limiter.limit(RATE_LIMIT_PER_MINUTE/minute)`. Added `tests/test_auth_limits.py`. | 563cc80 |
| 6 | CORS configuration is overly permissive (`allow_methods=*`, `allow_headers=*`) | Medium | Fixed (targeted tests pass; full suite not run on final tree) | Explicit method and header allowlists in `app/main.py`; production origins already required to be explicit. Covered by `tests/test_auth_limits.py`. | 0d91e9d |
| 7 | CRM tenant-isolation test failed under the default test environment | Medium | Verified (targeted run; app list now fixed in test config) | Reopened and re-run explicitly with `INSTALLED_APPS=hrms,crm,project_management`: `tests/test_crm_rest_api.py::test_crm_leads_crud_is_scoped_to_current_organization` — 1 passed (26.86s). No tenant-isolation defect was reproduced. `backend/tests/conftest.py` now sets that app list as the test default so the router is always registered and the test cannot 404 silently. | — (test config) |
| 8 | Frontend token storage, JWT `type`/`exp` enforcement, and refresh-token rotation/revocation | High | Fixed (targeted tests pass; full suite not run on final tree) | Refresh token moved to an HttpOnly cookie; access token kept in memory; JWT `exp` and `type` enforced; refresh tokens rotated and revoked through `UserSession`. See task 8 review below. The new migration is **not** verified on MySQL — see verification gaps. | d07e9cb, 952a4df |
| 9 | Route inventory for access-control review | Informational | Unverified | `docs/security/route-matrix.md` regenerates from `app.routes` with all apps enabled (870 routes, 96 dependency-level flags, 0 unreviewed). The earlier 96-flag review predates the FastAPI upgrade and has not been revalidated against the current route set. See task 9 review notes. | a606ffa, bd2da92 |
| 10 | Dependency vulnerabilities in Python and npm dependency trees | High | Verified (residual risk) | `pip-audit` fell from 162 findings in 13 packages to 3: `pypdf2` (stale local venv install only; no longer declared), `ecdsa 0.19.2` (Minerva timing issue; no upstream fix), and `python-jose 3.5.0` (asymmetric-key HMAC validation; app only uses HS256 with server-controlled secrets, no asymmetric key input). `npm audit` fell from 24 findings to 0. See residual-risk note below. | 3ee5fbc |
| 11 | Frontend production build has not been verified after security changes | Medium | Verified | `npm run build` succeeds with Vite 8.3.8 and React Router 7.18.6 after adapting the Vite config and axios mutation typing. | 3ee5fbc |
| 12 | Product naming still contains the old project name | Low | Deferred | Skipped by user; rename will be handled in a separate run. | — |

## Task 8 — auth surface review (report before fixes)

| Area | Observation | Assessment | Action |
| --- | --- | --- | --- |
| Frontend token storage | `authStore` used Zustand `persist`, writing `accessToken` and `refreshToken` to `localStorage`. | Clear issue: any XSS can exfiltrate long-lived refresh credentials. | Refresh token now set only as an HttpOnly, Secure (production), SameSite=Strict cookie scoped to `/api/v1/auth`; access token is held in memory only. `bootstrapAuth()` exchanges the cookie on page load. Split-origin deployments must proxy `/api` through the frontend origin or deliberately relax to `SameSite=None` with `Secure` (also requires `withCredentials`, already set). |
| JWT `type` claim | Access/refresh tokens set `type`; `verify_access_token`/`verify_refresh_token` check it. `jwt.decode` did not force `exp`. MFA tokens used only a `scope` claim. | `type` was enforced; `exp` requirement was missing. MFA tokens had no `type`. | `verify_token` now uses `options={"require_exp": True}`; MFA tokens carry `type="mfa"` verified alongside `scope`. Refresh tokens carry `jti`/`sid`. |
| Refresh rotation/revocation | `/auth/refresh` issued a new refresh token without checking or revoking the old one. `UserSession` was unused; `/auth/logout` was a no-op. | Clear issue: stolen refresh tokens remained valid forever and logout could not revoke them. | Refresh tokens carry `jti`/`sid`; `UserSession.session_id` stores the `jti` and `session_token_hash` stores the SHA-256 of the active token. Refresh validates both and marks the old session `Rotated`; logout revokes the session and clears the cookie. Migration `20260513_034_user_session_refresh_tokens.py` adds the column. |

## Task 9 — route matrix review notes (unverified)

`docs/security/route-matrix.md` lists every route with its auth dependency and required permission. It currently reports 870 routes and 96 dependency-level flags. The generator was repaired in `bd2da92` to traverse the nested `_IncludedRouter` objects introduced by the FastAPI upgrade and to accumulate `include_context.prefix`, restoring byte-for-byte parity with the committed matrix.

That parity check only proves the generator reproduces the *previous* output. The substantive review of those 96 flags was performed before the dependency upgrade and has **not** been revalidated against the current route set, so the conclusion below is recorded as unverified:

- Previously reviewed categories: AI Agents (37 routes), employee directory/org-search, payroll/Form 16/F&F/tax-proof/payslip downloads, profile change requests/probation, project-management files/attachments/reports, uploads, and reference data.
- Previously claimed in-handler controls: `_require_ai_access`, `_to_directory_item`, `_enforce_access`, `_enforce_view_access`, `accessible_project_query`, `_safe_upload_path`, and related helpers.
- Previous conclusion: 0 fully unauthenticated sensitive routes. **This conclusion is not currently verified.**

A differential review (old vs new by method, path, dependencies) is the appropriate next step; a full re-review of all 96 flags has not been performed.

## Task 10 — residual dependency advisories

- `pypdf2 3.0.1 / PYSEC-2026-1835` — a fix exists in `pypdf`, which is now the declared dependency and is used directly. The reported package remains only in the local virtual environment from an earlier install; it is not in `backend/requirements.txt`.
- `ecdsa 0.19.2 / PYSEC-2026-1325` — no fixed release is available. The vulnerable `sign_digest()` path is not used by this application.
- `python-jose 3.5.0 / PYSEC-2026-4298` — no fixed release is available. Tokens are signed and verified with HS256 using server-controlled secrets; the application never accepts DER/PEM/SSH asymmetric keys as HMAC secrets. An attacker able to replace `SECRET_KEY` already controls token issuance.

These findings are accepted and documented; no advisory is claimed as fixed without an upstream release.

## Verification gaps

These are explicit, open gaps. None is claimed as fixed or validated:

1. **Full suite never completed on the final tree.** The last completed full run was against a tree before `952a4df` and `bd2da92` and ended 192 passed / 5 failed. Those five failures were the `_IncludedRouter` route-inspection crash, subsequently fixed and checked only by targeted webhook tests (10 passed). No complete full-suite result exists for the final tree.
2. **No MySQL test of the `UserSession` migration.** `20260513_034_user_session_refresh_tokens.py` has only been exercised implicitly against SQLite in-memory `Base.metadata.create_all` in tests. It has not been applied with Alembic against MySQL, including upgrade/downgrade/upgrade.
3. **CRM webhook signature verified only with our own signer.** Tests generate signatures with `app.core.webhooks.sign_webhook_body`. The CRM vendor's documented signature algorithm, header names, and payload canonicalisation have not been checked against real vendor documentation or a recorded fixture. The disable-by-default feature flag is tested; real-vendor compatibility is not.

## Validation log

- `cd backend && pytest -q tests/test_seed_gating.py tests/test_auth.py` (task 1 targeted) — 14 passed.
- `cd backend && pytest -q tests/test_secure_uploads.py --tb=short` (task 2 targeted) — 14 passed.
- `cd backend && pytest -q tests/test_webhook_signatures.py --tb=short` (task 3 targeted) — 10 passed.
- `cd backend && pytest -q tests/test_secret_configuration.py --tb=short` (task 4 targeted) — 7 passed.
- `INSTALLED_APPS=hrms,crm,project_management pytest -q --timeout=60 --durations=25 tests/test_crm_rest_api.py::test_crm_leads_crud_is_scoped_to_current_organization` — 1 passed in 26.86s (log: `C:\Users\prati\AppData\Local\Temp\opencode\crm_tenant_test.log`).
- `cd backend && pytest -q tests/test_auth.py tests/test_auth_hardening.py tests/test_auth_limits.py` (final auth group) — 23 passed; 203 pre-existing Pydantic v1-style deprecation warnings, no failures.
- `INSTALLED_APPS=hrms,crm,project_management python backend/generate_route_matrix.py` — 870 routes, 96 flagged, 0 unreviewed; after `bd2da92` the generator reproduces the committed matrix byte-for-byte.
- `cd backend && pip-audit` after upgrades — 3 residual advisories (down from 162), all documented as accepted residual risk above.
- `cd frontend && npm audit` after upgrades — 0 vulnerabilities (down from 24).
- `cd frontend && npm run build` — succeeded with Vite 8.3.8 and React Router 7.18.6.
- Baseline before changes: 9 pre-existing failures under the default environment.
- Regressions found in the pre-final full run and fixed in `952a4df`: `pypdf` 7 removed `PdfMerger` (Form 16 merge now uses `PdfWriter`), the existing BGV module test posted an unsigned webhook (now signed), and the JWT rotation test omitted the now-required `exp` claim.
- Post-fix targeted re-runs: Form 16 and BGV module tests — 2 passed; `tests/test_security_hardening.py` — 4 passed.
- FastAPI nested-router artifact fixed in `bd2da92`; webhook suite re-run — 10 passed.
- No full-suite result on the final tree is recorded in this section.
