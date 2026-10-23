# CONN-ADGUARD-HOME-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `adguard-home-agent` as the connector identity. `create_mcp_server` resolves the packaged content of `adguard_home_agent` from it.
