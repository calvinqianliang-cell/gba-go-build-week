from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from operations_copilot.copilot_service import CopilotService


ROOT = Path(__file__).resolve().parents[1]
service = CopilotService()

app = FastAPI(
    title="GBA Go Operations Copilot",
    version="build-week-demo",
    description="Safe demo API for OpenAI Build Week submission.",
)


class DecisionRequest(BaseModel):
    operator_id: str = "demo_operator"
    note: str = ""


@app.get("/", response_class=HTMLResponse)
def demo_home() -> str:
    return (ROOT / "demo" / "index.html").read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict:
    return {
        "success": True,
        "service": "GBA Go Operations Copilot",
        "mode": "demo",
        "high_risk_ai_actions": "blocked_without_operator_approval",
    }


@app.post("/copilot/orders/{order_id}/explain")
def explain_order(order_id: str) -> dict:
    try:
        return service.explain_order(order_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown order_id: {order_id}") from None


@app.post("/copilot/orders/{order_id}/recommend")
def recommend_order(order_id: str) -> dict:
    try:
        return service.recommend_order_action(order_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown order_id: {order_id}") from None


@app.post("/copilot/actions/{action_id}/approve")
def approve_action(action_id: str, request: DecisionRequest) -> dict:
    try:
        return service.decide_action(action_id, "approved", request.operator_id, request.note)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown action_id: {action_id}") from None


@app.post("/copilot/actions/{action_id}/reject")
def reject_action(action_id: str, request: DecisionRequest) -> dict:
    try:
        return service.decide_action(action_id, "rejected", request.operator_id, request.note)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown action_id: {action_id}") from None


@app.get("/copilot/audit")
def audit() -> dict:
    return service.audit_log()


@app.get("/copilot/system/explain")
def system_explain() -> dict:
    return service.system_explain()

