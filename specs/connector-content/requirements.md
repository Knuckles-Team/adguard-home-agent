# CONN-ADGUARD-HOME-AGENT-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ADGUARD-HOME-AGENT-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `adguard-home-agent` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. Caller chain: pyproject scion_sdk.connector entry point adguard-home-agent -> adguard_home_agent/__init__.py::connector -> scion_sdk._connector_serve.build_server (L39), which serves the packaged skills, ontology and prompts (adguard_home_agent/skills, ontology, prompts). Shape: no code change; Connector(api, get_client, instructions) takes no content argument, so the SDK builds defaults with ConnectorContent.for_package; mirror the test in the container-manager-mcp repo's tests/test_default_content_surfaces.py using build_server and a FastMCP Client. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Planned test: `tests/test_default_content_surfaces.py::test_default_content_surfaces`. |
