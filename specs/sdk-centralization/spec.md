# CONN-ADGUARD-HOME-AGENT-SDK-CENTRALIZATION — Transport through the SDK

Owner: adguard-home-agent. Cross-repo IDs: `SDK-CENTRALIZED-CAPABILITIES-R001`, `SDK-CENTRALIZED-CAPABILITIES-R003`, `SDK-CENTRALIZED-CAPABILITIES-R008`, `SDK-CENTRALIZED-CAPABILITIES-R040`.

Extends: [SDK-CENTRALIZED-CAPABILITIES](https://github.com/Knuckles-Team/agent-connector-sdk/blob/main/specs/centralized-capabilities/spec.md)

## Purpose and user stories

The connector must reach AdGuard Home through the SDK. The SDK owns the governed HTTP client, retry and TLS profiles.

An operator points the connector at AdGuard Home. Transport security comes from one TLS profile, not from a connector flag.

## Requirements and acceptance

The rows are in [requirements.md](requirements.md). The proving tests are in [test-spec.md](test-spec.md).

## Why a new spec

The search covered `specs/` of this repository and the SDK centralized-capabilities spec. This repository had no spec for transport. The SDK owns the capability. This spec states how this connector uses it.

## Scope and interfaces

In scope: the connector's HTTP client, TLS handling and dependency floor.

Out of scope: the tool surface, which stays one tool per API operation, and the SDK modules themselves.
