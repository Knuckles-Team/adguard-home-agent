# CONN-ADGUARD-HOME-AGENT — Verification plan

Governing specification: [spec.md](spec.md).

| Requirement | Verification target |
|---|---|
| `CONN-ADGUARD-HOME-AGENT-R001` | `tests/test_tls_profile.py` must observe verification on by default, a configured CA carried into the client trust, and no call to disable warnings. |
| `CONN-ADGUARD-HOME-AGENT-R002` | `tests/test_sdk_transport.py::test_client_is_the_sdk_base_client` and `::test_rate_limit_backoff_comes_from_the_sdk` must pass. |
| `CONN-ADGUARD-HOME-AGENT-R003` | `tests/test_sdk_transport.py::test_request_shapes_are_unchanged` must pass. |
| `CONN-ADGUARD-HOME-AGENT-R004` | `tests/test_sdk_transport.py::test_dependencies_come_from_the_sdk` must pass. |

The owner must retain failure evidence and use canonical lifecycle tooling to regenerate `status.json`.

## Adoption of scion-sdk 0.10.0 (`CONN-ADGUARD-HOME-AGENT-R005`)

| Requirement | Test | Observation |
|---|---|---|
| `CONN-ADGUARD-HOME-AGENT-R005` | `tests/test_scion_sdk_0_10_imports.py::test_every_scion_sdk_import_resolves_on_the_pinned_release` | Every `scion_sdk` import resolves on the pinned release; a removed path fails the test. |
