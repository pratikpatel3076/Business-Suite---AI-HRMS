"""Application-wide encryption for secrets stored in the database.

Keys are derived from the dedicated ``ENCRYPTION_KEY`` setting, never from the
JWT signing keys. Rotating keys is a two-step process:

1. Deploy with ``ENCRYPTION_KEY`` set to the new value and
   ``ENCRYPTION_KEY_PREVIOUS`` set to the old value. Decryption tries both.
2. Re-save each encrypted record (or run ``reencrypt_secret`` on its values)
   so it is written with the new key, then remove ``ENCRYPTION_KEY_PREVIOUS``.
"""

from __future__ import annotations

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings


def get_fernet(key: str | None = None) -> Fernet:
    """Return a Fernet instance for the active or explicitly supplied key."""
    active_key = key or settings.ENCRYPTION_KEY
    if not active_key:
        raise RuntimeError("ENCRYPTION_KEY is not configured")
    digest = hashlib.sha256(active_key.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_secret(value: str | None) -> str | None:
    if not value:
        return None
    return get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_secret(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return get_fernet().decrypt(value.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        previous = settings.ENCRYPTION_KEY_PREVIOUS
        if not previous:
            raise
        return get_fernet(previous).decrypt(value.encode("utf-8")).decode("utf-8")


def reencrypt_secret(value: str | None) -> str | None:
    """Decrypt with the previous key if needed and re-encrypt with the active key."""
    decrypted = decrypt_secret(value)
    return encrypt_secret(decrypted)
