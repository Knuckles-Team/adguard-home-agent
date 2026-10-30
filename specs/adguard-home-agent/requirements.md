# CONN-ADGUARD-HOME-AGENT — Requirements

Governing specification: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ADGUARD-HOME-AGENT-R001` | **Verified transport.** The connector must take TLS trust from the SDK `resolve_tls_profile` in `adguard_home_agent/auth.py` and `adguard_home_agent/api_client.py`, verify server certificates by default, carry any per-instance CA through the profile into the client trust, and never silence the insecure-request warning. | `tests/test_tls_profile.py` must observe verification on by default, a configured CA carried into the client trust, and no call to disable warnings. |
| `CONN-ADGUARD-HOME-AGENT-R002` | **Governed client.** The `Api` client in `adguard_home_agent/api_client.py` must subclass the SDK `BaseApiClient` (`SCION-CENTRALIZED-CAPABILITIES-R001`, `SCION-CENTRALIZED-CAPABILITIES-R003`), send basic credentials through the SDK `BasicAuth`, and take the 429 backoff from the SDK. The package must not import `requests` or `urllib3`. | `tests/test_sdk_transport.py::test_client_is_the_sdk_base_client` and `::test_rate_limit_backoff_comes_from_the_sdk` must pass. |
| `CONN-ADGUARD-HOME-AGENT-R003` | **Same behaviour.** Each API method must keep its path, body and result shape. An error status must raise `AdGuard API error: <status> - <text>`. A 204 or empty body must return a success marker. | `tests/test_sdk_transport.py::test_request_shapes_are_unchanged` must pass. |
| `CONN-ADGUARD-HOME-AGENT-R004` | **SDK floor.** The package must depend on `scion-sdk[mcp]` at the latest release floor and must not pin `requests` (`SCION-CENTRALIZED-CAPABILITIES-R040`). | `tests/test_sdk_transport.py::test_dependencies_come_from_the_sdk` must pass. |
