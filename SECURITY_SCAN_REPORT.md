# Security Scan Report

Generated on 2026-07-21 Asia/Shanghai.

## Scope

Scanned the standalone Build Week repository:

```text
/Users/calvin.q/Desktop/WenXinXiShuoClean/gba-go-build-week
```

The repository was created as a new demo slice. It does not import the production Git history.

## Exclusions

The scanner excludes:

- `.venv`
- `.git`
- `demo_runtime`
- `__pycache__`
- `.pytest_cache`
- `.env.example`
- `SECURITY_SCAN_REPORT.md`
- `scripts/security_scan.sh`

These exclusions avoid false positives in third-party packages and the scanner's own pattern text.

## Patterns Checked

```text
sk-
postgresql://
postgres://
redis://
rediss://
password=
secret=
token=
api_key=
api-key=
PRIVATE KEY
```

## Current Tree Result

```text
Scanning current files for obvious secrets...
Security scan completed. Review any lines above before sharing.
```

No source-file findings were printed.

## Sensitive Data Handling

Removed or avoided:

- Production database URLs.
- Redis URLs.
- Railway variables.
- OpenAI API keys.
- Supabase credentials.
- JWT and session secrets.
- Apple signing files and certificates.
- Real passengers, drivers, phone numbers, exact coordinates, and real order locations.
- Internal production admin endpoints.

## Git History

No production Git history was copied into this demo repository. After initialization, the repository history contains only the standalone Build Week demo files.

## Verdict

```text
No obvious source-file secrets found in the standalone demo repository.
Repository is suitable for sharing after the user reviews eligibility and Devpost submission fields.
```

