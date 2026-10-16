# AGENTS.md

## Tech Stack & Architecture
- Language/Version: Python 3.12+
- Core Libraries: `agent-connector-sdk` (MCP server construction, manifests, content packs), `agent-utilities` (A2A agent runtime), `fastmcp`, `pydantic`
- Key principles: the MCP layer is a thin shim over a complete API client; one action-routed tool per domain tag; no business logic, HTTP or auth in a tool body.

### Layout
```
adguard_home_agent/
  _version.py          single version source (bumpversion target)
  api_client.py        complete AdGuard Home API client
  auth.py              env-driven client factory (ADGUARD_URL, ADGUARD_USERNAME, ADGUARD_PASSWORD, ADGUARD_SSL_VERIFY)
  mcp_server.py        create_mcp_server + per-suite <DOMAIN>TOOL toggles
  mcp/mcp_<domain>.py  register_<domain>_tools(mcp): `action` enum + `params_json`
  agent_server.py      A2A agent entry point
  connectors/          mcp_source_presets.json, tool_schema_fingerprints.json
  ontology/ prompts/ skills/   packs discovered via agent_utilities.*_providers entry points
connector_manifest.yml  machine-generated; never hand-edit
specs/                  spec-driven delivery (current state only)
```

### Regenerating generated artifacts
- Tool fingerprints: `python scripts/compute_tool_fingerprints.py --apply` after any tool signature change.
- `connector_manifest.yml`: `agent-utilities/scripts/generate_connector_manifests.py --connector-root .` (never edit by hand).

## Branching
Work on a topic branch in a real `git worktree`; never `git stash`, `git add -A` or `git add .`. A merge to `main` publishes to PyPI.

## Commands
```bash
uvx pre-commit run --all-files
uv run --frozen --no-sync pytest tests
```
