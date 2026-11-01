# CONN-ADGUARD-HOME-AGENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

The connector reuses the SDK TLS profile resolver. The connector owns operation mappings only. `auth.get_client` builds `Api`. TLS trust comes from the `adguard` profile (`ADGUARD_CA_BUNDLE`, `ADGUARD_CA_BUNDLE_REF`, `ADGUARD_TLS_PROFILE`) The SDK `BaseApiClient` resolves the same `ADGUARD` profile and builds the httpx client; `Api` adds the AdGuard result shapes. Retry on 429 comes from the SDK. There is no switch that disables verification.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest; the proof level each row names
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; shared capabilities come from the SDK
- **Scale/Scope**: 4 rows

## Constitution Check

- One owner per concept: pass. The connector owns one external system's calls, mappings and tools only.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
adguard_home_agent/auth.py  existing
adguard_home_agent/api_client.py  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

### Quality and release gates

Run `pre-commit run --all-files` and `pytest`.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-ADGUARD-HOME-AGENT-R001`: console_script adguard-home-agent (scion_sdk.cli:serve L18) -> scion_sdk installed_connectors -> adguard_home_agent/__init__.py::connector -> adguard_home_agent/auth.py::get_client -> adguard_home_agent/api_client.py::Api (L18) -> BaseApiClient with tls_service ADGUARD resolving the SDK TLS profile.
2. `CONN-ADGUARD-HOME-AGENT-R002`: console_script adguard-home-agent (scion_sdk.cli:serve L18) -> scion_sdk installed_connectors -> adguard_home_agent/__init__.py::connector -> adguard_home_agent/auth.py::get_client -> adguard_home_agent/api_client.py::Api (L18) -> BasicAuth and BaseApiClient._send.
3. `CONN-ADGUARD-HOME-AGENT-R003`: console_script adguard-home-agent (scion_sdk.cli:serve L18) -> scion_sdk installed_connectors -> adguard_home_agent/__init__.py::connector -> adguard_home_agent/auth.py::get_client -> adguard_home_agent/api_client.py::Api (L18).request (L40) which every API method calls.
4. `CONN-ADGUARD-HOME-AGENT-R004`: package install -> pyproject.toml dependencies -> scion_sdk consumed by adguard_home_agent/api_client.py and the console_script adguard-home-agent.

## Cross-repo seams

none. The cited owner rows are library capabilities the connector calls in process; spec.md names them.
