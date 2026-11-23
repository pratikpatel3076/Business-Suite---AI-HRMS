# Security audit

This document records the security review of the FastAPI backend and React frontend on branch `chore/security-hardening`.

Status values:

- **Fixed (full suite passed)** — code, targeted tests, and one complete backend-suite run on the final tree all passed. See the validation log for the command, result, and log path.
- **Unverified** — the control or claim was not confirmed by a reproducible check; it is recorded as open, not closed.
- **Verified** — the control already exists and was confirmed by tests or reproducible checks.
- **Verified (residual risk)** — upgrades were applied; remaining advisories have no applicable upstream fix or are not reachable in this application. These are accepted risks, not claims of a fix.
- **Deferred** — intentionally postponed until the user supplies the required input.

## Findings

| # | Finding | Severity | Status | Evidence / remediation | Commit |
| --- | --- | --- | --- | --- | --- |
| 1 | Demo users, well-known admin credentials, and sample CRM data were created by default and existing users were reset on every startup | Critical | Fixed (full suite passed) | Demo seeding is opt-in via `SEED_DEMO_DATA`, blocked in production, existing user privileges/password hashes are preserved, and production bootstrap uses `scripts/create_admin.py`. Added `tests/test_seed_gating.py` (targeted: 14 passed). | 6004e37 |
| 2 | Uploaded files were served by an unauthenticated `StaticFiles` mount at `/uploads/*` | High | Fixed (full suite passed) | Mount removed. Files served from `/api/v1/uploads/*` behind authentication, ownership/permission checks, and absolute-path, traversal, and symlink checks. Native browser requests use 60-second signed single-path URLs issued by an authenticated endpoint; no access token appears in a query string. Added `tests/test_secure_uploads.py` and later follow-up tests. | 22fa128, a5a9c6c, (item 2) |
| 3 | `ingest_vendor_webhook` and the CRM calendar webhook were unauthenticated | High | Fixed (full suite passed) | Shared HMAC-SHA256 verifier over raw body with a `<timestamp>.<body>` signed message, `hmac.compare_digest`, 5-minute replay window, and 401 on failure. BGV secrets are encrypted at rest and never returned by the API. CRM calendar webhook is disabled by default and signature-verified when enabled. Added `tests/test_webhook_signatures.py` (targeted: 10 passed). Vendor-algorithm compatibility is **not** verified — see verification gaps. | 3b3cae4, bd2da92 |
| 4 | `SECRET_KEY`/`REFRESH_SECRET_KEY` were per-process random values; CRM/PM encryption keys were derived from `SECRET_KEY` | High | Fixed (full suite passed) | Production requires explicit, >=32 char, distinct, non-placeholder `SECRET_KEY`, `REFRESH_SECRET_KEY`, and `ENCRYPTION_KEY`; startup raises on violation. Shared `app.core.encryption` derives Fernet keys from `ENCRYPTION_KEY` with `ENCRYPTION_KEY_PREVIOUS` rotation. Documented in `docs/security/SECRETS.md`. Added `tests/test_secret_configuration.py` (targeted: 7 passed). | e078a89 |
| 5 | Authentication endpoints had no request rate limiting despite `slowapi` and `RATE_LIMIT_PER_MINUTE` being configured | High | Fixed (full suite passed) | Shared `app.core.rate_limit` limiter, disabled in tests; login, MFA verify, and refresh use `@limiter.limit(RATE_LIMIT_PER_MINUTE/minute)`. Added `tests/test_auth_limits.py`. | 563cc80 |
| 6 | CORS configuration is overly permissive (`allow_methods=*`, `allow_headers=*`) | Medium | Fixed (full suite passed) | Explicit method and header allowlists in `app/main.py`; production origins already required to be explicit. Covered by `tests/test_auth_limits.py`. | 0d91e9d |
| 7 | CRM tenant-isolation test failed under the default test environment | Medium | Verified (targeted run; app list now fixed in test config) | Reopened and re-run explicitly with `INSTALLED_APPS=hrms,crm,project_management`: `tests/test_crm_rest_api.py::test_crm_leads_crud_is_scoped_to_current_organization` — 1 passed (26.86s). No tenant-isolation defect was reproduced. `backend/tests/conftest.py` now sets that app list as the test default so the router is always registered and the test cannot 404 silently. | — (test config) |
| 8 | Frontend token storage, JWT `type`/`exp` enforcement, and refresh-token rotation/revocation | High | Fixed (full suite passed) | Refresh token moved to an HttpOnly cookie; access token kept in memory; JWT `exp` and `type` enforced; refresh tokens rotated and revoked through `UserSession`. See task 8 review below. The new migration is **not** verified on MySQL — see verification gaps. | d07e9cb, 952a4df |
| 9 | Route inventory for access-control review | Informational | Unverified | `docs/security/route-matrix.md` regenerates from `app.routes` with all apps enabled (870 routes, 96 dependency-level flags, 0 unreviewed). The earlier 96-flag review predates the FastAPI upgrade and has not been revalidated against the current route set. See task 9 review notes. | a606ffa, bd2da92 |
| 10 | Dependency vulnerabilities in Python and npm dependency trees | High | Verified (residual risk) | `pip-audit` fell from 162 findings in 13 packages to 3: `pypdf2` (stale local venv install only; no longer declared), `ecdsa 0.19.2` (Minerva timing issue; no upstream fix), and `python-jose 3.5.0` (asymmetric-key HMAC validation; app only uses HS256 with server-controlled secrets, no asymmetric key input). `npm audit` fell from 24 findings to 0. See residual-risk note below. | 3ee5fbc |
| 11 | Frontend production build has not been verified after security changes | Medium | Verified | `npm run build` succeeds with Vite 8.3.8 and React Router 7.18.6 after adapting the Vite config and axios mutation typing. | 3ee5fbc |
| 12 | Product naming still contains the old project name | Low | Deferred | Skipped by user; rename will be handled in a separate run. | — |

