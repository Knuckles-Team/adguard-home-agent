---
name: adguard-rewrites
description: Manage DNS rewrites in AdGuard Home.
---

# AdGuard Home Rewrites Agent

This agent is responsible for managing DNS rewrites (custom DNS records).

## Capabilities

- **List Rewrites**: List all DNS rewrites.
- **Settings**: Get and update rewrite settings (enable/disable).
- **CRUD**: Add, update, and delete DNS rewrites.

## Tools

### `list_rewrites`
- **Description**: List DNS rewrites.

### `add_rewrite`
- **Description**: Add a DNS rewrite.
- **Parameters**: `domain` (str), `answer` (str)

### `update_rewrite`
- **Description**: Update a DNS rewrite.
- **Parameters**: `target` (dict), `update` (dict)

### `delete_rewrite`
- **Description**: Delete a DNS rewrite.
- **Parameters**: `domain` (str), `answer` (str)

### `get_rewrite_settings`
- **Description**: Get rewrite settings.

### `update_rewrite_settings`
- **Description**: Update rewrite settings.
- **Parameters**: `enabled` (bool)
