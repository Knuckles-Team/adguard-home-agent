# CONN-ADGUARD-HOME-AGENT — Design and implementation plan

Governing specification: [spec.md](spec.md).

## Existing system and reuse

The connector reuses the SDK TLS profile resolver. The connector owns operation mappings only.

## Architecture

`auth.get_client` resolves the `adguard` TLS profile (`ADGUARD_CA_BUNDLE`, `ADGUARD_CA_BUNDLE_REF`, `ADGUARD_TLS_PROFILE`) and hands it to `Api`, which applies it to its requests session. There is no switch that disables verification.

## Quality and release gates

Run `pre-commit run --all-files` and `pytest`.
