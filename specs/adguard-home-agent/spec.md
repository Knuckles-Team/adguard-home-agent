# CONN-ADGUARD-HOME-AGENT — AdGuard Home connector

## Outcome

The connector must expose reviewed DNS-filter operations through one governed integration boundary.
The connector must preserve credential, transport, source, and content contracts.

## Scope and owner

The `adguard-home-agent` repository owns DNS-filter operations and source mappings.
The shared connector SDK owns reusable transport, authentication, TLS, MCP, and ingest contracts.
The shared pipelines repository owns quality gates and delivery rendering.

Component: Connector integration
References: [Connector SDK](https://github.com/Knuckles-Team/agent-connector-sdk/blob/main/README.md)
Code: ../../adguard_home_agent/auth.py ../../adguard_home_agent/api_client.py ../../tests/test_tls_profile.py

## Non-goals

This specification grants no service access, credential creation, deployment, or approval exception.
The connector must not implement a graph engine, independent policy authority, or duplicate SDK runtime.

## Why a new spec

The repository had no local specification. The existing `specs/` tree held only the template. The transport defect (verification off by default, warning silenced) needs an owner, so this is the repository's first capability specification. Rows R002 to R004 move the client onto the SDK governed client.

## Requirements

See [requirements.md](requirements.md), [plan.md](plan.md), and [test-spec.md](test-spec.md).
