# CONN-ADGUARD-HOME-AGENT — AdGuard Home connector

## Outcome

The connector must expose reviewed DNS-filter operations through one governed integration boundary.
The connector must preserve credential, transport, source, and content contracts.

## Scope and owner

The `adguard-home-agent` repository owns DNS-filter operations and source mappings.
The shared connector SDK owns reusable transport, authentication, TLS, MCP, and ingest contracts.
The shared pipelines repository owns quality gates and delivery rendering.

Component: Connector integration
References: [Connector SDK](https://github.com/Knuckles-Team/scion-sdk/blob/main/README.md)
Code: ../../adguard_home_agent/auth.py ../../adguard_home_agent/api_client.py ../../tests/test_tls_profile.py

## Non-goals

This specification grants no service access, credential creation, deployment, or approval exception.
The connector must not implement a graph engine, independent policy authority, or duplicate SDK runtime.

## Why a new spec

The repository had no local specification. The existing `specs/` tree held only the template. The transport defect (verification off by default, warning silenced) needs an owner, so this is the repository's first capability specification. Rows R002 to R004 move the client onto the SDK governed client.

## Requirements

See [requirements.md](requirements.md), [plan.md](plan.md), and [test-spec.md](test-spec.md).

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - AdGuard Home connector (Priority: P1)

The connector must expose reviewed DNS-filter operations through one governed integration boundary.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-ADGUARD-HOME-AGENT-R001` (verified transport) is exercised, **Then** `tests/test_tls_profile.py` must observe verification on by default, a configured CA carried into the client trust, and no call to disable warnings. Test: `tests/test_tls_profile.py::test_default_verifies`.
2. **Given** the connector is configured, **When** the behaviour of row `CONN-ADGUARD-HOME-AGENT-R002` (governed client) is exercised, **Then** `tests/test_sdk_transport.py::test_client_is_the_sdk_base_client` and `::test_rate_limit_backoff_comes_from_the_sdk` must pass.
3. **Given** the connector is configured, **When** the behaviour of row `CONN-ADGUARD-HOME-AGENT-R003` (same behaviour) is exercised, **Then** `tests/test_sdk_transport.py::test_request_shapes_are_unchanged` must pass.

### Edge Cases

- If `CONN-ADGUARD-HOME-AGENT-R001` is not met, its proving test fails: verified transport.
- If `CONN-ADGUARD-HOME-AGENT-R002` is not met, its proving test fails: governed client.
- If `CONN-ADGUARD-HOME-AGENT-R003` is not met, its proving test fails: same behaviour.

## Requirements

- **FR-001**: Verified transport. Rows: `CONN-ADGUARD-HOME-AGENT-R001`.
- **FR-002**: Governed client. Rows: `CONN-ADGUARD-HOME-AGENT-R002`.
- **FR-003**: Same behaviour. Rows: `CONN-ADGUARD-HOME-AGENT-R003`.
- **FR-004**: SDK floor. Rows: `CONN-ADGUARD-HOME-AGENT-R004`.

## Success Criteria

- **SC-001**: `tests/test_tls_profile.py` must observe verification on by default, a configured CA carried into the client trust, and no call to disable warnings. Rows: `CONN-ADGUARD-HOME-AGENT-R001`.
- **SC-002**: `tests/test_sdk_transport.py::test_client_is_the_sdk_base_client` and `::test_rate_limit_backoff_comes_from_the_sdk` must pass. Rows: `CONN-ADGUARD-HOME-AGENT-R002`.
- **SC-003**: `tests/test_sdk_transport.py::test_request_shapes_are_unchanged` must pass. Rows: `CONN-ADGUARD-HOME-AGENT-R003`.
- **SC-004**: `tests/test_sdk_transport.py::test_dependencies_come_from_the_sdk` must pass. Rows: `CONN-ADGUARD-HOME-AGENT-R004`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-ADGUARD-HOME-AGENT-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-ADGUARD-HOME-AGENT-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-ADGUARD-HOME-AGENT-R003` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
| FR-004 | `CONN-ADGUARD-HOME-AGENT-R004` | [plan.md](plan.md) | T-004 | [test-spec.md](test-spec.md) |
