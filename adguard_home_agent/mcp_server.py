#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from adguard_home_agent.auth import get_client

__version__ = "0.15.0"

logger = get_logger(name="adguard-home-agent")
logger.setLevel(logging.INFO)


def register_system_tools(mcp: FastMCP):
    @mcp.tool(tags={"system"})
    async def adguard_home_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_version', 'set_protection', 'clear_cache'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home system operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_version":
            return client.get_version(**kwargs)
        if action == "set_protection":
            return client.set_protection(**kwargs)
        if action == "clear_cache":
            return client.clear_cache(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_access_tools(mcp: FastMCP):
    @mcp.tool(tags={"access"})
    async def adguard_home_access(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_access_list', 'set_access_list'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home access operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_access_list":
            return client.get_access_list(**kwargs)
        if action == "set_access_list":
            return client.set_access_list(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_blocked_services_tools(mcp: FastMCP):
    @mcp.tool(tags={"blocked-services"})
    async def adguard_home_blocked_services(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_blocked_services_list', 'get_all_blocked_services', 'update_blocked_services'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home blocked services operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_blocked_services_list":
            return client.get_blocked_services_list(**kwargs)
        if action == "get_all_blocked_services":
            return client.get_all_blocked_services(**kwargs)
        if action == "update_blocked_services":
            return client.update_blocked_services(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_filtering_tools(mcp: FastMCP):
    @mcp.tool(tags={"filtering"})
    async def adguard_home_filtering(
        action: str = Field(
            description="Action to perform. Must be one of: 'set_filtering_rules', 'check_host_filtering', 'set_filter_url_params', 'get_filtering_status', 'set_filtering_config', 'add_filter_url', 'remove_filter_url', 'refresh_filters'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home filtering operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "set_filtering_rules":
            return client.set_filtering_rules(**kwargs)
        if action == "check_host_filtering":
            return client.check_host_filtering(**kwargs)
        if action == "set_filter_url_params":
            return client.set_filter_url_params(**kwargs)
        if action == "get_filtering_status":
            return client.get_filtering_status(**kwargs)
        if action == "set_filtering_config":
            return client.set_filtering_config(**kwargs)
        if action == "add_filter_url":
            return client.add_filter_url(**kwargs)
        if action == "remove_filter_url":
            return client.remove_filter_url(**kwargs)
        if action == "refresh_filters":
            return client.refresh_filters(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_clients_tools(mcp: FastMCP):
    @mcp.tool(tags={"clients"})
    async def adguard_home_clients(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_clients', 'search_clients', 'add_client', 'update_client', 'delete_client'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home clients operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_clients":
            return client.list_clients(**kwargs)
        if action == "search_clients":
            return client.search_clients(**kwargs)
        if action == "add_client":
            return client.add_client(**kwargs)
        if action == "update_client":
            return client.update_client(**kwargs)
        if action == "delete_client":
            return client.delete_client(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_profile_tools(mcp: FastMCP):
    @mcp.tool(tags={"profile"})
    async def adguard_home_profile(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_profile', 'update_profile'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home profile operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_profile":
            return client.get_profile(**kwargs)
        if action == "update_profile":
            return client.update_profile(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_dhcp_tools(mcp: FastMCP):
    @mcp.tool(tags={"dhcp"})
    async def adguard_home_dhcp(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_dhcp_status', 'get_dhcp_interfaces', 'set_dhcp_config', 'find_active_dhcp', 'add_dhcp_static_lease', 'remove_dhcp_static_lease', 'update_dhcp_static_lease', 'reset_dhcp', 'reset_dhcp_leases'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home dhcp operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_dhcp_status":
            return client.get_dhcp_status(**kwargs)
        if action == "get_dhcp_interfaces":
            return client.get_dhcp_interfaces(**kwargs)
        if action == "set_dhcp_config":
            return client.set_dhcp_config(**kwargs)
        if action == "find_active_dhcp":
            return client.find_active_dhcp(**kwargs)
        if action == "add_dhcp_static_lease":
            return client.add_dhcp_static_lease(**kwargs)
        if action == "remove_dhcp_static_lease":
            return client.remove_dhcp_static_lease(**kwargs)
        if action == "update_dhcp_static_lease":
            return client.update_dhcp_static_lease(**kwargs)
        if action == "reset_dhcp":
            return client.reset_dhcp(**kwargs)
        if action == "reset_dhcp_leases":
            return client.reset_dhcp_leases(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_settings_tools(mcp: FastMCP):
    @mcp.tool(tags={"settings"})
    async def adguard_home_settings(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_parental_status', 'enable_parental_control', 'disable_parental_control', 'get_safebrowsing_status', 'enable_safebrowsing', 'disable_safebrowsing', 'get_safesearch_status'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home settings operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_parental_status":
            return client.get_parental_status(**kwargs)
        if action == "enable_parental_control":
            return client.enable_parental_control(**kwargs)
        if action == "disable_parental_control":
            return client.disable_parental_control(**kwargs)
        if action == "get_safebrowsing_status":
            return client.get_safebrowsing_status(**kwargs)
        if action == "enable_safebrowsing":
            return client.enable_safebrowsing(**kwargs)
        if action == "disable_safebrowsing":
            return client.disable_safebrowsing(**kwargs)
        if action == "get_safesearch_status":
            return client.get_safesearch_status(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_query_log_tools(mcp: FastMCP):
    @mcp.tool(tags={"query-log"})
    async def adguard_home_query_log(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_query_log', 'clear_query_log'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home query log operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_query_log":
            return client.get_query_log(**kwargs)
        if action == "clear_query_log":
            return client.clear_query_log(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_rewrites_tools(mcp: FastMCP):
    @mcp.tool(tags={"rewrites"})
    async def adguard_home_rewrites(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_rewrites', 'add_rewrite', 'delete_rewrite', 'update_rewrite', 'get_rewrite_settings', 'update_rewrite_settings'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home rewrites operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_rewrites":
            return client.list_rewrites(**kwargs)
        if action == "add_rewrite":
            return client.add_rewrite(**kwargs)
        if action == "delete_rewrite":
            return client.delete_rewrite(**kwargs)
        if action == "update_rewrite":
            return client.update_rewrite(**kwargs)
        if action == "get_rewrite_settings":
            return client.get_rewrite_settings(**kwargs)
        if action == "update_rewrite_settings":
            return client.update_rewrite_settings(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_tls_tools(mcp: FastMCP):
    @mcp.tool(tags={"tls"})
    async def adguard_home_tls(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_tls_status', 'configure_tls', 'validate_tls'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home tls operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_tls_status":
            return client.get_tls_status(**kwargs)
        if action == "configure_tls":
            return client.configure_tls(**kwargs)
        if action == "validate_tls":
            return client.validate_tls(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_mobile_tools(mcp: FastMCP):
    @mcp.tool(tags={"mobile"})
    async def adguard_home_mobile(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_doh_mobile_config', 'get_dot_mobile_config'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home mobile operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_doh_mobile_config":
            return client.get_doh_mobile_config(**kwargs)
        if action == "get_dot_mobile_config":
            return client.get_dot_mobile_config(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_stats_tools(mcp: FastMCP):
    @mcp.tool(tags={"stats"})
    async def adguard_home_stats(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_stats', 'reset_stats', 'get_stats_config', 'set_stats_config'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home stats operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_stats":
            return client.get_stats(**kwargs)
        if action == "reset_stats":
            return client.reset_stats(**kwargs)
        if action == "get_stats_config":
            return client.get_stats_config(**kwargs)
        if action == "set_stats_config":
            return client.set_stats_config(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_dns_tools(mcp: FastMCP):
    @mcp.tool(tags={"dns"})
    async def adguard_home_dns(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_dns_info', 'set_dns_config', 'test_upstream_dns'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage adguard home dns operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_dns_info":
            return client.get_dns_info(**kwargs)
        if action == "set_dns_config":
            return client.set_dns_config(**kwargs)
        if action == "test_upstream_dns":
            return client.test_upstream_dns(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="adguard-home-agent MCP",
        version=__version__,
        instructions="adguard-home-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_SYSTEMTOOL = to_boolean(os.getenv("SYSTEMTOOL", "True"))
    if DEFAULT_SYSTEMTOOL:
        register_system_tools(mcp)
    DEFAULT_ACCESSTOOL = to_boolean(os.getenv("ACCESSTOOL", "True"))
    if DEFAULT_ACCESSTOOL:
        register_access_tools(mcp)
    DEFAULT_BLOCKED_SERVICESTOOL = to_boolean(os.getenv("BLOCKED_SERVICESTOOL", "True"))
    if DEFAULT_BLOCKED_SERVICESTOOL:
        register_blocked_services_tools(mcp)
    DEFAULT_FILTERINGTOOL = to_boolean(os.getenv("FILTERINGTOOL", "True"))
    if DEFAULT_FILTERINGTOOL:
        register_filtering_tools(mcp)
    DEFAULT_CLIENTSTOOL = to_boolean(os.getenv("CLIENTSTOOL", "True"))
    if DEFAULT_CLIENTSTOOL:
        register_clients_tools(mcp)
    DEFAULT_PROFILETOOL = to_boolean(os.getenv("PROFILETOOL", "True"))
    if DEFAULT_PROFILETOOL:
        register_profile_tools(mcp)
    DEFAULT_DHCPTOOL = to_boolean(os.getenv("DHCPTOOL", "True"))
    if DEFAULT_DHCPTOOL:
        register_dhcp_tools(mcp)
    DEFAULT_SETTINGSTOOL = to_boolean(os.getenv("SETTINGSTOOL", "True"))
    if DEFAULT_SETTINGSTOOL:
        register_settings_tools(mcp)
    DEFAULT_QUERY_LOGTOOL = to_boolean(os.getenv("QUERY_LOGTOOL", "True"))
    if DEFAULT_QUERY_LOGTOOL:
        register_query_log_tools(mcp)
    DEFAULT_REWRITESTOOL = to_boolean(os.getenv("REWRITESTOOL", "True"))
    if DEFAULT_REWRITESTOOL:
        register_rewrites_tools(mcp)
    DEFAULT_TLSTOOL = to_boolean(os.getenv("TLSTOOL", "True"))
    if DEFAULT_TLSTOOL:
        register_tls_tools(mcp)
    DEFAULT_MOBILETOOL = to_boolean(os.getenv("MOBILETOOL", "True"))
    if DEFAULT_MOBILETOOL:
        register_mobile_tools(mcp)
    DEFAULT_STATSTOOL = to_boolean(os.getenv("STATSTOOL", "True"))
    if DEFAULT_STATSTOOL:
        register_stats_tools(mcp)
    DEFAULT_DNSTOOL = to_boolean(os.getenv("DNSTOOL", "True"))
    if DEFAULT_DNSTOOL:
        register_dns_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"adguard-home-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