## Follow-up hardening pass

Statuses below describe the current follow-up pass only. Each item is committed separately; the final full-suite result is recorded in item 9.

| # | Item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Upload URL prefix authorization | Fixed (targeted tests pass) | See below. |
| 2 | Signed single-path asset URLs; remove `?token=`; 15-minute access tokens | Fixed (targeted tests pass; frontend build passes) | See below. |
| 3 | Alembic-only schema changes in production | Fixed (targeted tests pass) | See below. |
| 4 | Environment allowlist and cookie/logging safety | Fixed (targeted tests pass) | See below. |
| 5 | Rate limiting per IP + email, Redis storage, proxy docs | Fixed (targeted tests pass) | See below. |
| 6 | Refresh/logout origin checks and rotated-token reuse revocation | Fixed (targeted tests pass; frontend build passes) | See below. |
| 7 | CI, Docker, ruff, SECURITY.md, .env.example | Fixed (configs validated locally; remote CI not run) | See below. |
| 8 | Release notes for session invalidation | Fixed (docs added) | See below. |
| 9 | Final full suite | Fixed (full suite passed) | See below. |

### Item 1 — upload authorization

Stored URLs are now checked against an explicit prefix allowlist in `app/core/upload_auth.py`; **unmapped prefixes are denied for every user, including admins and HR**. Employee documents and certificates resolve the owning employee from the DB row (`EmployeeDocument`, `EmployeeCertificate`, `GeneratedDocument`, education/experience URLs, profile photo) with a path-id fallback, and allow only the owner, HR (`employee_sensitive_view`), or an admin. Payroll/statutory/F&F exports require `payroll_view`; resumes and BGV reports require `recruitment_view`/`recruitment_manage`. Low-sensitivity directory images and explicitly mapped module prefixes have their own rules. `tests/test_upload_authorization.py` covers employee A vs employee B, owner access, HR access, unmapped prefixes, and permission-gated prefixes. Targeted run with `tests/test_secure_uploads.py`: **25 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item1_uploads.log`).

### Item 2 — signed asset URLs

`get_current_user_for_asset` no longer accepts a `?token=` access token. Authenticated callers use `POST /api/v1/uploads/sign`, which re-runs the item 1 authorization and returns a 60-second HMAC-SHA256 URL bound to one exact stored path (`app/core/asset_urls.py`). The download route accepts either a Bearer token with authorization or a valid `expires`/`sig` pair; expired, tampered, or path-mismatched signatures return 403. `ACCESS_TOKEN_EXPIRE_MINUTES` now defaults to 15. `frontend/src/lib/secureAssetUrl.ts` signs paths through the API and caches them for 55 seconds; existing callers keep the same synchronous hook API and never put tokens in URLs. `npm run build` succeeded. Targeted run: **33 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item2_signed.log`).

