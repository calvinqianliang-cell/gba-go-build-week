from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def main():
    health = client.get("/health")
    assert_equal(health.status_code, 200, "health status")
    assert_equal(health.json()["success"], True, "health success")

    explained = client.post("/copilot/orders/trip_demo_001/explain")
    assert_equal(explained.status_code, 200, "explain status")
    assert_equal(explained.json()["success"], True, "explain success")

    missing = client.post("/copilot/orders/missing_order/explain")
    assert_equal(missing.status_code, 404, "missing order status")

    recommended = client.post("/copilot/orders/trip_demo_003/recommend")
    assert_equal(recommended.status_code, 200, "recommend status")
    recommendation = recommended.json()
    assert_equal(recommendation["recommendation"], "manual_driver_restriction_review", "recommendation")
    assert_equal(recommendation["requires_human_approval"], True, "human approval required")
    assert_equal(recommendation["executed"], False, "ai execution blocked")

    action_id = recommendation["action_id"]
    approved = client.post(
        f"/copilot/actions/{action_id}/approve",
        json={"operator_id": "demo_operator", "note": "script approval"},
    )
    assert_equal(approved.status_code, 200, "approve status")
    assert_equal(approved.json()["executed_by_ai"], False, "approval does not mean AI execution")

    rejected_action = client.post("/copilot/orders/trip_demo_002/recommend").json()["action_id"]
    rejected = client.post(
        f"/copilot/actions/{rejected_action}/reject",
        json={"operator_id": "demo_operator", "note": "script rejection"},
    )
    assert_equal(rejected.status_code, 200, "reject status")
    assert_equal(rejected.json()["decision"], "rejected", "reject decision")

    system = client.get("/copilot/system/explain")
    assert_equal(system.status_code, 200, "system status")
    assert_equal(system.json()["certification_summary"]["completed"], 72000, "cert completed")
    assert_equal(system.json()["certification_summary"]["timeouts"], 0, "cert timeouts")

    audit = client.get("/copilot/audit")
    assert_equal(audit.status_code, 200, "audit status")
    if not audit.json()["records"]:
        raise AssertionError("audit records should not be empty")

    print("All critical demo tests passed")


if __name__ == "__main__":
    main()
