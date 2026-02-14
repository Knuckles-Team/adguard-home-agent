---
name: adguard-query-log
description: Manage and view query logs in AdGuard Home.
---

# AdGuard Home Query Log Agent

This agent is responsible for managing and viewing query logs.

## Capabilities

- **Get Query Log**: Retrieve query logs with filtering options.
- **Config**: Get and set query log configuration (retention, anonymization).
- **Clear**: Clear the query log.

## Tools

### `get_query_log`
- **Description**: Get query log.
- **Parameters**: `limit` (int), `older_than` (str), `response_status` (str), `search` (str)

### `get_query_log_config`
- **Description**: Get query log configuration.

### `set_query_log_config`
- **Description**: Set query log configuration.
- **Parameters**: `enabled` (bool), `interval` (int), `anonymize_client_ip` (bool)

### `clear_query_log`
- **Description**: Clear query log.
