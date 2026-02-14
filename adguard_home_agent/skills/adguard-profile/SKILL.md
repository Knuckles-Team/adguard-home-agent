---
name: AdGuard Home Profile Agent
description: Manage the current user profile in AdGuard Home.
---

# AdGuard Home Profile Agent

This agent is responsible for managing the current user profile in AdGuard Home.

## Capabilities

- **Get Profile**: Retrieve current user information.
- **Update Profile**: Update current user information (name, password, etc.).

## Tools

### `get_profile`
- **Description**: Get current user profile info.
- **Parameters**: None (uses default connection settings).

### `update_profile`
- **Description**: Update current user profile info.
- **Parameters**:
    - `profile_data` (dict): Profile data to update (e.g., `{"name": "newname", "password": "newpassword"}`).
