# CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Level | Setup and input | Expected observation | Evidence |
|---|---|---|---|---|---|
| T-001 | `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001` | Unit | Every child row. | See each child. |  |
| T-002 | `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.1` | Unit | `tests/test_sdk_transport.py::test_client_is_the_sdk_base_client` | The client is an SDK base client and the package imports no `requests`. |  |
| T-003 | `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.2` | Unit | `tests/test_sdk_transport.py::test_verification_cannot_be_disabled` | A verify override is refused and the factory reads no verification flag. |  |
| T-004 | `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.3` | Unit | `tests/test_sdk_transport.py::test_request_shapes_are_unchanged` | A request sends basic auth and a JSON body, and each status maps as before. |  |
| T-005 | `CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION-R001.4` | Unit | `tests/test_sdk_transport.py::test_dependencies_come_from_the_sdk` | `pyproject.toml` has no `requests` pin and the SDK floor is `0.3.11` or later. |  |
