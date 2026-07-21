#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8017}"

curl -fsS "$BASE_URL/health" >/dev/null
curl -fsS -X POST "$BASE_URL/copilot/orders/trip_demo_001/explain" >/dev/null
ACTION_ID="$(curl -fsS -X POST "$BASE_URL/copilot/orders/trip_demo_003/recommend" | python3 -c 'import json,sys; print(json.load(sys.stdin)["action_id"])')"
curl -fsS -X POST "$BASE_URL/copilot/actions/$ACTION_ID/approve" \
  -H 'Content-Type: application/json' \
  -d '{"operator_id":"demo_operator","note":"smoke approval"}' >/dev/null
curl -fsS "$BASE_URL/copilot/audit" >/dev/null
curl -fsS "$BASE_URL/copilot/system/explain" >/dev/null

echo "Smoke demo passed against $BASE_URL"

