# Test Report

Generated on 2026-07-21 Asia/Shanghai.

## Environment

- Repository path: `/Users/calvin.q/Desktop/WenXinXiShuoClean/gba-go-build-week`
- Python virtual environment: `.venv`
- Demo URL: `http://127.0.0.1:8017`
- OpenAI live mode: not run because no `OPENAI_API_KEY` was provided.
- OpenAI integration path: implemented in `operations_copilot/llm_client.py`.

## Commands Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/run_tests.py
.venv/bin/python -m pytest -q
bash scripts/security_scan.sh
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8017
bash scripts/smoke_demo.sh
```

## Results

```text
All critical demo tests passed
```

```text
6 passed in 0.22s
```

```text
Smoke demo passed against http://127.0.0.1:8017
```

## Coverage

- Health endpoint.
- Order explanation endpoint.
- Unknown order 404 behavior.
- Copilot recommendation endpoint.
- Human approval endpoint.
- Human rejection endpoint.
- Audit log endpoint.
- System explanation endpoint.
- Sanitized certification summary.
- No-API-key friendly behavior.

## Remaining Test Gaps

- Live OpenAI model call was not executed because no API key was available in this environment.
- Docker startup was not executed in this run.
- Devpost final submission still requires repository URL, video URL, session/feedback details if requested, truthful eligibility fields, and the user's final Submit confirmation.

## Verdict

```text
All critical demo tests passed
BUILD_WEEK_ENGINEERING_PACKET_READY
BUILD_WEEK_SUBMISSION_IN_PROGRESS
```
