# Devpost Submission Draft

## Project Name

GBA Go Operations Copilot

## Tagline

AI-native operations support for explainable reservation mobility.

## Short Description

GBA Go Operations Copilot helps mobility operators understand abnormal reservation orders, inspect fare and dispatch evidence, receive AI-assisted recommendations, and approve or reject high-risk actions with a clear audit trail.

## Inspiration

Reservation mobility platforms fail in ways that are hard for both passengers and operators to understand. A passenger may see no driver assigned, a driver may be blocked by a rule, a fare may need explanation, or production stability may need human interpretation. GBA Go explores how Codex and OpenAI models can turn those operational signals into clear, auditable decisions.

## What It Does

GBA Go Operations Copilot provides an operator-facing API and browser-based demo console for reservation mobility operations. Given an order id, the Copilot reads synthetic order, fare, dispatch, driver, risk, and stability evidence. It explains what happened, recommends the next operational action, and requires a human operator to approve or reject high-risk actions.

Each explanation is grounded in structured demo evidence rather than allowing the model to invent operational facts. AI recommendations and human decisions are logged separately. Approval records the operator's decision in the demo audit flow and does not mutate any production mobility system.

## How We Built It

The demo is a FastAPI service with synthetic sample data, a browser-based operator console, audit logging, and a centralized OpenAI Responses API integration module with environment-based secret handling, ready for authenticated model calls. The broader GBA Go system was developed with Codex assistance across dispatch, state, pricing, risk, and certification work. For Build Week, we cut a safe standalone slice that avoids production credentials and real user data.

The founder defined the reservation-mobility product direction, driver-friendly economics, fixed platform-fee policy, human-in-the-loop governance boundaries, operational requirements, and final acceptance criteria. Codex accelerated implementation, debugging, testing, security review, and submission packaging.

## Challenges We Ran Into

The biggest challenge was scope control. GBA Go is a larger mobility system, but a hackathon submission needs a crisp story and a safe demo. We had to separate production evidence from submission-safe artifacts, avoid exposing secrets, and make the Copilot useful without letting AI silently execute risky operational changes.

## Accomplishments That We Are Proud Of

- A clear operator workflow: explain, recommend, approve or reject, audit.
- Human-in-the-loop governance for high-risk mobility actions.
- Synthetic demo data covering normal dispatch, no-driver exception, driver restriction review, and route verification.
- A centralized OpenAI Responses API integration module with environment-based secret handling, ready for authenticated model calls.
- Sanitized evidence from the pre-existing GBA Go backend production certification: a 20 QPS x 3600 second run with 72,000 completed requests, 72,000 successful requests, zero timeouts, zero state inconsistencies, and TSS 3.849986.
- `TEST_REPORT.md`, `SECURITY_SCAN_REPORT.md`, and `CODEX_CONTRIBUTIONS.md` as supporting evidence.

## What We Learned

AI is most valuable in mobility operations when it helps humans understand complex system evidence. The goal is not to replace operators or bypass policy. The best pattern is AI explanation plus human approval plus auditability.

## What's Next

- Connect the Copilot to a staging GBA Go backend.
- Add richer policy-aware recommendations.
- Add role-based approval permissions.
- Add redaction and prompt review dashboards.
- Expand the demo into live operational workflows for dispatch support, fare explanation, and production incident review.

## Built With

OpenAI, Codex, OpenAI Responses API, Python, FastAPI, Uvicorn, HTML, JavaScript, JSON, REST API, Pytest, Make, synthetic sample data.

## Category

Work and Productivity

## Testing Instructions

```bash
git clone REPOSITORY_URL
cd gba-go-build-week
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make demo
```

Open `http://127.0.0.1:8017`.

Demo order ids:

- `trip_demo_001`
- `trip_demo_002`
- `trip_demo_003`
- `trip_demo_004`

Run tests:

```bash
make test
```

Run security scan:

```bash
make security-scan
```

Optional authenticated AI path:

```bash
export COPILOT_LLM_MODE=openai
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=your_model_name
make demo
```

## Privacy and Safety

This submission uses synthetic data only. It excludes production databases, Redis URLs, Railway variables, API keys, Apple signing files, real passenger or driver information, raw coordinates, and internal admin endpoints. AI cannot directly execute redispatch, unlock drivers, cancel orders, or mutate high-risk state; operator approval is required and audited.

If the OpenAI API is unavailable or no API key is configured, the demo fails safely and cannot perform any high-risk action. If no OpenAI API key is configured, the demo can use deterministic sample explanations for local evaluation, clearly labeled as non-model output.

## What Is New During Build Week

The standalone Operations Copilot demo slice, sample data, API endpoints, OpenAI client module, audit flow, browser demo console, README, security report, and Devpost submission package were assembled for Build Week. The broader GBA Go concept and earlier engineering work existed before Build Week and are disclosed as pre-existing background.

These additions are isolated in the Build Week repository and can be verified through the repository commit history, automated tests, security scan report, and Codex session records.
