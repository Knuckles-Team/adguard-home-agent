# CONN-ADGUARD-HOME-AGENT — Requirements

Governing specification: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ADGUARD-HOME-AGENT-R001` | **Verified transport.** The connector must take TLS trust from the SDK `resolve_tls_profile` in `adguard_home_agent/auth.py` and `adguard_home_agent/api_client.py`, verify server certificates by default, carry any per-instance CA through the profile, and never silence the insecure-request warning. | `tests/test_tls_profile.py` must observe verification on by default, a configured CA carried onto the session, and no call to disable warnings. |
