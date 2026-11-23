"""Production must not create or patch schema outside Alembic."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI

from app.core.config import local_schema_management_enabled, settings
from app.main import lifespan


@pytest.mark.parametrize(
    "environment,expected",
    [("development", True), ("test", True), ("production", False), ("staging", False)],
)
def test_local_schema_management_flag(environment, expected, monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", environment)
    assert local_schema_management_enabled() is expected


@pytest.mark.parametrize(
    "environment,should_create",
    # "test" short-circuits startup entirely before reaching the schema block.
    [("development", True), ("test", False), ("production", False)],
)
async def test_lifespan_only_creates_schema_outside_production(
    environment, should_create, monkeypatch, tmp_path
):
    monkeypatch.setattr(settings, "ENVIRONMENT", environment)
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setattr("app.main.is_app_enabled", lambda name: True)

    calls = []
    fake_base = MagicMock()
    fake_base.metadata.create_all.side_effect = lambda bind: calls.append("create_all")
    fake_crm = MagicMock(side_effect=lambda db: calls.append("ensure_crm_schema"))
    fake_pms = MagicMock(side_effect=lambda db: calls.append("ensure_pms_schema"))
    fake_init = MagicMock(side_effect=lambda db: calls.append("init_db"))
    fake_session = MagicMock()

    with (
        patch("app.db.base.Base", fake_base),
        patch("app.apps.crm.schema.ensure_crm_schema", fake_crm),
        patch("app.apps.project_management.schema.ensure_pms_schema", fake_pms),
        patch("app.db.init_db.init_db", fake_init),
        patch("app.db.session.SessionLocal", return_value=fake_session),
        patch("app.ai_agents.services.registry.AiAgentRegistryService"),
        patch("app.ai_agents.tools.ai_tool_registry_service.AiToolRegistryService"),
    ):
        async with lifespan(FastAPI()):
            pass

    assert ("create_all" in calls) is should_create
    assert ("ensure_crm_schema" in calls) is should_create
    assert ("ensure_pms_schema" in calls) is should_create
    assert ("init_db" in calls) is (environment != "test")
