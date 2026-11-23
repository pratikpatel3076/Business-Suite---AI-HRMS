#!/bin/sh
set -eu

# Local Docker Compose uses this to prepare the database before the API starts.
# A fresh database is created from the installed models and stamped at Alembic
# head; an existing database follows the normal migration chain. Production
# deployments should still run `alembic upgrade head` as an explicit release
# step rather than relying on container startup.
if [ "${RUN_MIGRATIONS_ON_START:-false}" = "true" ]; then
    db_state="$(python scripts/init_schema.py --check-empty)"
    if [ "$db_state" = "empty" ]; then
        echo "Empty database: initializing schema and stamping Alembic head..."
        python scripts/init_schema.py
    else
        echo "Existing database: running Alembic migrations..."
        alembic upgrade head
    fi
fi

exec "$@"
