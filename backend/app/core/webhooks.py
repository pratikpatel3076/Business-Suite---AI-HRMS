"""Shared HMAC verification for inbound webhooks."""

from __future__ import annotations

import hashlib
import hmac
import time

from fastapi import HTTPException, status

SIGNATURE_HEADER = "X-Webhook-Signature"
TIMESTAMP_HEADER = "X-Webhook-Timestamp"
DEFAULT_TOLERANCE_SECONDS = 300

_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid webhook signature",
)


def sign_webhook_body(secret: str, timestamp: str, raw_body: bytes) -> str:
    """Build the signature a vendor should send in X-Webhook-Signature."""
    message = timestamp.encode("utf-8") + b"." + raw_body
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_webhook_signature(
    raw_body: bytes,
    secret: str | None,
    signature: str | None,
    timestamp: str | None,
    *,
    tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
    now: float | None = None,
) -> None:
    """Verify a timestamped HMAC-SHA256 signature in constant time.

    The signed message is ``<timestamp>.<raw request body>``. Signing the raw
    bytes (rather than re-serialised JSON) avoids canonicalisation mismatches.
    """
    if not secret or not signature or not timestamp:
        raise _UNAUTHORIZED

    try:
        sent_at = int(timestamp)
    except (TypeError, ValueError):
        raise _UNAUTHORIZED from None

    current = time.time() if now is None else now
    if abs(current - sent_at) > tolerance_seconds:
        raise _UNAUTHORIZED

    provided = signature.split("=", 1)[1] if signature.lower().startswith("sha256=") else signature
    expected = sign_webhook_body(secret, timestamp, raw_body)
    if not hmac.compare_digest(expected, provided):
        raise _UNAUTHORIZED
