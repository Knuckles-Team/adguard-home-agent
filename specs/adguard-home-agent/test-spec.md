# CONN-ADGUARD-HOME-AGENT — Verification plan

Governing specification: [spec.md](spec.md).

| Requirement | Verification target |
|---|---|
| `CONN-ADGUARD-HOME-AGENT-R001` | `tests/test_tls_profile.py` must observe verification on by default, a configured CA carried onto the session, and no call to disable warnings. |

The owner must retain failure evidence and use canonical lifecycle tooling to regenerate `status.json`.
