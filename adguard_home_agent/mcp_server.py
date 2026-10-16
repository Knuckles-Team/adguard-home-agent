"""AdGuard Home MCP server entry point."""

from __future__ import annotations

import sys
from typing import Any

from agent_connector_sdk.config import load_config, setting
from agent_connector_sdk.mcp.server import create_mcp_server

from adguard_home_agent._version import __version__
from adguard_home_agent.mcp import (
    register_system_tools,
    register_access_tools,
    register_blocked_services_tools,
    register_filtering_tools,
    register_clients_tools,
    register_profile_tools,
    register_dhcp_tools,
    register_settings_tools,
    register_query_log_tools,
    register_rewrites_tools,
    register_tls_tools,
    register_mobile_tools,
    register_stats_tools,
    register_dns_tools,
)

__all__ = ["get_mcp_instance", "mcp_server"]

_INSTRUCTIONS = (
    "AdGuard Home MCP Server - condensed action-routed tools for DNS filtering, "
    "clients, DHCP, rewrites, query log, statistics and system settings."
)


def get_mcp_instance() -> tuple[Any, Any, list[Any]]:
    """Build the server; each ``<DOMAIN>TOOL`` env toggle gates one tool suite."""
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="adguard-home-agent",
        version=__version__,
        instructions=_INSTRUCTIONS,
    )
    if setting("SYSTEMTOOL", True):
        register_system_tools(mcp)
    if setting("ACCESSTOOL", True):
        register_access_tools(mcp)
    if setting("BLOCKED_SERVICESTOOL", True):
        register_blocked_services_tools(mcp)
    if setting("FILTERINGTOOL", True):
        register_filtering_tools(mcp)
    if setting("CLIENTSTOOL", True):
        register_clients_tools(mcp)
    if setting("PROFILETOOL", True):
        register_profile_tools(mcp)
    if setting("DHCPTOOL", True):
        register_dhcp_tools(mcp)
    if setting("SETTINGSTOOL", True):
        register_settings_tools(mcp)
    if setting("QUERY_LOGTOOL", True):
        register_query_log_tools(mcp)
    if setting("REWRITESTOOL", True):
        register_rewrites_tools(mcp)
    if setting("TLSTOOL", True):
        register_tls_tools(mcp)
    if setting("MOBILETOOL", True):
        register_mobile_tools(mcp)
    if setting("STATSTOOL", True):
        register_stats_tools(mcp)
    if setting("DNSTOOL", True):
        register_dns_tools(mcp)

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
