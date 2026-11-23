"""Short-lived, single-path signed URLs for asset downloads.

The signature is an HMAC over the exact stored path and an expiry timestamp.
It is issued only after the normal per-prefix authorization check, so a signed
URL is a 60-second capability for one file and cannot be replayed for another.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from urllib.parse import quote

from app.core.config import settings

ASSET_URL_TTL_SECONDS = 60


def _signature(message: str) -> str:
    return hmac.new(settings.SECRET_KEY.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()


def create_signed_asset_url(relative_path: str) -> str:
    """Return an API path with a 60-second signature bound to ``relative_path``."""
    expires = str(int(time.time()) + ASSET_URL_TTL_SECONDS)
    sig = _signature(f"{relative_path}|{expires}")
    # The API base prefix is added by the client, so this stays relative to it.
    return f"/uploads/{quote(relative_path)}?expires={expires}&sig={sig}"


def verify_signed_asset_url(relative_path: str, expires: str | None, sig: str | None) -> bool:
    """Validate a signed URL for exactly ``relative_path``."""
    if not expires or not sig:
        return False
    try:
        expiry = int(expires)
    except (TypeError, ValueError):
        return False
    now = int(time.time())
    if expiry < now or expiry > now + ASSET_URL_TTL_SECONDS:
        return False
    expected = _signature(f"{relative_path}|{expires}")
    return hmac.compare_digest(expected, sig)