### Item 3 — Alembic-only schema in production

`local_schema_management_enabled()` in `app/core/config.py` gates schema work to `ENVIRONMENT in {"development", "test"}`. The startup lifespan now calls `Base.metadata.create_all`, `ensure_crm_schema`, and `ensure_pms_schema` only under that flag; production relies entirely on Alembic. Demo CRM seeding is likewise skipped outside local environments. `tests/test_startup_schema.py` asserts the flag values and that a production lifespan makes no schema calls (development makes them). Targeted run with the secret-configuration suite: **14 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item3_startup.log`).

### Item 4 — environment safety

`ENVIRONMENT` now defaults to `production`, is restricted to `development`/`test`/`production`, and `ENVIRONMENT=test` is rejected outside pytest. The refresh cookie is `Secure` in every environment except local development; the test `TestClient` uses an https base URL so it still exercises the cookie flow. `AuditLogMiddleware._log_request` now logs persistence and token-parsing failures with `logger.exception` instead of swallowing them silently, and redacts `sig` alongside token parameters. `tests/test_environment_safety.py` covers the default, invalid values, the pytest guard, cookie flags, and error logging. Targeted run with the auth suites: **40 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item4_environment.log`).

### Item 5 — auth rate limiting

`app/core/rate_limit.py` now defines fixed limits: login and `POST /api/v1/auth/mfa/verify` are each `5/minute` **both** per source IP (default key) and per account (`get_email_key` for login, `get_mfa_subject_key` for the MFA token subject); `POST /api/v1/auth/refresh` is `30/minute` per IP. Counters use `storage_uri=settings.REDIS_URL`; the in-memory fallback is enabled only when `ENVIRONMENT=development`, so test and production fail closed if Redis is unavailable. The obsolete `RATE_LIMIT_PER_MINUTE` setting was removed from config and `.env.example`. `docs/deployment_split_frontend_backend.md` now documents `--proxy-headers`/`--forwarded-allow-ips` with trusted proxy CIDRs, and the new `backend/Dockerfile` starts Uvicorn with those flags and a `FORWARDED_ALLOW_IPS` override. `tests/test_auth_limits.py` covers constants, route wiring, Redis/fallback config, normalized key funcs, and per-IP/per-account 429 behavior with an isolated in-memory limiter. Targeted run with the auth/environment suites: **37 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item5_rate_limits.log`).

### Item 6 — refresh cookie CSRF defenses

`POST /api/v1/auth/refresh` and `POST /api/v1/auth/logout` now call `_verify_cookie_auth_request`, which requires an `Origin` (or parsed `Referer`) exactly matching `BACKEND_CORS_ORIGINS` plus the `X-CSRF-Token: hrms-app` custom header. Wildcard origins are rejected. The refresh endpoint no longer accepts `refresh_token` from the request body; the token is read only from the HttpOnly cookie. The frontend sends the CSRF header on every API request and the backend CORS allowlist includes `X-CSRF-Token`. `docs/deployment_split_frontend_backend.md` documents the cross-site case: `SameSite=None; Secure` must not be adopted without the origin allowlist and CSRF header, and the cookie policy remains `Strict` by default.

Replaying a rotated refresh token now finds the `Rotated` session row and revokes **every** active `UserSession` for that user before returning 401. `tests/test_auth_hardening.py` covers missing/unlisted origins, Referer fallback, missing CSRF header, body-token rejection, logout checks, and rotated-token replay revoking a second independent session. Targeted run: **33 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item6_csrf.log`).

### Item 7 — CI, containers, lint config, and policy docs

Added `.github/workflows/ci.yml` with two jobs. The backend job installs pinned requirements, runs `ruff check .`, runs the full pytest suite with `ENVIRONMENT: test`, performs an Alembic round trip against a MySQL 8 service container (`upgrade head` → `downgrade -1` → `upgrade head`), and runs `pip-audit -r requirements.txt` with only the two documented advisories ignored by ID so new findings still fail CI. The frontend job runs `npm ci`, `npm run build`, and `npm audit --audit-level=moderate`.

