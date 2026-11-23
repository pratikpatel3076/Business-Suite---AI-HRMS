import json
import time

import pytest
from fastapi import status

from app.core.config import settings
from app.core.webhooks import SIGNATURE_HEADER, TIMESTAMP_HEADER, sign_webhook_body
from app.main import app

BGV_SECRET = "bgv-webhook-secret-0123456789"


def _headers(secret: str, raw_body: bytes, *, timestamp: str | None = None, signature: str | None = None) -> dict[str, str]:
    sent_at = timestamp or str(int(time.time()))
    return {
        "Content-Type": "application/json",
        TIMESTAMP_HEADER: sent_at,
        SIGNATURE_HEADER: signature or sign_webhook_body(secret, sent_at, raw_body),
    }


@pytest.fixture
def bgv_webhook_setup(client, superuser_headers):
    vendor = client.post(
        "/api/v1/background-verification/vendors",
        json={"name": "Signature Vendor", "webhook_secret_ref": BGV_SECRET},
        headers=superuser_headers,
    ).json()
    request = client.post(
        "/api/v1/background-verification/requests",
        json={
            "vendor_id": vendor["id"],
            "candidate_id": 1,
            "package_name": "Signature Package",
            "vendor_reference": "SIG-REF-1",
            "checks": [{"check_type": "Identity"}],
        },
        headers=superuser_headers,
    ).json()
    return vendor["id"], request["id"]


def _bgv_body() -> bytes:
    return json.dumps(
        {"vendor_reference": "SIG-REF-1", "event_type": "verification.updated", "status": "Completed"},
        separators=(",", ":"),
    ).encode("utf-8")


def test_bgv_vendor_secret_is_not_returned(db, bgv_webhook_setup):
    from app.models.background_verification import BackgroundVerificationVendor

    vendor_id, _ = bgv_webhook_setup
    vendor = db.query(BackgroundVerificationVendor).filter(BackgroundVerificationVendor.id == vendor_id).first()
    assert vendor is not None
    assert vendor.webhook_secret_ref != BGV_SECRET


def test_bgv_webhook_accepts_valid_signature(client, bgv_webhook_setup):
    vendor_id, _ = bgv_webhook_setup
    raw = _bgv_body()
    response = client.post(
        f"/api/v1/background-verification/webhooks/{vendor_id}",
        content=raw,
        headers=_headers(BGV_SECRET, raw),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "Completed"


def test_bgv_webhook_rejects_invalid_signature(client, bgv_webhook_setup):
    vendor_id, _ = bgv_webhook_setup
    raw = _bgv_body()
    response = client.post(
        f"/api/v1/background-verification/webhooks/{vendor_id}",
        content=raw,
        headers=_headers("wrong-secret", raw),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_bgv_webhook_rejects_missing_signature(client, bgv_webhook_setup):
    vendor_id, _ = bgv_webhook_setup
    response = client.post(
        f"/api/v1/background-verification/webhooks/{vendor_id}",
        content=_bgv_body(),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_bgv_webhook_rejects_replayed_signature(client, bgv_webhook_setup):
    vendor_id, _ = bgv_webhook_setup
    raw = _bgv_body()
    stale_timestamp = str(int(time.time()) - 3600)
    response = client.post(
        f"/api/v1/background-verification/webhooks/{vendor_id}",
        content=raw,
        headers=_headers(BGV_SECRET, raw, timestamp=stale_timestamp),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_crm_calendar_webhook_is_disabled_by_default(monkeypatch, client):
    monkeypatch.setattr(settings, "CRM_CALENDAR_WEBHOOK_ENABLED", False)
    if not any(route.path == "/api/v1/crm/calendar/webhook" for route in app.routes):
        pytest.skip("CRM router is not installed in this test environment")

    response = client.post("/api/v1/crm/calendar/webhook", content=b"{}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("case", ["valid", "invalid", "missing", "replayed"])
def test_crm_calendar_webhook_signature_verification(monkeypatch, client, case):
    monkeypatch.setattr(settings, "CRM_CALENDAR_WEBHOOK_ENABLED", True)
    monkeypatch.setattr(settings, "CRM_CALENDAR_WEBHOOK_SECRET", "calendar-webhook-secret-0123456789")
    if not any(route.path == "/api/v1/crm/calendar/webhook" for route in app.routes):
        pytest.skip("CRM router is not installed in this test environment")

    raw = json.dumps({"event": "event.updated"}, separators=(",", ":")).encode("utf-8")
    secret = "calendar-webhook-secret-0123456789"
    if case == "missing":
        headers = {"Content-Type": "application/json"}
    elif case == "replayed":
        headers = _headers(secret, raw, timestamp=str(int(time.time()) - 3600))
    elif case == "invalid":
        headers = _headers("wrong-secret", raw)
    else:
        headers = _headers(secret, raw)

    response = client.post("/api/v1/crm/calendar/webhook", content=raw, headers=headers)
    expected = status.HTTP_200_OK if case == "valid" else status.HTTP_401_UNAUTHORIZED
    assert response.status_code == expected
