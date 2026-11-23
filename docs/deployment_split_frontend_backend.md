# Split Deployment: Frontend, Backend, and DigitalOcean MySQL

This project is now set up for separate deployment:

- Frontend: static React/Vite build on any web server.
- Backend: FastAPI API server on a backend server.
- Database: DigitalOcean Managed MySQL.

## Backend

Configure `backend/.env` on the backend server.

Use either a full database URL:

```env
DATABASE_URL=mysql+pymysql://doadmin:password@db-mysql-region-do-user-000000-0.b.db.ondigitalocean.com:25060/ai_hrms?charset=utf8mb4
```

Or individual values:

```env
MYSQL_USER=doadmin
MYSQL_PASSWORD=your_password
MYSQL_SERVER=db-mysql-region-do-user-000000-0.b.db.ondigitalocean.com
MYSQL_PORT=25060
MYSQL_DB=ai_hrms
MYSQL_SSL_CA=/path/to/ca-certificate.crt
```

Set CORS to the real frontend URL:

```env
BACKEND_PUBLIC_URL=https://api.yourdomain.com
FRONTEND_PUBLIC_URL=https://hrms.yourdomain.com
BACKEND_CORS_ORIGINS=["https://hrms.yourdomain.com"]
```

Run the backend API behind HTTPS and route all API traffic under:

```text
https://api.yourdomain.com/api/v1
```

Uploaded files are served only through authenticated API routes:

```text
https://api.yourdomain.com/api/v1/uploads
```

## Auth rate limiting and proxy headers

Login and `POST /api/v1/auth/mfa/verify` are limited to **5 requests per minute per source IP and per account** (email for login, MFA token subject for verification). `POST /api/v1/auth/refresh` is limited to **30 requests per minute per source IP**. Counters are stored in Redis at `REDIS_URL`; Redis is required in production and the in-memory fallback is enabled only for local development. If Redis is unavailable in production, requests fail closed rather than silently dropping the limit.

Because the per-IP limit depends on the real client address, Uvicorn must trust the reverse proxy that sets `X-Forwarded-For`:

```bash
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --proxy-headers \
  --forwarded-allow-ips "10.0.0.0/8,172.16.0.0/12"
```

Set `--forwarded-allow-ips` to the exact CIDR(s) of your load balancer or reverse proxy. Do **not** use `*` on a publicly exposed API: a client could spoof `X-Forwarded-For` and bypass both the IP limit and the per-account protections. If the API is exposed directly with no proxy, omit `--proxy-headers` and rely on `request.client.host`.

The backend Docker image starts Uvicorn with these flags and reads the trusted CIDR list from `FORWARDED_ALLOW_IPS` (default `127.0.0.1`):

```bash
docker run \
  -e FORWARDED_ALLOW_IPS="10.0.0.0/8,172.16.0.0/12" \
  -e REDIS_URL="redis://redis:6379/0" \
  -p 8000:8000 \
  ai-hrms-backend
```

## Session cookies and CSRF

The refresh token is set by the backend as an `HttpOnly`, `Secure`, `SameSite=Strict` cookie scoped to `/api/v1/auth`. It is **cookie-only**: the old `refresh_token` request-body fallback has been removed.

`POST /api/v1/auth/refresh` and `POST /api/v1/auth/logout` additionally require both of these on every call:

- an `Origin` header (or `Referer` as a fallback) whose origin exactly matches an entry in `BACKEND_CORS_ORIGINS`; and
- an `X-CSRF-Token: hrms-app` custom header.

The frontend sends that header on every API request. Because a custom header forces a CORS preflight cross-site, an attacker page cannot satisfy the check unless the origin is explicitly allowed; a missing, unlisted, or wildcard origin returns `403`. `X-CSRF-Token` must stay in the backend CORS `allow_headers` list.

**Recommended deployment:** proxy `/api/*` through the frontend origin so the browser sees one site (see the same-origin configuration below). `SameSite=Strict` then works with silent refresh.

**Cross-site deployment:** if you deliberately need the cookie on a different site and change it to `SameSite=None; Secure`, do so **only with the Origin/Referer allowlist and CSRF header above still enabled**. Never combine `SameSite=None` with `BACKEND_CORS_ORIGINS=["*"]`, and keep `Secure`, `HttpOnly`, explicit origins, and `allow_credentials=True`. The cookie becomes cross-site, so the custom header and origin check are the controls that prevent CSRF, not the `SameSite` attribute.

## Background Workers

Start the task worker:

```bash
celery -A app.worker worker -l info
```

Start the beat scheduler, which is required for scheduled leave accruals:

```bash
celery -A app.worker beat -l info
```

Keep Celery Beat running in production for `accrual_frequency` values such as monthly, quarterly, and annual to credit leave balances on schedule.

## Frontend

Build once:

```bash
npm run build
```

Deploy `frontend/dist` to the frontend server. Then edit this deployed file:

```text
app-config.js
```

For split frontend/backend servers:

```js
window.__AI_HRMS_CONFIG__ = {
  apiBaseUrl: "https://api.yourdomain.com/api/v1",
};
```

For same-origin deployments with a reverse proxy:

```js
window.__AI_HRMS_CONFIG__ = {
  apiBaseUrl: "",
};
```

In same-origin mode, proxy these paths from the frontend domain to the backend:

```text
/api/*     -> backend server
```

## Local Development

Frontend dev proxy defaults to `http://localhost:8001`. Override it in `frontend/.env`:

```env
VITE_DEV_API_PROXY_TARGET=http://localhost:8001
```