Added root `ruff.toml` (critical error/undefined-name rules only) and pinned `ruff`/`pip-audit` in `backend/requirements.txt` so local and CI checks use the same versions. Added `backend/Dockerfile` (proxy-header Uvicorn command, now with an entrypoint), `backend/docker-entrypoint.sh` (optional `RUN_MIGRATIONS_ON_START`), `backend/.dockerignore`, `frontend/Dockerfile`, `frontend/nginx.conf` (SPA fallback plus `/api/` proxy with forwarded headers), and root `docker-compose.yml` with `api`, `mysql`, `redis`, and `web` services plus health checks and persistent volumes. `backend/.env.example` now documents all three signing/encryption keys and their previous-key rotation values, `SEED_DEMO_DATA`, `REDIS_URL`, the 15-minute access token, and the fact that demo fixtures are ignored in production. `SECURITY.md` records the reporting process, mandatory deployment controls, and accepted residual risks.

Remote GitHub Actions was **not** executed because nothing was pushed. Local validation: `docker compose config --quiet` passed, both YAML files parsed with `yaml.safe_load`, `ruff check .` passed, the exact `pip-audit` command returned `No known vulnerabilities found, 3 ignored`, and `npm audit --audit-level=moderate` returned `0 vulnerabilities`. Docker image builds and the MySQL migration round trip were not run locally because the Docker daemon is unavailable; the round trip is now an explicit CI step.

### Item 8 — release notes

Added `docs/RELEASE_NOTES.md` with an explicit deployment notice: all existing sessions are invalidated on deploy because refresh tokens now require a `jti` claim and a matching `UserSession` row, so users must sign in again. The same operational note is included in `SECURITY.md`.

### Item 9 — final full suite

One final backend-suite run was executed on the completed hardening tree with `INSTALLED_APPS=hrms,crm,project_management` and `ENVIRONMENT=test`: `pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25` — **245 passed, 0 failed, 307 warnings in 207.29s (0:03:27)**. Log: `C:\Users\prati\AppData\Local\Temp\opencode\full_suite_hardening.log`. The shell wrapper reports exit code 1 because PowerShell's `*>` stream redirect writes native stderr as error records; the pytest summary line records the pass. This is the only full-suite run for this follow-up pass; earlier item validations were targeted only.

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

1. **RESOLVED — full suite completed on the final tree.** Earlier full runs ended 192 passed / 5 failed against pre-fix trees (the `_IncludedRouter` route-inspection crash). After `952a4df`, `bd2da92`, the test-config fix, the middleware speed fix, and the matrix sanity checks, the single final full run passed 200 / 200 in 194.87s. See the validation log for the log path.
2. **Unverified on MySQL: no MySQL test of the `UserSession` migration.** `20260513_034_user_session_refresh_tokens.py` has only been exercised implicitly against SQLite in-memory `Base.metadata.create_all` in tests. It has not been applied with Alembic against MySQL, including upgrade/downgrade/upgrade. Docker CLI 29.8.1 is installed but the Docker daemon is not running (`npipe:////./pipe/dockerDesktopLinuxEngine` unavailable), so no MySQL container could be started. `alembic heads` reports exactly one head, `20260513_034`.
3. **CRM webhook signature verified only with our own signer.** Tests generate signatures with `app.core.webhooks.sign_webhook_body`. The CRM vendor's documented signature algorithm, header names, and payload canonicalisation have not been checked against real vendor documentation or a recorded fixture. The disable-by-default feature flag is tested; real-vendor compatibility is not.

## Validation log

