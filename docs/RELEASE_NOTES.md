# Release notes

## Security hardening

- **Sessions:** All existing sessions are invalidated on deploy because refresh tokens now require a `jti` claim and a matching `UserSession` row. Users must sign in again after the upgrade.
