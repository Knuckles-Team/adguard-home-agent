# Deployment

Build with `docker/Dockerfile`; `docker/mcp.compose.yml` runs the MCP server over streamable HTTP on port 8000 with a `/health` check, and `docker/agent.compose.yml` runs the A2A agent. Configuration comes from the environment (see Configuration).
