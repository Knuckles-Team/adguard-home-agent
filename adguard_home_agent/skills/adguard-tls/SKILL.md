---
name: adguard-tls
description: Manage TLS configuration in AdGuard Home.
tags: [tls]
---

# AdGuard Home TLS Agent

This agent is responsible for managing the TLS configuration in AdGuard Home.

## Capabilities

- **Get TLS Status**: Retrieve current TLS configuration and status.
- **Configure TLS**: Update TLS configuration.
- **Validate TLS**: Validate TLS configuration.

## Tools

### `get_tls_status`
- **Description**: Get TLS status.
- **Parameters**: None (uses default connection settings).

### `configure_tls`
- **Description**: Configure TLS.
- **Parameters**:
    - `config` (dict): TLS configuration object.

### `validate_tls`
- **Description**: Validate TLS configuration.
- **Parameters**:
    - `config` (dict): TLS configuration object to validate.
