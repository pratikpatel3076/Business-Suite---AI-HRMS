import pytest
from pydantic import ValidationError

from app.core.config import PLACEHOLDER_SECRETS, Settings, settings
from app.core.encryption import decrypt_secret, encrypt_secret, reencrypt_secret

VALID_SECRET = "a-unique-production-secret-with-32-chars"
VALID_REFRESH = "a-different-refresh-secret-with-32-chars"
VALID_ENCRYPTION = "a-different-encryption-key-with-32-chars"


def _production_settings(**overrides):
    values = {
        "ENVIRONMENT": "production",
        "SECRET_KEY": VALID_SECRET,
        "REFRESH_SECRET_KEY": VALID_REFRESH,
        "ENCRYPTION_KEY": VALID_ENCRYPTION,
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_production_requires_explicit_secrets():
    with pytest.raises(ValidationError, match="SECRET_KEY must be set"):
        Settings(_env_file=None, ENVIRONMENT="production")


def test_production_rejects_short_secret():
    with pytest.raises(ValidationError, match="at least 32 characters"):
        _production_settings(SECRET_KEY="short")


def test_production_rejects_placeholder_secret():
    placeholder = next(iter(PLACEHOLDER_SECRETS))
    with pytest.raises(ValidationError, match="placeholder"):
        _production_settings(SECRET_KEY=placeholder)


def test_production_rejects_identical_signing_keys():
    with pytest.raises(ValidationError, match="must be different"):
        _production_settings(REFRESH_SECRET_KEY=VALID_SECRET)


def test_production_rejects_encryption_key_reuse():
    with pytest.raises(ValidationError, match="distinct from the JWT signing keys"):
        _production_settings(ENCRYPTION_KEY=VALID_SECRET)


def test_encryption_key_is_independent_of_secret_key(monkeypatch):
    monkeypatch.setattr(settings, "SECRET_KEY", VALID_SECRET)
    monkeypatch.setattr(settings, "REFRESH_SECRET_KEY", VALID_REFRESH)
    monkeypatch.setattr(settings, "ENCRYPTION_KEY", VALID_ENCRYPTION)
    monkeypatch.setattr(settings, "ENCRYPTION_KEY_PREVIOUS", None)

    encrypted = encrypt_secret("sensitive-value")
    monkeypatch.setattr(settings, "SECRET_KEY", "rotated-signing-key-that-is-long-enough")

    assert decrypt_secret(encrypted) == "sensitive-value"


def test_encryption_key_rotation(monkeypatch):
    old_key = "old-encryption-key-with-at-least-32-chars"
    new_key = "new-encryption-key-with-at-least-32-chars"

    monkeypatch.setattr(settings, "ENCRYPTION_KEY", old_key)
    monkeypatch.setattr(settings, "ENCRYPTION_KEY_PREVIOUS", None)
    encrypted = encrypt_secret("rotate-me")

    monkeypatch.setattr(settings, "ENCRYPTION_KEY", new_key)
    monkeypatch.setattr(settings, "ENCRYPTION_KEY_PREVIOUS", old_key)
    assert decrypt_secret(encrypted) == "rotate-me"

    rewritten = reencrypt_secret(encrypted)
    monkeypatch.setattr(settings, "ENCRYPTION_KEY_PREVIOUS", None)
    assert decrypt_secret(rewritten) == "rotate-me"
    assert rewritten != encrypted
