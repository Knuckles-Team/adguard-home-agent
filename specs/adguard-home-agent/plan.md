# CONN-ADGUARD-HOME-AGENT — Design and implementation plan

Governing specification: [spec.md](spec.md).

## Existing system and reuse

The connector reuses the SDK TLS profile resolver. The connector owns operation mappings only.

## Architecture

`auth.get_client` builds `Api`. TLS trust comes from the `adguard` profile (`ADGUARD_CA_BUNDLE`, `ADGUARD_CA_BUNDLE_REF`, `ADGUARD_TLS_PROFILE`) The SDK `BaseApiClient` resolves the same `ADGUARD` profile and builds the httpx client; `Api` adds the AdGuard result shapes. Retry on 429 comes from the SDK. There is no switch that disables verification.

## Quality and release gates

Run `pre-commit run --all-files` and `pytest`.
