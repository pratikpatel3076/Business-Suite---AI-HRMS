# Gemeinsam

Gemeinsam is a modular HRMS/ERP platform with separate HRMS, CRM, and Project Management apps sharing one FastAPI backend and React frontend.

Modular HRMS/ERP platform (HRMS, CRM, Project Management). Portfolio project, security-hardened; see docs/security/AUDIT.md for what was verified and what is still open.

## Implemented vs experimental

Statuses are based on registered routers, existing tests, and explicit gaps in [docs/todo.md](docs/todo.md). "Working" means the module has routes and test coverage; it does not mean every external integration is live.

| Module | Status | Basis |
| --- | --- | --- |
| HRMS core (org structure, employees, attendance, leave, documents, helpdesk) | Working | `backend/app/api/v1/` routers; `test_employees.py`, `test_attendance.py`, `test_leave.py`, `test_document_governance.py` |
| Recruitment and onboarding | Working | `recruitment.py`, `onboarding.py` routers; `test_top_gap_closure.py`, `test_new_hrms_modules.py` |
| Payroll, tax, and statutory calculations | Partial | 142-route payroll API; `test_payroll_*` suites; portal conformance, real Form 16 DSC, and e-filing remain open in `docs/todo.md` |
| CRM records, pipeline, activities, approvals | Working | `backend/app/apps/crm/api/router.py`; `test_crm_rest_api.py` covers tenant-scoped CRUD |
| CRM mail, SMS, WhatsApp, and calendar providers | Experimental | Mock/placeholder adapters in `app/apps/crm/api/router.py`; Google/Outlook adapters have TODO configuration points |
| Project Management (boards, tasks, sprints, reports) | Working | `backend/app/apps/project_management/api/router.py`; `test_pms_project_access.py` |
| AI agents | Experimental | Conversation, approval, and audit routes exist, but `app/ai_agents/api.py` returns `AI_ENGINE_PLACEHOLDER` ("AI engine is not connected yet") |
| Background verification | Partial | Vendor/request/check CRUD and signed webhook tests; vendor API submission is recorded, not integrated with a real provider |
| Workflow engine and notifications | Partial | `workflow_engine.py` and `notifications.py` routers; `test_workflow_engine_depth.py`, `test_notifications.py`; `docs/todo.md` still lists retry workers |
| SSO and MFA | Partial | OIDC initiate/callback in `sso.py`; `sso.py` returns "SAML not yet implemented"; MFA verification routes exist but rollout policy remains open |
| WhatsApp ESS | Partial | Templates, opt-in, inbound intents, and outbound queue in `whatsapp_ess.py`; outbound messages are stored as `Queued`, with no Meta Cloud API dispatch |
| Biometric and geo attendance | Partial | Device/import and proof foundations in `attendance.py`; vendor SDK sync and mobile capture are open in `docs/todo.md` |
| Custom fields, forms, reports, and analytics | Partial | `custom_fields.py` and `reports.py` routers; `test_custom_forms_dei.py`; `docs/todo.md` describes analytics as basic |

## Tech stack

- Backend: Python 3.12, FastAPI 0.165.0, SQLAlchemy 2.0.30, Alembic 1.13.1, Pydantic 2.14.4, Celery 5.4.0, Redis 5.0.6.
- Database: MySQL 8 in the Compose stack; SQLite in-memory for tests. The database name is `ai_hrms` in `docker-compose.yml`, `backend/.env.example`, and CI.
- Frontend: React 18.3.1, TypeScript 5.2.2, Vite 8.3.8, React Router 7.18.6, TanStack Query 5.45.0, Zustand 4.5.2, Tailwind CSS 3.4.4.
- Tooling: pytest 9.2.0, Ruff 0.17.6, pip-audit 2.10.1, npm audit in CI.

## Quick start with Docker

Set `SECRET_KEY`, `REFRESH_SECRET_KEY`, `ENCRYPTION_KEY`, `REDIS_URL`, `ENVIRONMENT`, and `SEED_DEMO_DATA` in your shell or `backend/.env` (see `backend/.env.example`). Generate three distinct secrets of at least 32 characters. Use `ENVIRONMENT=development` and `SEED_DEMO_DATA=false` locally; Compose supplies the container Redis URL.

```bash
docker-compose up
```

Create the first administrator (the script prompts for missing values and enforces the password policy):

```bash
docker-compose exec -e ADMIN_EMAIL=you@example.com -e ADMIN_PASSWORD='<your-password>' api python scripts/create_admin.py
```

No default passwords are provided. Replace the placeholders with your own values.

## Local development

Backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
set ENVIRONMENT=development
set DATABASE_URL=mysql+pymysql://<user>:<password>@localhost:3306/ai_hrms
uvicorn app.main:app --reload --port 8000
```

On macOS/Linux use `source venv/bin/activate`, `export ENVIRONMENT=development`, and `export DATABASE_URL=...`.

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

Tests and schema:

```bash
cd backend
pytest
python scripts/init_schema.py
alembic upgrade head
```

Use `python scripts/init_schema.py` only for an empty database; it creates the current schema and stamps the Alembic head. Use `alembic upgrade head` for existing databases. Replaying the full migration chain on an empty database is a known open defect; see [docs/security/AUDIT.md](docs/security/AUDIT.md).

## Security summary

- Refresh tokens are HttpOnly, Secure outside local development, and SameSite=Strict cookies; access tokens stay in memory. Refresh and logout require an allowed Origin/Referer and `X-CSRF-Token`.
- Uploads are authorized by path prefix and record ownership; downloads use 60-second HMAC-signed single-path URLs instead of query-string tokens.
- Inbound webhooks use HMAC-SHA256 verification over the raw body with a replay window; background-verification secrets are encrypted at rest.
- Login and MFA verification are limited to 5/minute per IP and per account; refresh is 30/minute per IP, with Redis-backed counters.
- Production validates distinct, non-placeholder secrets and explicit CORS origins; `ENVIRONMENT` is restricted to development, test, and production.
- Production schema changes are Alembic-only; startup schema creation is gated to development and test.
- CI runs pytest, Ruff, an Alembic round trip on MySQL 8, pip-audit, npm ci, npm run build, and npm audit. See [.github/workflows/ci.yml](.github/workflows/ci.yml).
- Open verification gaps and accepted residual risks are recorded in [SECURITY.md](SECURITY.md) and [docs/security/AUDIT.md](docs/security/AUDIT.md).

## Project layout

```text
.github/workflows/   CI jobs
backend/             FastAPI app, models, Alembic revisions, scripts, tests
docs/                audit, architecture notes, backlog
frontend/            React/Vite app
```

## Clone

```bash
git clone https://github.com/pratikpatel3076/gemeinsam.git
cd gemeinsam
```

## Naming

Gemeinsam was previously known as AI HRMS, Business Suite, KaryaFlow, and Vyapara. Older links, bookmarks, and search results may still reference those former names.
