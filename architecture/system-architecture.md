# System Architecture

```text
Passenger / Driver iOS App
        |
GBA Go API Gateway
        |
+------------------+------------------+----------------+
| Fare Engine      | Dispatch Engine  | Risk Engine    |
+------------------+------------------+----------------+
        |
State Engine + Event Evidence
        |
PostgreSQL + Redis production topology evidence
        |
Operations Copilot
        |
Human Approval + Audit Log
```

## Fare Engine

Calculates passenger-facing fare evidence and keeps driver income separate from platform fee. The demo sample data exposes the fare breakdown but not production pricing secrets.

## Dispatch Engine

Filters available drivers by status, reservation eligibility, risk controls, and service tags. The Copilot reads dispatch evidence and explains why a driver was assigned or blocked.

## State Engine

Preserves order truth as a state-action path. In the production system this avoids hidden controller-side mutations. In the demo, state is represented by synthetic JSON fixtures.

## Risk Engine

Marks orders that need manual review. Copilot can explain risk evidence but cannot override a hold on its own.

## PostgreSQL and Redis

The production system uses PostgreSQL for durable state and Redis for read-model/cache behavior. The demo includes only a sanitized stability summary; it does not include live connection strings.

## Operations Copilot

The Copilot has two powers:

- Explain what happened.
- Recommend what an operator may do next.

It does not directly unlock drivers, cancel orders, mutate order status, or bypass risk controls.

## Human Approval

Every high-risk recommendation requires an explicit operator decision. The audit log stores the AI recommendation, the human decision, and the final demo effect as separate records.

