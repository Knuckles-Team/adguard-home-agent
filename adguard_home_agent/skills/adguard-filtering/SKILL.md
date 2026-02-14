---
name: adguard-filtering
description: Manage filtering settings in AdGuard Home.
---

# AdGuard Home Filtering Agent

This agent is responsible for managing filtering settings in AdGuard Home.

## Capabilities

- **Get Filtering Status**: GET current filtering status.
- **Set Filtering Config**: Enable/disable filtering and set update interval.
- **Set Filtering Rules**: Set user-defined custom filtering rules.
- **Check Host Filtering**: Check if a host is filtered.
- **Filter Lists**: Add, remove, and update filter lists (URLs).

## Tools

### `get_filtering_status`
- **Description**: Get filtering status.

### `set_filtering_config`
- **Description**: Set filtering configuration.
- **Parameters**: `enabled` (bool), `interval` (int)

### `set_filtering_rules`
- **Description**: Set user-defined filtering rules.
- **Parameters**: `rules` (list of str)

### `check_host_filtering`
- **Description**: Check if a host is filtered.
- **Parameters**: `name` (str)

### `set_filter_url_params`
- **Description**: Set parameters for a filter list URL.
- **Parameters**: `url` (str), `name` (str), `whitelist` (bool)

### `add_filter_url`
- **Description**: Add a new filter list.
- **Parameters**: `name` (str), `url` (str), `whitelist` (bool)

### `remove_filter_url`
- **Description**: Remove a filter list.
- **Parameters**: `url` (str), `whitelist` (bool)

### `refresh_filters`
- **Description**: Refresh all filter lists.
- **Parameters**: `whitelist` (bool)
