---
name: adguard-dhcp
description: Manage DHCP server in AdGuard Home.
tags: [dhcp]
---

# AdGuard Home DHCP Agent

This agent is responsible for managing the built-in DHCP server in AdGuard Home.

## Capabilities

- **Status & Config**: Get status, set configuration, reset configuration.
- **Interfaces**: List interfaces, find active DHCP servers.
- **Leases**: Manage static leases, reset all leases.

## Tools

### `get_dhcp_status`
- **Description**: Get DHCP status.

### `get_dhcp_interfaces`
- **Description**: Get available network interfaces.

### `set_dhcp_config`
- **Description**: Set DHCP configuration.
- **Parameters**: `config` (dict)

### `find_active_dhcp`
- **Description**: Search for an active DHCP server on a specific interface.
- **Parameters**: `interface` (str)

### `add_dhcp_static_lease`
- **Description**: Add a static DHCP lease.
- **Parameters**: `mac` (str), `ip` (str), `hostname` (str)

### `remove_dhcp_static_lease`
- **Description**: Remove a static DHCP lease.
- **Parameters**: `mac` (str), `ip` (str), `hostname` (str)

### `update_dhcp_static_lease`
- **Description**: Update a static DHCP lease.
- **Parameters**: `mac` (str), `ip` (str), `hostname` (str)

### `reset_dhcp`
- **Description**: Reset DHCP configuration.

### `reset_dhcp_leases`
- **Description**: Reset all DHCP leases.
