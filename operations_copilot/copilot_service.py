from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from operations_copilot.data_store import DataStore
from operations_copilot.llm_client import LLMClient


HIGH_RISK_ACTIONS = {
    "redispatch",
    "manual_driver_restriction_review",
    "manual_route_verification",
    "cancel_order",
    "keep_frozen",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class CopilotService:
    def __init__(self, store: Optional[DataStore] = None, llm: Optional[LLMClient] = None):
        self.store = store or DataStore()
        self.llm = llm or LLMClient()

    def _evidence_package(self, order_id: str) -> dict[str, Any]:
        trip = self.store.get_trip(order_id)
        if trip is None:
            raise KeyError(order_id)
        return {
            "order": trip,
            "driver": self.store.get_driver(trip.get("driver_id")),
            "passenger": self.store.get_passenger(trip.get("passenger_id")),
            "events": self.store.events_for_order(order_id),
        }

    def explain_order(self, order_id: str) -> dict[str, Any]:
        package = self._evidence_package(order_id)
        order = package["order"]
        dispatch_events = package["events"]["dispatch"]
        risk_events = package["events"]["risk"]
        driver = package["driver"]

        if order["status"] == "assigned":
            summary = "The reservation is assigned to an eligible demo driver."
            attention = ["Monitor pickup timing and keep the audit trail intact."]
        elif order.get("blocked_reason") == "no_driver_available":
            summary = "The order did not dispatch because no eligible online driver remained after filtering."
            attention = ["Check nearby zones before redispatching.", "Do not assign offline or restricted drivers."]
        elif order.get("blocked_reason") == "driver_reservation_limited":
            summary = "The best candidate is available, but reservation dispatch is limited for this driver."
            attention = ["Human review is required before changing the restriction."]
        elif order.get("blocked_reason") == "map_route_unverified":
            summary = "The route could not be trusted enough to quote or dispatch automatically."
            attention = ["Verify the route manually before generating a fare."]
        else:
            summary = "The order needs operator inspection."
            attention = ["Review dispatch and risk evidence."]

        evidence = []
        evidence.extend(event["reason"] for event in dispatch_events)
        evidence.extend(control for event in risk_events for control in event.get("controls", []))
        if driver:
            evidence.append(f"driver status: {driver['status']}")
            evidence.append(f"reservation_allowed: {driver['reservation_allowed']}")
            evidence.append(f"risk score: {driver['risk_score']}")

        llm_payload = {
            "order": {
                "order_id": order["order_id"],
                "status": order["status"],
                "blocked_reason": order.get("blocked_reason"),
                "distance_km": order.get("distance_km"),
                "eta_minutes": order.get("eta_minutes"),
                "passenger_price": order.get("passenger_price"),
                "special_note": order.get("special_note"),
            },
            "driver": {
                "driver_id": driver.get("driver_id") if driver else None,
                "status": driver.get("status") if driver else None,
                "reservation_allowed": driver.get("reservation_allowed") if driver else None,
                "risk_score": driver.get("risk_score") if driver else None,
                "documents": driver.get("documents") if driver else None,
            },
            "events": package["events"],
            "human_boundary": "AI can explain and recommend only. Risky actions require explicit operator approval.",
        }

        return {
            "success": True,
            "order_id": order_id,
            "summary": summary,
            "attention": attention,
            "evidence": evidence,
            "llm": self.llm.complete(llm_payload),
            "human_boundary": "No high-risk action has been executed by AI.",
        }

    def recommend_order_action(self, order_id: str) -> dict[str, Any]:
        package = self._evidence_package(order_id)
        order = package["order"]

        if order["status"] == "assigned":
            recommendation = "monitor"
            rationale = "The order is already assigned and no intervention is required."
            high_risk = False
        elif order.get("blocked_reason") == "no_driver_available":
            recommendation = "redispatch"
            rationale = "The operator can rebalance the zone or retry after more drivers come online."
            high_risk = True
        elif order.get("blocked_reason") == "driver_reservation_limited":
            recommendation = "manual_driver_restriction_review"
            rationale = "Driver documents are valid, but reservation eligibility is disabled."
            high_risk = True
        elif order.get("blocked_reason") == "map_route_unverified":
            recommendation = "manual_route_verification"
            rationale = "The route confidence is too low to quote or dispatch automatically."
            high_risk = True
        else:
            recommendation = "manual_review"
            rationale = "The order does not match a known low-risk automated path."
            high_risk = True

        action_id = f"act_{uuid4().hex[:12]}"
        record = {
            "record_type": "ai_recommendation",
            "action_id": action_id,
            "order_id": order_id,
            "ai_recommendation": recommendation,
            "rationale": rationale,
            "high_risk": high_risk,
            "decision": "pending_operator_decision",
            "created_at": utc_now(),
            "evidence": self.explain_order(order_id)["evidence"],
        }
        self.store.append_audit(record)
        return {
            "success": True,
            "action_id": action_id,
            "order_id": order_id,
            "recommendation": recommendation,
            "rationale": rationale,
            "high_risk": high_risk,
            "requires_human_approval": high_risk,
            "executed": False,
        }

    def decide_action(self, action_id: str, decision: str, operator_id: str, note: str = "") -> dict[str, Any]:
        audit = self.store.read_audit()
        recommendation = next(
            (
                record
                for record in reversed(audit)
                if record.get("action_id") == action_id and record.get("record_type") == "ai_recommendation"
            ),
            None,
        )
        if recommendation is None:
            raise KeyError(action_id)
        if decision not in {"approved", "rejected"}:
            raise ValueError("decision must be approved or rejected")

        final_effect = "no_state_change"
        if decision == "approved" and recommendation["ai_recommendation"] in HIGH_RISK_ACTIONS:
            final_effect = "operator_approved_demo_action_logged"
        elif decision == "approved":
            final_effect = "low_risk_action_acknowledged"

        record = {
            "record_type": "operator_decision",
            "action_id": action_id,
            "order_id": recommendation["order_id"],
            "ai_recommendation": recommendation["ai_recommendation"],
            "decision": decision,
            "approved_by": operator_id,
            "operator_note": note,
            "final_effect": final_effect,
            "created_at": utc_now(),
        }
        self.store.append_audit(record)
        return {
            "success": True,
            "action_id": action_id,
            "decision": decision,
            "executed_by_ai": False,
            "final_effect": final_effect,
            "audit_recorded": True,
        }

    def audit_log(self) -> dict[str, Any]:
        return {"success": True, "records": self.store.read_audit()}

    def system_explain(self) -> dict[str, Any]:
        cert = self.store.certification_summary()
        return {
            "success": True,
            "system": "GBA Go Operations Copilot",
            "architecture": [
                "Passenger and driver app signals",
                "Fare engine",
                "Dispatch engine",
                "State and risk engine",
                "PostgreSQL and Redis production evidence",
                "Operations Copilot",
                "Human approval and audit log",
            ],
            "certification_summary": cert,
            "operator_interpretation": (
                "The demo system turns dispatch, risk, fare, and stability evidence into an operator-readable "
                "summary. It does not let AI silently unlock drivers, cancel orders, or mutate state."
            ),
        }
