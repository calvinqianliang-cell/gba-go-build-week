# Security

This Build Week repository is designed to be shareable.

## Included

- Synthetic passengers, drivers, trips, dispatch events, and risk events.
- Sanitized stability certification summary.
- Local demo audit log path.
- OpenAI model calling code that reads `OPENAI_API_KEY` from the environment.

## Excluded

- Production database URLs.
- Redis URLs.
- Railway variables.
- OpenAI API keys.
- Apple developer certificates or signing files.
- Supabase credentials.
- JWT or session secrets.
- Real passenger or driver identities.
- Real phone numbers, addresses, order locations, or coordinates.
- Internal production admin routes.
- Production backups and logs.

## Model Data Policy

When `COPILOT_LLM_MODE=openai`, the LLM client sends a minimized evidence package:

- order id
- order status
- blocked reason
- fare summary
- driver eligibility status
- risk and dispatch evidence
- human approval boundary

It does not send raw personal identifiers, credentials, phone numbers, exact coordinates, or production infrastructure details.

## Reporting

If you find a security issue in this demo repository, open a private issue or contact the project owner directly. Do not publish secrets or exploit details publicly.

