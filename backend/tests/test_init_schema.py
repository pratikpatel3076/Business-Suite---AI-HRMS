"""Fresh-install schema initialization: create_all plus an Alembic head stamp."""

import os
import subprocess
import sys
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text

from scripts.init_schema import main

BACKEND_ROOT = Path(__file__).resolve().parents[1]


def _url(tmp_path, name="fresh.sqlite3"):
    return f"sqlite:///{tmp_path / name}"


def _head():
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    heads = ScriptDirectory.from_config(config).get_heads()
    assert len(heads) == 1
    return heads[0]


def _tables(url):
    engine = create_engine(url)
    try:
        return set(inspect(engine).get_table_names())
    finally:
        engine.dispose()


def _stamped_version(url):
    engine = create_engine(url)
    try:
        with engine.connect() as connection:
            return connection.execute(text("SELECT version_num FROM alembic_version")).scalar()
    finally:
        engine.dispose()


def _create_legacy_users_table(url):
    engine = create_engine(url)
    try:
        with engine.begin() as connection:
            connection.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY)"))
    finally:
        engine.dispose()


def test_init_schema_creates_schema_and_stamps_head(tmp_path):
    url = _url(tmp_path)

    assert main(["--database-url", url]) == 0

    tables = _tables(url)
    # Common models plus every installed app's models are loaded.
    assert {"users", "employees", "crm_leads", "pms_projects", "alembic_version"} <= tables
    assert _stamped_version(url) == _head()


def test_init_schema_refuses_non_empty_database(tmp_path, capsys):
    url = _url(tmp_path)
    _create_legacy_users_table(url)

    assert main(["--database-url", url]) == 1

    captured = capsys.readouterr()
    assert "Refusing to initialize a non-empty database" in captured.err
    assert "users" in captured.err
    assert "alembic_version" not in _tables(url)


def test_init_schema_refuses_when_only_version_table_exists(tmp_path, capsys):
    url = _url(tmp_path)
    engine = create_engine(url)
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL PRIMARY KEY)")
        )
    engine.dispose()

    assert main(["--database-url", url]) == 1

    assert "alembic_version" in capsys.readouterr().err


def test_init_schema_force_stamps_non_empty_database(tmp_path):
    url = _url(tmp_path)
    _create_legacy_users_table(url)

    assert main(["--database-url", url, "--force"]) == 0

    assert {"users", "employees", "alembic_version"} <= _tables(url)
    assert _stamped_version(url) == _head()


def test_init_schema_check_empty_reports_state(tmp_path, capsys):
    url = _url(tmp_path)

    assert main(["--database-url", url, "--check-empty"]) == 0
    assert capsys.readouterr().out.strip() == "empty"

    _create_legacy_users_table(url)

    assert main(["--database-url", url, "--check-empty"]) == 0
    assert capsys.readouterr().out.strip() == "populated"


def test_init_schema_cli_exits_one_on_refusal(tmp_path):
    url = _url(tmp_path)
    _create_legacy_users_table(url)

    env = dict(os.environ)
    # Settings rejects ENVIRONMENT=test outside pytest.
    env["ENVIRONMENT"] = "development"
    result = subprocess.run(
        [sys.executable, "scripts/init_schema.py", "--database-url", url],
        cwd=BACKEND_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Refusing to initialize a non-empty database" in result.stderr
