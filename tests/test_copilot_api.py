from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_explain_normal_order_without_api_key_is_friendly(monkeypatch):
    monkeypatch.setenv("COPILOT_LLM_MODE", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/copilot/orders/trip_demo_001/explain")
    body = response.json()
    assert response.status_code == 200
    assert body["success"] is True
    assert body["llm"]["status"] in {"skipped_no_api_key", "local_mode"}


def test_explain_unknown_order_404():
    response = client.post("/copilot/orders/missing_order/explain")
    assert response.status_code == 404


def test_recommend_approve_and_audit():
    response = client.post("/copilot/orders/trip_demo_003/recommend")
    body = response.json()
    assert response.status_code == 200
    assert body["recommendation"] == "manual_driver_restriction_review"
    assert body["requires_human_approval"] is True
    assert body["executed"] is False

    approved = client.post(
        f"/copilot/actions/{body['action_id']}/approve",
        json={"operator_id": "demo_operator", "note": "test approval"},
    )
    assert approved.status_code == 200
    assert approved.json()["executed_by_ai"] is False
    assert approved.json()["audit_recorded"] is True

    audit = client.get("/copilot/audit").json()
    assert any(record.get("action_id") == body["action_id"] for record in audit["records"])


def test_recommend_reject_and_audit():
    response = client.post("/copilot/orders/trip_demo_002/recommend")
    action_id = response.json()["action_id"]

    rejected = client.post(
        f"/copilot/actions/{action_id}/reject",
        json={"operator_id": "demo_operator", "note": "test rejection"},
    )
    assert rejected.status_code == 200
    assert rejected.json()["decision"] == "rejected"
    assert rejected.json()["final_effect"] == "no_state_change"


def test_system_explain_contains_sanitized_certification():
    response = client.get("/copilot/system/explain")
    body = response.json()
    assert response.status_code == 200
    assert body["certification_summary"]["completed"] == 72000
    assert body["certification_summary"]["timeouts"] == 0

