"""Create the schema for a fresh installation and mark Alembic at head.

Replaying the full migration chain on an empty database is currently broken:
revision 001 calls ``Base.metadata.create_all()`` against live metadata, so
later revisions that add the same columns fail with "duplicate column".
For a new installation this script creates the schema directly from the
installed apps' models and stamps the Alembic head, which makes a subsequent
``alembic upgrade head`` a no-op.

Existing databases must use ``alembic upgrade head`` instead. This script
refuses to touch a database that already contains an Alembic version table or
any application table, unless ``--force`` is passed.

Run from ``backend/`` (a path override is available for SQLite tests):

    python scripts/init_schema.py
    python scripts/init_schema.py --database-url sqlite:///./fresh.db
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect

from app.core.config import settings

VERSION_TABLE = "alembic_version"


def alembic_config(database_url: str | None = None) -> Config:
    """Build an Alembic config pointing at the same database we just created."""
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", database_url or settings.SQLALCHEMY_DATABASE_URI)
    return config


def _existing_tables(engine) -> set[str]:
    return set(inspect(engine).get_table_names())


def _application_base():
    # Importing app.db.base loads common models plus every installed app's
    # models (via module_registry.import_model_modules()).
    import app.db.base  # noqa: F401
    from app.db.base_class import Base

    return Base


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize a fresh database schema and stamp Alembic head.")
    parser.add_argument(
        "--database-url",
        default=None,
        help="Override DATABASE_URL (primarily for SQLite tests).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Proceed even when tables already exist. Not recommended for real deployments.",
    )
    parser.add_argument(
        "--check-empty",
        action="store_true",
        help="Print 'empty' or 'populated' without changing anything (used by docker-entrypoint.sh).",
    )
    args = parser.parse_args(argv)

    url = args.database_url or settings.SQLALCHEMY_DATABASE_URI
    engine = create_engine(url)
    try:
        tables = _existing_tables(engine)
    except Exception as exc:
        print(f"Cannot inspect database: {exc}", file=sys.stderr)
        return 2

    if args.check_empty:
        print("empty" if not tables else "populated")
        return 0

    Base = _application_base()
    blocking = sorted(tables & (set(Base.metadata.tables) | {VERSION_TABLE}))
    if blocking and not args.force:
        print("Refusing to initialize a non-empty database.", file=sys.stderr)
        print("Existing table(s): " + ", ".join(blocking), file=sys.stderr)
        print(
            "Existing databases must use 'alembic upgrade head'. "
            "Use --force only if you intentionally want to override this guard.",
            file=sys.stderr,
        )
        return 1

    Base.metadata.create_all(bind=engine)

    config = alembic_config(url)
    script = ScriptDirectory.from_config(config)
    heads = script.get_heads()
    if len(heads) != 1:
        raise RuntimeError(f"Expected exactly one Alembic head, found: {heads}")
    head = heads[0]
    # Use MigrationContext directly so the stamp goes to this engine, not to
    # the URL that alembic/env.py would read back from settings.
    with engine.begin() as connection:
        MigrationContext.configure(connection).stamp(script, head)
    engine.dispose()

    created = sorted(set(Base.metadata.tables) - tables)
    print(f"Created {len(created)} table(s) and stamped Alembic head {head}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
