---
name: adguard-stats
description: Manage and view statistics in AdGuard Home.
tags: [stats]
---

# AdGuard Home Stats Agent

This agent is responsible for managing and viewing statistics.

## Capabilities

- **Get Stats**: Retrieve overall statistics.
- **Config**: Get and set statistics configuration (retention interval).
- **Reset**: Reset all statistics.

## Tools

### `get_stats`
- **Description**: Get overall statistics.

### `get_stats_config`
- **Description**: Get statistics configuration.

### `set_stats_config`
- **Description**: Set statistics configuration.
- **Parameters**: `interval` (int)

### `reset_stats`
- **Description**: Reset all statistics.
