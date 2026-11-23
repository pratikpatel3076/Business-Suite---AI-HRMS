#!/bin/sh
set -eu

# Local Docker Compose uses this to apply migrations before the API starts.
# Deployments should run `alembic upgrade head` as an explicit release step.
if [ "${RUN_MIGRATIONS_ON_START:-false}" = "true" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
fi

exec "$@"
