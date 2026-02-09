# AdGuard Home Agent - A2A | AG-UI | MCP | API

![PyPI - Version](https://img.shields.io/pypi/v/adguard-home-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/adguard-home-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/adguard-home-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/adguard-home-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/adguard-home-agent)
![PyPI - License](https://img.shields.io/pypi/l/adguard-home-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/adguard-home-agent)


![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/adguard-home-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/adguard-home-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/adguard-home-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/adguard-home-agent)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/adguard-home-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/adguard-home-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/adguard-home-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/adguard-home-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/adguard-home-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/adguard-home-agent)

*Version: 0.1.1*

## Overview

The **AdGuard Home MCP Server** provides a Model Context Protocol (MCP) interface to interact with the AdGuard Home API, enabling automation and management of AdGuard Home resources such as devices, DNS servers, filter lists, query logs, and statistics. This server is designed to integrate seamlessly with AI-driven workflows and can be deployed as a standalone service or used programmatically.

### Features

- **Comprehensive API Coverage**: Manage AdGuard Home resources including devices, DNS servers, filter lists, query logs, and statistics.
- **MCP Integration**: Exposes AdGuard Home API functionalities as MCP tools for use with AI agents or direct API calls.
- **Authentication**: Supports Basic Authentication.
- **Environment Variable Support**: Securely configure credentials and settings via environment variables.
- **Docker Support**: Easily deployable as a Docker container for scalable environments.
- **Extensive Documentation**: Clear examples and instructions for setup, usage, and testing.

## MCP

### MCP Tools

The `adguard-home-agent` package exposes the following MCP tools, organized by category:

### Account Management
- `get_account_limits()`: Get account limits.

### Device Management
- `list_devices()`: List all devices.
- `create_device(name, device_type, dns_server_id)`: Create a new device.
- `get_device(device_id)`: Get details of a specific device.
- `update_device(device_id, name, device_type, dns_server_id)`: Update an existing device.
- `delete_device(device_id)`: Delete a device.

### DNS Server Management
- `list_dns_servers()`: List all DNS servers.

### Filtering
- `list_filter_lists()`: List all filter lists.

### Statistics
- `get_stats_categories(time_from_millis, time_to_millis)`: Get category statistics.

### Query Log
- `get_query_log(time_from_millis, time_to_millis, limit)`: Get query log.

## A2A Agent

### Architecture:

```mermaid
---
config:
  layout: dagre
---
flowchart TB
 subgraph subGraph0["Agent Capabilities"]
        C["Agent"]
        B["A2A Server - Uvicorn/FastAPI"]
        D["MCP Tools"]
        F["Agent Skills"]
  end
    C --> D & F
    A["User Query"] --> B
    B --> C
    D --> E["Platform API"]

     C:::agent
     B:::server
     A:::server
    classDef server fill:#f9f,stroke:#333
    classDef agent fill:#bbf,stroke:#333,stroke-width:2px
    style B stroke:#000000,fill:#FFD600
    style D stroke:#000000,fill:#BBDEFB
    style F fill:#BBDEFB
    style A fill:#C8E6C9
    style subGraph0 fill:#FFF9C4
```

### Component Interaction Diagram

```mermaid
sequenceDiagram
    participant User
    participant Server as A2A Server
    participant Agent as Agent
    participant Skill as Agent Skills
    participant MCP as MCP Tools

    User->>Server: Send Query
    Server->>Agent: Invoke Agent
    Agent->>Skill: Analyze Skills Available
    Skill->>Agent: Provide Guidance on Next Steps
    Agent->>MCP: Invoke Tool
    MCP-->>Agent: Tool Response Returned
    Agent-->>Agent: Return Results Summarized
    Agent-->>Server: Final Response
    Server-->>User: Output
```

## Usage

### MCP CLI

| Short Flag | Long Flag                          | Description                                                                 |
|------------|------------------------------------|-----------------------------------------------------------------------------|
| -h         | --help                             | Display help information                                                    |
|            | --auth-type                        | Authentication type (default: none)                                         |

### A2A CLI
#### Endpoints
- **Web UI**: `http://localhost:8000/` (if enabled)
- **A2A**: `http://localhost:8000/a2a` (Discovery: `/a2a/.well-known/agent.json`)
- **AG-UI**: `http://localhost:8000/ag-ui` (POST)

| Long Flag        | Description                                      | Default                     |
|------------------|--------------------------------------------------|-----------------------------|
| --host           | Host to bind the server to                       | 0.0.0.0                     |
| --port           | Port to bind the server to                       | 9000                        |
| --reload         | Enable auto-reload                               | False                       |
| --provider       | LLM Provider (openai, anthropic, google, etc)    | openai                      |
| --model-id       | LLM Model ID                                     | qwen/qwen3-4b-2507               |
| --base-url       | LLM Base URL (for OpenAI compatible providers)   | http://host.docker.internal:1234/v1    |
| --api-key        | LLM API Key                                      | ollama                      |
| --mcp-url        | MCP Server URL to connect to                     | None                        |
| --mcp-config     | MCP Server Config                                | .../mcp_config.json         |
| --skills-directory| Directory containing agent skills               | ...                         |
| --web            | Enable Pydantic AI Web UI                        | False (Env: ENABLE_WEB_UI)  |

### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access). To start the server, use the following commands:

#### Run in stdio mode (default):
```bash
adguard-home-mcp
```

#### Run in HTTP mode:
```bash
adguard-home-mcp --transport http --host 0.0.0.0 --port 8012
```

Set environment variables for authentication:
```bash
export ADGUARD_URL="http://adguard-home:3000"
export ADGUARD_USERNAME="your-username"
export ADGUARD_PASSWORD="your-password"
```

### Use API Directly

You can interact with the AdGuard Home API directly using the `Api` class from `adguard_api.py`. Below is an example of creating a device:

```python
from adguard_home_agent.adguard_api import Api

# Initialize the API client
client = Api(
    base_url="http://adguard-home:3000",
    username="your-username",
    password="your-password"
)

# Create a device
device = client.create_device(
    name="Test Device",
    device_type="mobile",
    dns_server_id="123"
)
print(device)
```

### Deploy MCP Server as a Service

The AdGuard Home MCP server can be deployed using Docker.

#### Using Docker Run

```bash
docker pull knucklessg1/adguard-home-mcp:latest

docker run -d \
  --name adguard-home-mcp \
  -p 8012:8012 \
  -e HOST=0.0.0.0 \
  -e PORT=8012 \
  -e TRANSPORT=http \
  -e ADGUARD_URL=http://adguard-home:3000 \
  -e ADGUARD_USERNAME=your-username \
  -e ADGUARD_PASSWORD=your-password \
  knucklessg1/adguard-home-mcp:latest
```

#### Using Docker Compose

Create a `compose.yml` file:

```yaml
services:
  adguard-home-mcp:
    image: knucklessg1/adguard-home-mcp:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8012
      - TRANSPORT=http
      - ADGUARD_URL=${ADGUARD_URL}
      - ADGUARD_USERNAME=${ADGUARD_USERNAME}
      - ADGUARD_PASSWORD=${ADGUARD_PASSWORD}
    ports:
      - "8012:8012"
```

Run the service:

```bash
docker-compose up -d
```

## Install Python Package

Install the `adguard-home-agent` package using pip:

```bash
python -m pip install adguard-home-agent[all]
```

### Dependencies

Ensure the following Python packages are installed:
- `requests`
- `fastmcp`
- `pydantic`

Install dependencies manually if needed:
```bash
python -m pip install requests fastmcp pydantic
```

## Tests

### Pre-commit Checks

Run pre-commit checks to ensure code quality and formatting:
```bash
pre-commit run --all-files
```

To set up pre-commit hooks:
```bash
pre-commit install
```

### Validate MCP Server

Validate the MCP server configuration and tools using the MCP inspector:
```bash
npx @modelcontextprotocol/inspector adguard-home-mcp
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code passes pre-commit checks and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/Knuckles-Team/adguard-home-agent). For general inquiries, contact the maintainers via GitHub.

### Documentation

https://github.com/AdguardTeam/AdGuardHome/blob/master/openapi/openapi.yaml
