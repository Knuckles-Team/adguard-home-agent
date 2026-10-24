# AGENTS.md

<!-- agent-contract:start -->
## Agent contract

Tool-neutral rules for any AI agent or human working in this repository. This block is maintained by the fleet standard; edit outside the markers.

- **Owner boundary:** this repository owns one external system's calls, mappings and MCP tools (spec prefix `CONN-ADGUARD-HOME-AGENT-`); it depends on the connector SDK only. Feature routing across repositories: [ecosystem boundaries](https://github.com/Knuckles-Team/pipelines/blob/main/reference/ecosystem-boundaries.md).
- **Setup:** run `uv sync --locked`, then `uvx pre-commit install --hook-type pre-commit --hook-type pre-push`.
- **Gates:** `uvx pre-commit run --all-files` must pass before you push. Do not bypass hooks to get green.
- **Commits:** one logical change per commit with a `Spec: <ID>` trailer (or `Spec: none (<reason>)`), plus a `Co-Authored-By:` trailer naming the assisting agent. Stage explicit paths only; never `git add -A` or `git add .`. Use your own configured Git identity, never a tool or bot name.
- **Org rules:** [organization AGENTS.md](https://github.com/Knuckles-Team/.github/blob/main/AGENTS.md).
<!-- agent-contract:end -->

## Tech Stack & Architecture
- Language/Version: Python 3.12+
- Core Libraries: `agent-connector-sdk` (MCP server construction, manifests, content packs), `agent-utilities` (A2A agent runtime), `fastmcp`, `pydantic`
- Key principles: the MCP layer is a thin shim over a complete API client; one typed tool per API client operation (SDK 0.3.0); no business logic, HTTP or auth in a tool body.

### Layout
```
adguard_home_agent/
  _version.py          single version source (bumpversion target)
  api_client.py        complete AdGuard Home API client
  auth.py              env-driven client factory (ADGUARD_URL, ADGUARD_USERNAME, ADGUARD_PASSWORD, ADGUARD_CA_BUNDLE; TLS via the SDK resolve_tls_profile)
  mcp_server.py        create_mcp_server + per-suite <DOMAIN>TOOL toggles
  mcp/mcp_<domain>.py  register_<domain>_tools(mcp): `action` enum + `params_json`
  connectors/          mcp_source_presets.json, tool_schema_fingerprints.json
  ontology/ prompts/ skills/   packs discovered via agent_utilities.*_providers entry points
connector_manifest.yml  machine-generated; never hand-edit
specs/                  spec-driven delivery (current state only)
```

### Regenerating generated artifacts
- Tool pins: `connector-certify . --write -- adguard-home-agent` after any tool signature change.
- `connector_manifest.yml`: `agent-utilities/scripts/generate_connector_manifests.py --connector-root .` (never edit by hand).

## Branching
Work on a topic branch in a real `git worktree`; never `git stash`, `git add -A` or `git add .`. A merge to `main` publishes to PyPI.

## Commands
```bash
uvx pre-commit run --all-files
uv run --frozen --no-sync pytest tests
```