- `cd backend && pytest -q tests/test_seed_gating.py tests/test_auth.py` (task 1 targeted) — 14 passed.
- `cd backend && pytest -q tests/test_secure_uploads.py --tb=short` (task 2 targeted) — 14 passed.
- `cd backend && pytest -q tests/test_webhook_signatures.py --tb=short` (task 3 targeted) — 10 passed.
- `cd backend && pytest -q tests/test_secret_configuration.py --tb=short` (task 4 targeted) — 7 passed.
- `INSTALLED_APPS=hrms,crm,project_management pytest -q --timeout=60 --durations=25 tests/test_crm_rest_api.py::test_crm_leads_crud_is_scoped_to_current_organization` — 1 passed in 26.86s (log: `C:\Users\prati\AppData\Local\Temp\opencode\crm_tenant_test.log`).
- `cd backend && pytest -q tests/test_auth.py tests/test_auth_hardening.py tests/test_auth_limits.py` (final auth group) — 23 passed; 203 pre-existing Pydantic v1-style deprecation warnings, no failures.
- `INSTALLED_APPS=hrms,crm,project_management python backend/generate_route_matrix.py` (run from the repo root) — 870 routes, 96 flagged, 0 unreviewed; output is byte-identical to the committed matrix.
- `pytest -q --timeout=60 --durations=25 tests/test_route_matrix_generator.py` — 3 passed. Sanity checks cover `/api/v1` prefix preservation, >0 flagged routes, and classification of `/api/v1/auth/login` as public and `GET /api/v1/payroll/runs` as permission-protected.
- Differential review of committed matrix vs regenerated matrix keyed by `(method, path, auth dependencies)`: 866 unique keys in each, 0 added, 0 removed, 0 dependency changes. No rows changed, so no additional row-level review was required; the earlier 96-flag substantive review has still not been redone.
- `cd backend && pip-audit` after upgrades — 3 residual advisories (down from 162), all documented as accepted residual risk above.
- `cd frontend && npm audit` after upgrades — 0 vulnerabilities (down from 24).
- `cd frontend && npm run build` — succeeded with Vite 8.3.8 and React Router 7.18.6.
- Baseline before changes: 9 pre-existing failures under the default environment.
- Regressions found in the pre-final full run and fixed in `952a4df`: `pypdf` 7 removed `PdfMerger` (Form 16 merge now uses `PdfWriter`), the existing BGV module test posted an unsigned webhook (now signed), and the JWT rotation test omitted the now-required `exp` claim.
- Post-fix targeted re-runs: Form 16 and BGV module tests — 2 passed; `tests/test_security_hardening.py` — 4 passed.
- FastAPI nested-router artifact fixed in `bd2da92`; webhook suite re-run — 10 passed.
- Suite slowness diagnosis: `pytest --collect-only -q` reports 197 tests in 0.26s. A fixed five-test sample (auth login, auth refresh, CRM tenant isolation, Form 16, PMS project access) took **64.79s** before the fix (logs: `C:\Users\prati\AppData\Local\Temp\opencode\sample_before.log`), with ~4.5s setup and ~4s per HTTP call. `AuditLogMiddleware` opened `SessionLocal()` on every request; in tests that points at an absent MySQL server and each connection attempt cost ~4.08s before the exception was swallowed. No test depends on middleware-generated audit rows (fixtures insert them directly), so persistence is skipped when `ENVIRONMENT=test`. The same five tests then took **3.90s**, all passing (`C:\Users\prati\AppData\Local\Temp\opencode\sample_after.log`). Production audit logging is unchanged.
- `alembic heads` — single head `20260513_034`. MySQL upgrade/downgrade/upgrade could not be executed: Docker daemon unavailable.
- **Prior full suite** (before the follow-up hardening pass): `cd backend && pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25` with `INSTALLED_APPS=hrms,crm,project_management` — **200 passed, 0 failed, 307 warnings in 194.87s (0:03:14)**. Log: `C:\Users\prati\AppData\Local\Temp\opencode\full_suite_final.log`. The shell wrapper reports exit code 1 because PowerShell's `*>` stream redirect writes native stderr as error records; the pytest log itself records 200 passed and no failures.
- Follow-up item 1: `pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25 tests/test_upload_authorization.py tests/test_secure_uploads.py` — **25 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item1_uploads.log`).
- Follow-up item 2: `pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25 tests/test_signed_asset_urls.py tests/test_upload_authorization.py tests/test_secure_uploads.py` — **33 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item2_signed.log`); `npm run build` succeeded (`C:\Users\prati\AppData\Local\Temp\opencode\item2_frontend_build.log`).
- Follow-up item 3: `pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25 tests/test_startup_schema.py tests/test_secret_configuration.py` — **14 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item3_startup.log`).
- Follow-up item 4: `pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25 tests/test_environment_safety.py tests/test_secret_configuration.py tests/test_startup_schema.py tests/test_auth.py tests/test_auth_hardening.py` — **40 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item4_environment.log`).
- Follow-up item 5: `pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25 tests/test_auth_limits.py tests/test_auth.py tests/test_auth_hardening.py tests/test_environment_safety.py` — **37 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item5_rate_limits.log`).
- Follow-up item 6: `pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25 tests/test_auth_hardening.py tests/test_auth.py tests/test_auth_limits.py` — **33 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item6_csrf.log`); `npm run build` succeeded (`C:\Users\prati\AppData\Local\Temp\opencode\item6_frontend_build.log`).
- Follow-up item 7 local config validation: `docker compose config --quiet` passed; `yaml.safe_load` parsed `.github/workflows/ci.yml` and `docker-compose.yml`; `ruff check .` passed; `pip-audit -r requirements.txt --ignore-vuln PYSEC-2026-1325 --ignore-vuln PYSEC-2026-4298` reported `No known vulnerabilities found, 3 ignored`; `npm audit --audit-level=moderate` reported `0 vulnerabilities`.
- Follow-up item 8: `docs/RELEASE_NOTES.md` added with the session-invalidation notice.
- Follow-up item 9 (final, run once): `INSTALLED_APPS=hrms,crm,project_management ENVIRONMENT=test pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25` — **245 passed, 0 failed, 307 warnings in 207.29s (0:03:27)**. Log: `C:\Users\prati\AppData\Local\Temp\opencode\full_suite_hardening.log`.

