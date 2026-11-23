# Secret configuration and rotation

## Required production settings

`ENVIRONMENT=production` refuses to start unless these values are explicitly set in the environment or `.env`:

- `SECRET_KEY` — access-token and MFA-token signing key.
- `REFRESH_SECRET_KEY` — refresh-token signing key; must differ from `SECRET_KEY`.
- `ENCRYPTION_KEY` — Fernet key source for values encrypted at rest (CRM/PM OAuth tokens, BGV webhook secrets); must differ from both JWT keys.

Each value must be at least 32 characters and must not be one of the placeholders from `backend/.env.example`. In development and test, missing values are generated per process for convenience; do not rely on those across restarts.

## Rotating `SECRET_KEY` / `REFRESH_SECRET_KEY`

1. Generate a new random value (for example `python -c "import secrets; print(secrets.token_urlsafe(48))"`).
2. Set `SECRET_KEY_PREVIOUS` (or `REFRESH_SECRET_KEY_PREVIOUS`) to the current value.
3. Deploy with the new active value. Existing tokens remain verifiable via the previous key until they expire.
4. After the maximum token lifetime has elapsed, remove the `*_PREVIOUS` variable.

## Rotating `ENCRYPTION_KEY`

Encrypted database values are versioned by trying the active key first and `ENCRYPTION_KEY_PREVIOUS` second.

1. Set `ENCRYPTION_KEY_PREVIOUS` to the current key.
2. Set `ENCRYPTION_KEY` to the new key and deploy. Reads continue to work with both keys.
3. Re-save every encrypted record so it is rewritten with the new key. `app.core.encryption.reencrypt_secret()` is available for a migration or maintenance script. The affected columns are:
   - `calendar_integrations.access_token_encrypted`, `refresh_token_encrypted`
   - `pms_dev_integrations.access_token_encrypted`, `webhook_secret_encrypted`
   - `background_verification_vendors.webhook_secret_ref`
4. Verify no rows decrypt with the previous key, then remove `ENCRYPTION_KEY_PREVIOUS`.

Never rotate `SECRET_KEY` and `ENCRYPTION_KEY` in the same deployment step unless both previous values are configured.
