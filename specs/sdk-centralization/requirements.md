# CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A child row `.n` is one five-minute unit of work. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001` | **Transport comes from the SDK (rollup).** The connector must use the SDK for HTTP, retry and TLS. Children `.1` to `.4` deliver it. | See each child. |
| `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.1` | **Governed client.** The `Api` client must subclass the SDK `BaseApiClient` and must not import `requests` or `urllib3` (`SDK-CENTRALIZED-CAPABILITIES-R001`, `SDK-CENTRALIZED-CAPABILITIES-R003`). It must send HTTP basic credentials through the SDK `BasicAuth`. The 429 backoff comes from the SDK. Proving test: `tests/test_sdk_transport.py::test_client_is_the_sdk_base_client`. | The client is an SDK base client and the package imports no `requests`. |
| `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.2` | **TLS profile only.** The connector must take transport trust from `resolve_tls_profile` for the `ADGUARD` settings prefix (`SDK-CENTRALIZED-CAPABILITIES-R008`). It must not read a verification flag, must not silence TLS warnings and must refuse a `verify` override. Proving test: `tests/test_sdk_transport.py::test_verification_cannot_be_disabled`. | A verify override is refused and the factory reads no verification flag. |
| `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.3` | **Same behaviour.** Each API method must keep its path, body and result shape. An error status must raise `AdGuard API error: <status> - <text>`. A 204 or empty body must return a success marker. Proving test: `tests/test_sdk_transport.py::test_request_shapes_are_unchanged`. | A request sends basic auth and a JSON body, and each status maps as before. |
| `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.4` | **SDK floor.** The package must depend on `agent-connector-sdk[mcp]` at the latest release floor and must not pin `requests` (`SDK-CENTRALIZED-CAPABILITIES-R040`). Proving test: `tests/test_sdk_transport.py::test_dependencies_come_from_the_sdk`. | `pyproject.toml` has no `requests` pin and the SDK floor is `0.3.11` or later. |