## Second hardening pass

Statuses below describe the current pass only. Each item is committed separately; the final full-suite result is recorded in item 5. The earlier pass above remains unchanged.

| # | Item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Upload prefix inventory and authorization | Fixed (targeted tests pass) | See below. |
| 2 | Derived asset-URL signing key | Fixed (targeted tests pass) | See below. |
| 3 | 30-second refresh replay grace window | Fixed (targeted tests pass) | See below. |
| 4 | Empty-database Alembic baseline review | KNOWN OPEN DEFECT (still open; see fresh-install follow-up below) | See below. |
| 5 | Final full suite and branch report | Fixed (full suite passed) | See below. |

### Second-pass item 1 — upload prefix inventory and authorization

Added `backend/scripts/enumerate_upload_prefixes.py`, which combines an AST scan of `settings.UPLOAD_DIR` joins, `_save_upload` calls, `/uploads/` literals, and directory creation with a canonical inventory verified against source lines. It prints every backend-written prefix (including dynamic employee/run/FY/organisation segments), maps each to the rule in `app/core/upload_auth.py`, and exits non-zero on an unmapped producer. The full printed inventory is in `C:\Users\prati\AppData\Local\Temp\opencode\item1_upload_prefix_inventory.log`; it reports no unmapped prefixes. PMS attachments are explicitly reported as out of scope because they use the independent `PMS_UPLOAD_ROOT` setting.

`PREFIX_RULES` is now the single source of truth for enforcement and mapping. It covers the gaps from this pass: `probation_letters/` (HR/superuser only), `statutory_validations/`, `templates/statutory/`, both `quotations/` and `crm/quotations/`, and every `exports/*` subfolder (`payroll/<run>/`, `payroll/<run>/payments/`, `payroll/statutory_validations/`, `payroll/<run>/bank_advice/`, `statutory/`, and `statutory/<run>/`). Unmapped prefixes remain denied for every user, including admins and HR.

Payslips, Form 16, and tax proofs now resolve the owning employee from the persisted DB URL first (`PayrollRecord.payslip_pdf_url`, `Form16Record` part paths, and `EmployeeTaxProof.file_path` joined through its declaration), then fall back to the employee id in the path/filename. The owner may download their own file in addition to `payroll_view`/HR/superuser. Added tests for own payslip and Form 16 (200), another employee's payslip and Form 16 (403), filename fallback without a DB row, HR access to a probation letter (200), and a made-up prefix (403). Targeted run with `tests/test_signed_asset_urls.py`: **26 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item1_targeted_tests.log`).

### Second-pass item 2 — derived asset-URL signing key

