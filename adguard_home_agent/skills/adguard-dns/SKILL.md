---
name: adguard-dns
description: Manage DNS settings in AdGuard Home.
---

# AdGuard Home DNS Agent

This agent is responsible for managing DNS settings in AdGuard Home.

## Capabilities

- **Get DNS Info**: Retrieve current DNS configuration.
- **Set DNS Config**: Update DNS configuration (upstream servers, bootstrap DNS, etc.).
- **Test Upstream DNS**: Test connectivity to upstream DNS servers.
- **Set Protection**: Enable or disable protection.
- **Clear Cache**: Clear the DNS cache.

## Tools

### `get_dns_info`
- **Description**: Get general DNS parameters.

### `set_dns_config`
- **Description**: Set general DNS parameters.
- **Parameters**: `config` (dict)

### `test_upstream_dns`
- **Description**: Test upstream configuration.
- **Parameters**: `upstreams` (list of str)

### `set_protection`
- **Description**: Set protection state.
- **Parameters**: `enabled` (bool), `duration` (int, optional)

### `clear_cache`
- **Description**: Clear DNS cache.
