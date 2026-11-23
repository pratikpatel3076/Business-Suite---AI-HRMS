# Security policy

## Supported versions

Security fixes are applied to the current `main` branch and to active release branches. This repository does not yet publish semantic-version tags; use the commit SHA when reporting a deployment-specific issue.

## Reporting a vulnerability

Please **do not open a public issue** for an unpatched vulnerability. Email the maintainers at `security@aihrms.com` with:

- affected commit/tag and deployment environment;
- reproduction steps or a proof of concept;
- impact and any known mitigations.

You should receive an acknowledgement within 3 business days. We will confirm the finding, prepare a fix, and coordinate disclosure with you before publishing details. Please do not include real credentials, tokens, or personal data in reports.

## Deployment requirements

These controls are mandatory for any non-local deployment:

1. **Secrets.** Set distinct, >=32-character `SECRET_KEY`, `REFRESH_SECRET_KEY`, and `ENCRYPTION_KEY` values from a secret manager. Never use the placeholders in `backend/.env.example`. `ENCRYPTION_KEY_PREVIOUS` supports key rotation. Startup rejects missing, short, placeholder, or duplicate secrets in `ENVIRONMENT=production`.
2. **Environment.** `ENVIRONMENT` defaults to `production` and accepts only `development`, `test`, and `production`. `ENVIRONMENT=test` is rejected outside pytest. Demo fixtures are opt-in via `SEED_DEMO_DATA` and never run in production.
3. **HTTPS and cookies.** Serve the API over HTTPS. The refresh cookie is `HttpOnly`, `Secure` (except local development), and `SameSite=Strict`. Access tokens live in memory only and expire after 15 minutes.
4. **Same-origin API.** Prefer proxying `/api/*` through the frontend origin (the bundled `nginx.conf` does this). If a cross-site cookie is unavoidable, use `SameSite=None; Secure` only with explicit CORS origins and CSRF defenses below; never use a wildcard origin.
5. **CSRF.** `/api/v1/auth/refresh` and `/api/v1/auth/logout` require an allowed `Origin`/`Referer` and the `X-CSRF-Token: hrms-app` header. The refresh token is cookie-only; request-body tokens are rejected. Replaying a rotated refresh token revokes all active sessions for that user.
6. **Redis and rate limits.** Provide `REDIS_URL` for auth rate-limit counters. Login and MFA verification are limited to 5/minute per IP and per account; refresh is 30/minute per IP. The in-memory fallback is development-only and production fails closed if Redis is unavailable.
7. **Proxy headers.** Run Uvicorn with `--proxy-headers` and set `--forwarded-allow-ips` to the exact proxy/load-balancer CIDRs. Do not use `*` on a publicly exposed API. The backend image reads `FORWARDED_ALLOW_IPS` (default `127.0.0.1`).
8. **Schema.** Production schema changes are applied only by `alembic upgrade head`. Application startup does not call `create_all` or `ensure_*_schema` outside development/test. CI verifies `upgrade head`, `downgrade -1`, and `upgrade head` against MySQL 8.
9. **Uploads.** Files are served only through authenticated `/api/v1/uploads/*` routes with ownership/permission checks and absolute-path, traversal, and symlink validation. Native browser downloads use 60-second HMAC-signed single-path URLs; no access token is placed in a query string.
10. **Audit logging.** Keep `AuditLogMiddleware` enabled in production; it records security-relevant requests and redacts token parameters.

## Operational notes

- **Sessions are invalidated on deploy:** refresh tokens now require a `jti` claim and a matching `UserSession` row. Tokens issued before this change cannot be refreshed, so users must sign in again.
- Rotate keys by setting `*_PREVIOUS` before replacing the primary value. Retire the previous value only after all issued tokens have expired.
- CI runs pytest, Ruff, an Alembic MySQL round trip, `pip-audit`, `npm ci`, `npm run build`, and `npm audit` on every push and pull request.

## Accepted residual risks

- `ecdsa 0.19.2` (`PYSEC-2026-1325`) has no fixed release. The vulnerable `sign_digest()` path is not used by this application.
- `python-jose 3.5.0` (`PYSEC-2026-4298`) has no fixed release. Tokens use only HS256 with server-controlled secrets; the application does not accept asymmetric keys as HMAC secrets. Both advisories are ignored by ID in CI so new findings still fail the build.
- CRM calendar webhook signature compatibility with the vendor's exact algorithm is not yet verified.
- The 96 flagged rows in `docs/security/route-matrix.md` were reviewed before the FastAPI upgrade and have not been revalidated against the current 870-route matrix.
