import json
import time
from typing import Callable, Optional
from urllib.parse import parse_qsl, urlencode
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.config import settings


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Logs API requests to the audit_logs table, including failures."""

    SKIP_PREFIXES = (f"{settings.API_V1_STR}/uploads",)
    SKIP_ENDPOINTS = {"/health"}

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if self._should_skip(request):
            return await call_next(request)

        start_time = time.time()
        try:
            response = await call_next(request)
            duration_ms = int((time.time() - start_time) * 1000)

            try:
                await self._log_request(request, response.status_code, duration_ms)
            except Exception:
                pass

            return response
        except Exception as exc:
            duration_ms = int((time.time() - start_time) * 1000)
            try:
                await self._log_request(request, 500, duration_ms, error=exc)
            except Exception:
                pass
            raise

    def _should_skip(self, request: Request) -> bool:
        path = request.url.path
        if path in self.SKIP_ENDPOINTS:
            return True
        return any(path.startswith(prefix) for prefix in self.SKIP_PREFIXES)

    async def _log_request(self, request: Request, status_code: int, duration_ms: int, error: Optional[Exception] = None):
        if settings.ENVIRONMENT == "test":
            # The test suite overrides get_db with an in-memory session, but
            # middleware cannot use that override. Opening SessionLocal here
            # would attempt a real MySQL connection (~4s timeout per request)
            # and the failure is swallowed, so tests paid the cost for no data.
            # Audit persistence is not under test; fixtures insert rows directly.
            return

        from app.db.session import SessionLocal
        from app.models.audit import AuditLog
        from app.core.security import verify_access_token

        user_id = None
        try:
            auth = request.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                payload = verify_access_token(auth[7:])
                if payload:
                    user_id = int(payload.get("sub", 0)) or None
        except Exception:
            pass

        db = SessionLocal()
        try:
            forwarded_for = request.headers.get("x-forwarded-for")
            ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else (
                request.client.host if request.client else None
            )
            log = AuditLog(
                user_id=user_id,
                method=request.method,
                endpoint=str(request.url.path),
                ip_address=ip_address,
                user_agent=request.headers.get("user-agent"),
                status_code=status_code,
                duration_ms=duration_ms,
                action="ERROR" if status_code >= 500 else request.method,
                description=self._description(request, error),
            )
            db.add(log)
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

    def _description(self, request: Request, error: Optional[Exception]) -> Optional[str]:
        parts = []
        if request.url.query:
            # Asset requests carry a bearer token in the query string because
            # browsers cannot set headers on <img>/<a> requests. Never persist it.
            redacted = [
                (key, "REDACTED" if key.lower() in {"token", "access_token"} else value)
                for key, value in parse_qsl(request.url.query, keep_blank_values=True)
            ]
            parts.append(f"query={urlencode(redacted)}")
        if error:
            parts.append(f"error={type(error).__name__}: {str(error)[:1000]}")
        return " | ".join(parts) if parts else None