`app/core/asset_urls.py` now derives its HMAC key with `HMAC-SHA256(SECRET_KEY, b"asset-url")`. The derived key is used for both signing and verification, giving domain separation from JWT signing and any other HMAC use of `SECRET_KEY`; no new environment variable is needed, so the existing production validation of `SECRET_KEY` still applies. Added `asset_url_signing_key()` and tests asserting the exact derived value, that a signature made with the raw `SECRET_KEY` is rejected, and that the derived signature verifies. All existing expiry, path-binding, and tamper tests still pass. Targeted run with `tests/test_upload_authorization.py` and `tests/test_secure_uploads.py`: **42 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item2_targeted_tests.log`).

### Second-pass item 3 — 30-second refresh replay grace window

`app/api/v1/auth.py` now defines `REFRESH_REPLAY_GRACE_SECONDS = 30` and `_within_refresh_replay_grace()`, which measures the age of a rotated session's `last_seen_at` (treating SQLite-naive values as UTC). A replay of a just-rotated token still returns 401, but within the 30-second window it no longer revokes the user's other active sessions — this tolerates a client whose cookie jar lagged one rotation. A replay after the window is still treated as theft and revokes every active session. Updated `test_rotated_refresh_replay_revokes_every_user_session` to age the rotated session past the window, and added `test_rotated_refresh_replay_within_grace_keeps_sessions`, which proves an immediate replay returns 401, leaves the active-session count unchanged, and keeps an independent session usable. Targeted run with `tests/test_auth.py`: **23 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item3_targeted_tests.log`).

### Second-pass item 4 — empty-database Alembic baseline review

Attempted `alembic upgrade head` against an empty database. Docker was unavailable locally (`failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`), so the MySQL empty-DB run could not be executed in this environment. A local empty SQLite database was used instead; the upgrade failed with `duplicate column name: interests` on `[SQL: ALTER TABLE employees ADD COLUMN interests TEXT]` (log: `C:\Users\prati\AppData\Local\Temp\opencode\alembic_empty_db.log`).

Root cause: the baseline revision `backend/alembic/versions/20260430_001_initial_hrms_schema.py` implements `upgrade()` with `Base.metadata.create_all(bind=bind)` against the live `app.db.base.Base` metadata rather than a frozen schema snapshot. On a fresh database this creates the full current schema, so the next revision, `20260430_002_employee_optional_profile.py`, fails when it re-adds `interests` (along with `research_work`, `family_information`, and `health_information`). The same pattern affects many later `op.add_column` migrations (attendance computation, employee directory fields, CRM activity/email depth, notification channels, MFA enforcement, SSO providers, and PMS objects), so the chain break is systemic rather than a single column.

This item is report-only: no migration, Alembic file, or CI job was edited, and the failing check was not suppressed or hidden. The empty-database failure remains open. A clean install needs a frozen initial baseline (or an idempotent chain) before it can be trusted; this should be addressed in a dedicated change with a real MySQL empty-DB verification.

### Second-pass item 5 — final full suite and branch report

Ran the full backend suite once on the final tree with `INSTALLED_APPS=hrms,crm,project_management ENVIRONMENT=test python -m pytest -q --tb=short -p no:cacheprovider --timeout=60 --durations=25`: **255 passed, 0 failed, 307 warnings in 212.76s (0:03:32)**. Log: `C:\Users\prati\AppData\Local\Temp\opencode\full_suite_hardening_pass2.log`. Both new replay-grace tests appear in the slowest-25 list and passed.

`git log --oneline origin/main..HEAD` was captured before this item's commit and listed 29 commits: the first four of this pass (one commit per item), plus the 25 earlier-pass commits recorded above. This item's AUDIT commit is added on top of that list. Nothing was merged or pushed.

