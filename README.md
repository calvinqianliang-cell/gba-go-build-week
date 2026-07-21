# GBA Go Operations Copilot

GBA Go Operations Copilot is a Build Week demo cut from the GBA Go reservation mobility system. It shows how an operator-facing AI layer can explain fare, dispatch, driver restriction, risk, and production stability evidence while keeping high-risk actions behind explicit human approval.

This repository is intentionally small. It uses synthetic sample data and does not include production databases, Redis URLs, Railway variables, Apple signing files, user records, or internal admin routes.

## What It Does

- Explains why a reservation order was assigned, blocked, or routed to operator review.
- Recommends operational actions such as redispatch, driver restriction review, or route verification.
- Blocks AI from executing risky actions directly.
- Requires an operator to approve or reject each action.
- Writes AI recommendations and operator decisions to an audit log.
- Grounds each explanation in structured demo evidence instead of allowing the model to invent operational facts.
- Includes a centralized OpenAI Responses API integration module with environment-based secret handling in `operations_copilot/llm_client.py`, ready for authenticated model calls.
- Runs without an API key in local mode so judges can inspect the demo safely.

## Demo Orders

- `trip_demo_001`: normal assigned reservation.
- `trip_demo_002`: no eligible driver after dispatch filtering.
- `trip_demo_003`: driver is available but reservation-limited, so operator review is required.
- `trip_demo_004`: route confidence is too low to quote automatically.

## Quick Start

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make demo
```

Open:

```text
http://127.0.0.1:8017
```

Run tests:

```bash
make test
```

Optional pytest suite:

```bash
pytest -q
```

Run the security scan:

```bash
make security-scan
```

## Optional Authenticated AI Path

The demo defaults to local mode so no sample data leaves the machine. In that mode it uses deterministic sample explanations clearly labeled as non-model output.

To use the authenticated OpenAI path, provide a valid API key and model name at runtime:

```bash
export COPILOT_LLM_MODE=openai
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=your_model_name
make demo
```

The client sends only a minimized order summary, driver eligibility fields, dispatch/risk evidence, and the human-approval boundary. It does not send phone numbers, raw coordinates, payment credentials, or production hostnames.

If the OpenAI API is unavailable or no API key is configured, the demo fails safely and cannot perform any high-risk action.

## API

```text
POST /copilot/orders/{order_id}/explain
POST /copilot/orders/{order_id}/recommend
POST /copilot/actions/{action_id}/approve
POST /copilot/actions/{action_id}/reject
GET  /copilot/audit
GET  /copilot/system/explain
GET  /health
```

## Example Flow

```bash
curl -X POST http://127.0.0.1:8017/copilot/orders/trip_demo_003/explain
curl -X POST http://127.0.0.1:8017/copilot/orders/trip_demo_003/recommend
curl -X POST http://127.0.0.1:8017/copilot/actions/ACT_ID/approve \
  -H 'Content-Type: application/json' \
  -d '{"operator_id":"demo_operator","note":"Approved for demo"}'
curl http://127.0.0.1:8017/copilot/audit
```

## Architecture

```text
Passenger / Driver Signals
        |
Fare + Dispatch + State + Risk Evidence
        |
Synthetic Sample Data for Demo
        |
Operations Copilot
        |
Explain / Recommend
        |
Human Approval
        |
Audit Log
```

## Codex Usage

Codex helped turn a larger production mobility project into a safe Build Week demo slice. The work focused on scoping, architecture explanation, synthetic data, API implementation, tests, security scanning, and truthful submission packaging. The production system history includes Codex-assisted debugging around dispatch, state consistency, cache/read-model behavior, and long-run stability evidence.

The founder defined the reservation-mobility product direction, driver-friendly economics, fixed platform-fee policy, human-in-the-loop governance boundaries, operational requirements, and final acceptance criteria. Codex accelerated implementation, debugging, testing, security review, and submission packaging.

## Human Boundary

AI recommendations never unlock drivers, cancel orders, redispatch, or mutate production state directly. The operator must explicitly approve or reject every high-risk recommendation, and the decision is recorded separately from the AI recommendation.

Approval records the operator's decision in the demo audit flow and does not mutate any production mobility system.

## Security

See `SECURITY.md` and `SECURITY_SCAN_REPORT.md`.

## Known Limits

- This repository is a demo slice, not the full production backend.
- Sample data is synthetic.
- Docker support is included, but local virtualenv startup is the primary tested path.
- OpenAI mode requires a valid API key supplied by the operator at runtime.
