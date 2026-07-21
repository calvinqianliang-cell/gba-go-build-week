import json
import os
import urllib.error
import urllib.request
from typing import Any


SYSTEM_PROMPT = (
    "You are GBA Go Operations Copilot. Explain reservation mobility operations "
    "using only the sanitized evidence provided. Do not invent private data, do "
    "not claim an action has been executed, and always preserve human approval "
    "as the boundary for risky operational changes."
)


def _extract_response_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    chunks: list[str] = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str):
                chunks.append(text)
    return "\n".join(chunks).strip()


class LLMClient:
    def __init__(self) -> None:
        self.mode = os.getenv("COPILOT_LLM_MODE", "local").lower()
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.6")
        self.timeout = int(os.getenv("OPENAI_TIMEOUT_SECONDS", "20"))

    def summarize_input(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "order_id": payload.get("order", {}).get("order_id"),
            "status": payload.get("order", {}).get("status"),
            "dispatch_event_count": len(payload.get("events", {}).get("dispatch", [])),
            "risk_event_count": len(payload.get("events", {}).get("risk", [])),
            "contains_raw_phone": False,
            "contains_raw_location_coordinates": False,
        }

    def complete(self, payload: dict[str, Any]) -> dict[str, Any]:
        input_summary = self.summarize_input(payload)
        if self.mode != "openai":
            return {
                "used_model": False,
                "status": "local_mode",
                "model": None,
                "input_summary": input_summary,
                "message": "COPILOT_LLM_MODE is local; no data was sent to OpenAI.",
            }
        if not self.api_key:
            return {
                "used_model": False,
                "status": "skipped_no_api_key",
                "model": self.model,
                "input_summary": input_summary,
                "message": "OPENAI_API_KEY is required when COPILOT_LLM_MODE=openai.",
            }

        body = {
            "model": self.model,
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            return {
                "used_model": False,
                "status": "openai_http_error",
                "model": self.model,
                "input_summary": input_summary,
                "message": f"OpenAI API returned HTTP {exc.code}.",
                "error_excerpt": error_body[:500],
            }
        except Exception as exc:  # pragma: no cover - network path depends on user env
            return {
                "used_model": False,
                "status": "openai_request_error",
                "model": self.model,
                "input_summary": input_summary,
                "message": str(exc),
            }

        return {
            "used_model": True,
            "status": "completed",
            "model": self.model,
            "input_summary": input_summary,
            "output_summary": _extract_response_text(data)[:1200],
            "response_id": data.get("id"),
        }

