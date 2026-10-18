"""AdGuard Home MCP server entry point."""

from __future__ import annotations

import sys
from typing import Any

from agent_connector_sdk.config import load_config
from agent_connector_sdk.mcp.server import create_mcp_server
from agent_connector_sdk.mcp.tool_surface import register_tool_surface

from adguard_home_agent._version import __version__
from adguard_home_agent.api_client import Api
from adguard_home_agent.auth import get_client

__all__ = ["get_mcp_instance", "mcp_server"]

_INSTRUCTIONS = (
    "AdGuard Home MCP Server - one tool per API operation for DNS filtering, "
    "clients, DHCP, rewrites, query log, statistics and system settings."
)


def get_mcp_instance() -> tuple[Any, Any, list[Any]]:
    """Build the server: one typed tool per AdGuard Home API operation."""
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="adguard-home-agent",
        version=__version__,
        instructions=_INSTRUCTIONS,
    )
    register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="adguard-home-agent",
    )

    for middleware in middlewares:
        mcp.add_middleware(middleware)
    return mcp, args, middlewares


def mcp_server() -> None:
    """Run the server on the transport ``--transport`` selects."""
    mcp, args, _middlewares = get_mcp_instance()
    print(f"adguard-home-agent MCP v{__version__}", file=sys.stderr)
    if args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    mcp_server()
