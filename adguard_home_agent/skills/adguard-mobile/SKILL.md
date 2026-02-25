---
name: adguard-mobile
description: Retrieve mobile configuration files for AdGuard Home.
tags: [mobile]
---

# AdGuard Home Mobile Config Agent

This agent is responsible for retrieving mobile configuration files (.mobileconfig) for iOS/macOS devices.

## Capabilities

- **Get DoH Config**: Retrieve DNS-over-HTTPS .mobileconfig.
- **Get DoT Config**: Retrieve DNS-over-TLS .mobileconfig.

## Tools

### `get_doh_mobile_config`
- **Description**: Get DNS over HTTPS .mobileconfig.
- **Parameters**:
    - `host` (str): Host name.
    - `client_id` (str): Client ID.

### `get_dot_mobile_config`
- **Description**: Get DNS over TLS .mobileconfig.
- **Parameters**:
    - `host` (str): Host name.
    - `client_id` (str): Client ID.
