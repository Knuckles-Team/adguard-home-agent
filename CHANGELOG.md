# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.17.6] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [0.17.5] - 2026-10-23

### Changed
- Requires `agent-connector-sdk>=0.4.1`; data sources are declared in code (`connector_sources`).

## [Unreleased]

- The client is now built on the SDK governed HTTP client (`BaseApiClient`); the own `requests` session and pin are removed. 429 backoff comes from the SDK.

## [0.17.1]

### Security
- TLS now comes from the SDK `resolve_tls_profile`: verification is always on, a per-instance CA is set with `ADGUARD_CA_BUNDLE`, and the insecure-request warning is no longer silenced. `ADGUARD_SSL_VERIFY` is removed.

### Added
-

### Changed
-

### Fixed
-

## [0.2.55] - 2026-04-29

### Added
- Initial release
