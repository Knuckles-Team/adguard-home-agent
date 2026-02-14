---
name: adguard-clients
description: Manage clients in AdGuard Home.
---

# AdGuard Home Clients Agent

This agent is responsible for managing clients in AdGuard Home.

## Capabilities

- **List Clients**: List all configured clients.
- **Search Clients**: Search for clients by IP, name, or ClientID.
- **CRUD**: Add, update, and delete clients.

## Tools

### `list_clients`
- **Description**: List all clients.

### `search_clients`
- **Description**: Search for clients.
- **Parameters**: `query` (str)

### `add_client`
- **Description**: Add a new client.
- **Parameters**: `name` (str), `ids` (list of str), various settings...

### `update_client`
- **Description**: Update a client.
- **Parameters**: `name` (str), `data` (dict)

### `delete_client`
- **Description**: Delete a client.
- **Parameters**: `name` (str)