```text
9311528 docs(security): report empty-database Alembic baseline defect
27da043 fix(security): add 30-second refresh replay grace window
1b0f7b4 fix(security): derive asset URL signing key
68308ad fix(security): complete upload prefix authorization coverage
8934bf7 docs(security): record final full-suite result
531930a docs: warn that deploy invalidates existing sessions
8e82d7e ci: add CI, Docker stack, lint config, and security policy
4256128 fix(auth): require Origin and CSRF header for cookie auth
09ff76a fix(auth): enforce Redis-backed rate limits with proxy-safe IP keys
f55ccc0 fix(config): restrict environments and harden cookie/logging defaults
344866a fix(startup): keep production schema under Alembic control
dbfdbb9 fix(assets): issue signed single-path URLs instead of query tokens
a5a9c6c fix(uploads): authorize stored URLs by prefix and deny unknown paths
c5a9a95 docs(security): record final full-suite result in audit
18eb4d1 test(routes): add generator sanity checks and refactor for import
0bc7134 perf(tests): skip middleware audit writes in test environment
1d28066 test(crm): enable all apps by default and verify tenant isolation
2baf827 docs(security): rewrite audit with honest verification statuses
bd2da92 fix(backend): support nested FastAPI routers in route checks
952a4df fix(backend): repair suite regressions from security hardening
3ee5fbc build(deps): upgrade Python and frontend dependencies
a606ffa docs(security): add route access-control matrix
d07e9cb fix(auth): harden token storage, JWT claims, and refresh rotation
0d91e9d fix(cors): harden allowed methods and headers
563cc80 feat(auth): rate-limit authentication endpoints
3b3cae4 fix(webhooks): verify HMAC signatures for inbound webhooks
e078a89 fix(secrets): require explicit production keys and add rotation
22fa128 fix(uploads): require authentication for uploaded file downloads
6004e37 fix(seed): make demo data opt-in and block production seeding
```

## Fresh-install schema initialization (follow-up)

| # | Change | Status | Evidence |
| --- | --- | --- | --- |
| 1 | `scripts/init_schema.py` for fresh installs | Verified (targeted tests pass) | See below. |
| 2 | Docker entrypoint chooses fresh-install vs. migration | Verified (config review) | See below. |
| 3 | CI fresh-install and Alembic round-trip check | Verified (config review; MySQL run not local) | See below. |
| 4 | Database documentation and open-defect record | Documented | See below. |

### Fresh installs vs. existing databases

`backend/scripts/init_schema.py` is the only supported path for a fresh, empty database. It loads the common models plus the models of every installed app, runs `Base.metadata.create_all()`, and stamps the single Alembic head programmatically through `MigrationContext`. It exits 1 with a clear message if the database already contains an `alembic_version` table or any application table, unless `--force` is passed. `backend/tests/test_init_schema.py` covers an empty SQLite DB (all app tables created and head stamped), refusal on a non-empty DB, refusal when only the version table exists, `--force`, `--check-empty`, and the real CLI exit code — **6 passed** (`C:\Users\prati\AppData\Local\Temp\opencode\item1_init_schema_tests.log`).

Existing databases must use `alembic upgrade head`. `backend/docker-entrypoint.sh` now uses `init_schema.py --check-empty` when `RUN_MIGRATIONS_ON_START=true`: an empty DB is initialized and stamped, otherwise the normal migration chain runs.

CI's Alembic step was replaced with `python scripts/init_schema.py`, `alembic upgrade head` (expected no-op), `alembic downgrade -1`, `alembic upgrade head`, then an `information_schema` SQL assertion that `user_sessions.session_id` and a unique index on it exist (the head revision adds both). No `continue-on-error` was added and no other job was changed. The MySQL portion has not been executed locally because the Docker daemon is unavailable; it is recorded as config-reviewed, not locally verified.

### KNOWN OPEN DEFECT — full Alembic chain on an empty database

Replaying the full migration chain on an empty database is broken. Revision `backend/alembic/versions/20260430_001_initial_hrms_schema.py` calls `Base.metadata.create_all(bind=bind)` against the live `app.db.base.Base` metadata instead of a frozen baseline. On a fresh DB this creates the entire current schema, so later revisions re-add those columns and fail with `duplicate column name: interests` (`C:\Users\prati\AppData\Local\Temp\opencode\alembic_empty_db.log`). The same pattern recurs in many later `op.add_column` migrations.

This defect is **not fixed**. No migration or CI file was edited to hide it, and it must not be reported as fixed. Proposed fix: replace revision 001's `create_all` with a frozen baseline snapshot of the original schema, then re-verify the full `alembic upgrade head` chain from an empty MySQL 8 database, including the downgrade/upgrade round trip and the `user_sessions.session_id` unique-index check. Until that lands, fresh installs use `scripts/init_schema.py` and existing databases use `alembic upgrade head`.
