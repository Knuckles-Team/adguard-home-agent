# Concepts

`adguard-home-agent` is a thin MCP shim over a complete AdGuard Home API client.

- `adguard_home_agent/api_client.py` wraps the AdGuard Home HTTP API.
- `adguard_home_agent/mcp_server.py` registers one typed tool per `Api` client operation (`adguard_home_<operation>`).
- `adguard_home_agent/mcp_server.py` builds the server with `scion_sdk` and gates each suite with a `<DOMAIN>TOOL` toggle.
- `connector_manifest.yml` is machine-generated from the ontology and source presets; never edit it by hand.

## Ecosystem bridge

**ECO-4.0** - this connector is built on `scion-sdk` (MCP server construction, manifests, content packs) and federates its ontology and skills into the hub through the `agent_utilities.*_providers` entry points. See the [agent-utilities concept registry](https://knuckles-team.github.io/agent-utilities/concepts/).
