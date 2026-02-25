---
name: adguard-blocked-services
description: Manage blocked services in AdGuard Home.
tags: [blocked-services]
---

# AdGuard Home Blocked Services Agent

This agent is responsible for managing blocked services (e.g., YouTube, Facebook).

## Capabilities

- **List Services**: Get a list of all available services and currently blocked services.
- **Update Services**: Update the list of blocked services.

## Tools

### `get_all_blocked_services`
- **Description**: Get all available services that can be blocked.

### `get_blocked_services_list`
- **Description**: Get the list of currently blocked services.

### `update_blocked_services`
- **Description**: Update the list of blocked services.
- **Parameters**: `services` (list of str)
