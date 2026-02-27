#!/usr/bin/env python
# coding: utf-8

import os
import sys
import logging
from typing import Optional, List, Dict, Union

import requests
from pydantic import Field
from eunomia_mcp.middleware import EunomiaMcpMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp import FastMCP
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.server.auth import OAuthProxy, RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier, StaticTokenVerifier
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.utilities.logging import get_logger
from agent_utilities.mcp_utilities import (
    create_mcp_parser,
    config,
)
from agent_utilities.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)
from adguard_home_agent.adguard_api import Api

__version__ = "0.2.18"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)


def register_prompts(mcp: FastMCP):
    @mcp.prompt()
    def review_filtering_rules() -> str:
        """Review current filtering rules and blacklists."""
        return "Please review the current filtering rules and blacklists to ensure optimal ad blocking and security."

    @mcp.prompt()
    def optimize_dns_settings() -> str:
        """Optimize DNS settings for performance and privacy."""
        return "Analyze the current DNS configuration and suggest optimizations for better performance and privacy."

    @mcp.prompt()
    def analyze_query_log() -> str:
        """Analyze query logs for suspicious activity."""
        return "Analyze the recent query logs to identify any suspicious domains or blocked requests that might indicate an issue."

    @mcp.prompt()
    def configure_parental_controls() -> str:
        """Configure parental control settings."""
        return "Help me configure parental controls to ensure a safe browsing environment for my family."

    @mcp.prompt()
    def manage_clients() -> str:
        """Manage connected clients and their specific settings."""
        return "I need to manage the connected clients, including assigning specific policies and identifying devices."

    @mcp.prompt()
    def add_dns_rewrite() -> str:
        """Add a new DNS rewrite rule."""
        return "I want to add a new DNS rewrite rule to redirect a domain to a specific IP address."

    @mcp.prompt()
    def update_dns_rewrite() -> str:
        """Update an existing DNS rewrite rule."""
        return "I need to update an existing DNS rewrite rule."

    @mcp.prompt()
    def delete_dns_rewrite() -> str:
        """Delete a DNS rewrite rule."""
        return "I want to remove a DNS rewrite rule that is no longer needed."


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(tags={"system"})
    async def get_version(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get AdGuard Home version."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_version()

    @mcp.tool(tags={"access"})
    async def get_access_list(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """List current access list (allowed/disallowed clients, blocked hosts)."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_access_list()

    @mcp.tool(tags={"access"})
    async def set_access_list(
        allowed_clients: Optional[List[str]] = Field(
            None, description="List of allowed clients"
        ),
        disallowed_clients: Optional[List[str]] = Field(
            None, description="List of disallowed clients"
        ),
        blocked_hosts: Optional[List[str]] = Field(
            None, description="List of blocked hosts"
        ),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set access list."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_access_list(
            allowed_clients=allowed_clients,
            disallowed_clients=disallowed_clients,
            blocked_hosts=blocked_hosts,
        )

    @mcp.tool(tags={"blocked-services"})
    async def get_blocked_services_list(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> List[Dict]:
        """List blocked services."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_blocked_services_list()

    @mcp.tool(tags={"blocked-services"})
    async def get_all_blocked_services(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get all available blocked services."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_all_blocked_services()

    @mcp.tool(tags={"blocked-services"})
    async def update_blocked_services(
        services: List[str] = Field(..., description="List of services to block"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Update blocked services list."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.update_blocked_services(services=services)

    @mcp.tool(tags={"filtering"})
    async def set_filtering_rules(
        rules: List[str] = Field(..., description="List of filtering rules"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set user-defined filtering rules."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_filtering_rules(rules=rules)

    @mcp.tool(tags={"filtering"})
    async def check_host_filtering(
        name: str = Field(..., description="Host name to check"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Check if a host is filtered."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.check_host_filtering(name=name)

    @mcp.tool(tags={"filtering"})
    async def set_filter_url_params(
        url: str = Field(..., description="URL of the filter"),
        name: str = Field(..., description="Name of the filter"),
        whitelist: bool = Field(False, description="Is it a whitelist?"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set filter URL parameters."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_filter_url_params(url=url, name=name, whitelist=whitelist)

    @mcp.tool(tags={"clients"})
    async def list_clients(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """List clients."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.list_clients()

    @mcp.tool(tags={"clients"})
    async def search_clients(
        query: str = Field(..., description="Query string (IP, name, or ClientID)"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> List[Dict]:
        """Search for clients."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.search_clients(query=query)

    @mcp.tool(tags={"profile"})
    async def get_profile(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get current user profile info."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_profile()

    @mcp.tool(tags={"profile"})
    async def update_profile(
        profile_data: Dict = Field(..., description="Profile data to update"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Update current user profile info."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.update_profile(profile_data=profile_data)

    @mcp.tool(tags={"clients"})
    async def add_client(
        name: str = Field(..., description="Name of the client"),
        ids: List[str] = Field(
            ..., description="List of identifiers (IP, CIDR, MAC, ClientID)"
        ),
        use_global_settings: bool = Field(True, description="Use global settings"),
        filtering_enabled: bool = Field(True, description="Enable filtering"),
        parent_access: bool = Field(False, description="Enable parental control"),
        safe_search_enabled: bool = Field(False, description="Enable safe search"),
        safe_browsing_enabled: bool = Field(False, description="Enable safe browsing"),
        tags: Optional[List[str]] = Field(None, description="Client tags"),
        upstreams: Optional[List[str]] = Field(
            None, description="Upstream DNS servers"
        ),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Add a new client."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.add_client(
            name=name,
            ids=ids,
            use_global_settings=use_global_settings,
            filtering_enabled=filtering_enabled,
            parent_access=parent_access,
            safe_search_enabled=safe_search_enabled,
            safe_browsing_enabled=safe_browsing_enabled,
            tags=tags,
            upstreams=upstreams,
        )

    @mcp.tool(tags={"clients"})
    async def update_client(
        name: str = Field(..., description="Name of the client"),
        data: Dict = Field(..., description="Client data to update"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Update a client."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.update_client(name=name, data=data)

    @mcp.tool(tags={"clients"})
    async def delete_client(
        name: str = Field(..., description="Name of the client"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Delete a client."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.delete_client(name=name)

    @mcp.tool(tags={"dhcp"})
    async def get_dhcp_status(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get DHCP status."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_dhcp_status()

    @mcp.tool(tags={"dhcp"})
    async def get_dhcp_interfaces(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get available network interfaces for DHCP."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_dhcp_interfaces()

    @mcp.tool(tags={"dhcp"})
    async def set_dhcp_config(
        config: Dict = Field(..., description="DHCP configuration"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set DHCP configuration."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_dhcp_config(config=config)

    @mcp.tool(tags={"dhcp"})
    async def find_active_dhcp(
        interface: str = Field(..., description="Network interface to check"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Search for an active DHCP server on the network."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.find_active_dhcp(interface=interface)

    @mcp.tool(tags={"dhcp"})
    async def add_dhcp_static_lease(
        mac: str = Field(..., description="MAC address"),
        ip: str = Field(..., description="IP address"),
        hostname: str = Field(..., description="Hostname"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Add a static DHCP lease."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.add_dhcp_static_lease(mac=mac, ip=ip, hostname=hostname)

    @mcp.tool(tags={"dhcp"})
    async def remove_dhcp_static_lease(
        mac: str = Field(..., description="MAC address"),
        ip: str = Field(..., description="IP address"),
        hostname: str = Field(..., description="Hostname"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Remove a static DHCP lease."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.remove_dhcp_static_lease(mac=mac, ip=ip, hostname=hostname)

    @mcp.tool(tags={"dhcp"})
    async def update_dhcp_static_lease(
        mac: str = Field(..., description="MAC address"),
        ip: str = Field(..., description="IP address"),
        hostname: str = Field(..., description="Hostname"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Update a static DHCP lease."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.update_dhcp_static_lease(mac=mac, ip=ip, hostname=hostname)

    @mcp.tool(tags={"dhcp"})
    async def reset_dhcp(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Reset DHCP configuration."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.reset_dhcp()

    @mcp.tool(tags={"dhcp"})
    async def reset_dhcp_leases(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Reset DHCP leases."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.reset_dhcp_leases()

    @mcp.tool(tags={"filtering"})
    async def get_filtering_status(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get filtering status."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_filtering_status()

    @mcp.tool(tags={"filtering"})
    async def set_filtering_config(
        enabled: bool = Field(..., description="Enable filtering"),
        interval: int = Field(..., description="Update interval in hours"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set filtering configuration."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_filtering_config(enabled=enabled, interval=interval)

    @mcp.tool(tags={"filtering"})
    async def add_filter_url(
        name: str = Field(..., description="Name of the filter"),
        url: str = Field(..., description="URL of the filter"),
        whitelist: bool = Field(False, description="Is it a whitelist?"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Add a filter URL."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.add_filter_url(name=name, url=url, whitelist=whitelist)

    @mcp.tool(tags={"filtering"})
    async def remove_filter_url(
        url: str = Field(..., description="URL of the filter to remove"),
        whitelist: bool = Field(False, description="Is it a whitelist?"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Remove a filter URL."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.remove_filter_url(url=url, whitelist=whitelist)

    @mcp.tool(tags={"filtering"})
    async def refresh_filters(
        whitelist: bool = Field(False, description="Refresh whitelists?"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Refresh all filters."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.refresh_filters(whitelist=whitelist)

    @mcp.tool(tags={"settings"})
    async def get_parental_status(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get parental control status."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_parental_status()

    @mcp.tool(tags={"settings"})
    async def enable_parental_control(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Enable parental control."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.enable_parental_control()

    @mcp.tool(tags={"settings"})
    async def disable_parental_control(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Disable parental control."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.disable_parental_control()

    @mcp.tool(tags={"settings"})
    async def get_safebrowsing_status(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get safe browsing status."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_safebrowsing_status()

    @mcp.tool(tags={"settings"})
    async def enable_safebrowsing(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Enable safe browsing."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.enable_safebrowsing()

    @mcp.tool(tags={"settings"})
    async def disable_safebrowsing(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Disable safe browsing."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.disable_safebrowsing()

    @mcp.tool(tags={"settings"})
    async def get_safesearch_status(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get safe search status."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_safesearch_status()

    @mcp.tool(tags={"query-log"})
    async def get_query_log(
        time_from_millis: int = Field(..., description="Start time in milliseconds"),
        time_to_millis: int = Field(..., description="End time in milliseconds"),
        limit: int = Field(20, description="Max number of logs to return"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get query log."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_query_log(
            time_from_millis=time_from_millis,
            time_to_millis=time_to_millis,
            limit=limit,
        )

    @mcp.tool(tags={"rewrites"})
    async def list_rewrites(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> List[Dict]:
        """List DNS rewrites."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.list_rewrites()

    @mcp.tool(tags={"rewrites"})
    async def add_rewrite(
        domain: str = Field(..., description="Domain to rewrite"),
        answer: str = Field(..., description="Answer to rewrite to"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Add a DNS rewrite."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.add_rewrite(domain=domain, answer=answer)

    @mcp.tool(tags={"rewrites"})
    async def delete_rewrite(
        domain: str = Field(..., description="Domain to rewrite"),
        answer: str = Field(..., description="Answer to rewrite to"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Delete a DNS rewrite."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.delete_rewrite(domain=domain, answer=answer)

    @mcp.tool(tags={"rewrites"})
    async def update_rewrite(
        target: Dict = Field(..., description="Target rewrite rule"),
        update: Dict = Field(..., description="Updated rewrite rule"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Update a DNS rewrite."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.update_rewrite(target=target, update=update)

    @mcp.tool(tags={"rewrites"})
    async def get_rewrite_settings(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get rewrite settings."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_rewrite_settings()

    @mcp.tool(tags={"rewrites"})
    async def update_rewrite_settings(
        enabled: bool = Field(..., description="Enable/disable rewrites"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Update rewrite settings."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.update_rewrite_settings(enabled=enabled)

    @mcp.tool(tags={"tls"})
    async def get_tls_status(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get TLS status."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_tls_status()

    @mcp.tool(tags={"tls"})
    async def configure_tls(
        config: Dict = Field(..., description="TLS configuration"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Configure TLS."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.configure_tls(config=config)

    @mcp.tool(tags={"tls"})
    async def validate_tls(
        config: Dict = Field(..., description="TLS configuration to validate"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Validate TLS configuration."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.validate_tls(config=config)

    @mcp.tool(tags={"mobile"})
    async def get_doh_mobile_config(
        host: str = Field(..., description="Host name"),
        client_id: str = Field(..., description="Client ID"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> str:
        """Get DNS over HTTPS .mobileconfig."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_doh_mobile_config(host=host, client_id=client_id)

    @mcp.tool(tags={"mobile"})
    async def get_dot_mobile_config(
        host: str = Field(..., description="Host name"),
        client_id: str = Field(..., description="Client ID"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> str:
        """Get DNS over TLS .mobileconfig."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_dot_mobile_config(host=host, client_id=client_id)

    @mcp.tool(tags={"stats"})
    async def get_stats(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get overall statistics."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_stats()

    @mcp.tool(tags={"dns"})
    async def get_dns_info(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get general DNS parameters."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_dns_info()

    @mcp.tool(tags={"dns"})
    async def set_dns_config(
        config: Dict = Field(..., description="DNS configuration"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set general DNS parameters."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_dns_config(config=config)

    @mcp.tool(tags={"system"})
    async def set_protection(
        enabled: bool = Field(..., description="Enable/disable protection"),
        duration: Optional[int] = Field(None, description="Duration in milliseconds"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set protection state."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_protection(enabled=enabled, duration=duration)

    @mcp.tool(tags={"system"})
    async def clear_cache(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Clear DNS cache."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.clear_cache()

    @mcp.tool(tags={"dns"})
    async def test_upstream_dns(
        upstreams: List[str] = Field(..., description="List of upstreams to test"),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Test upstream configuration."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.test_upstream_dns(upstreams=upstreams)

    @mcp.tool(tags={"stats"})
    async def reset_stats(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Reset statistics."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.reset_stats()

    @mcp.tool(tags={"stats"})
    async def get_stats_config(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Get statistics configuration."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_stats_config()

    @mcp.tool(tags={"stats"})
    async def set_stats_config(
        interval: int = Field(
            ..., description="Statistics retention interval in milliseconds"
        ),
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Set statistics configuration."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_stats_config(interval=interval)

    @mcp.tool(tags={"query-log"})
    async def clear_query_log(
        base_url: str = Field(
            default=os.environ.get("ADGUARD_URL", "http://localhost:3000"),
            description="The base URL of the AdGuard Home instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ADGUARD_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ADGUARD_PASSWORD", None),
            description="Password for authentication",
        ),
    ) -> Dict:
        """Clear query log."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.clear_query_log()


def mcp_server():
    print(f"Adguard Home MCP v{__version__}")
    parser = create_mcp_parser()

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        parser.print_help()

        sys.exit(0)

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    config["enable_delegation"] = args.enable_delegation
    config["audience"] = args.audience or config["audience"]
    config["delegated_scopes"] = args.delegated_scopes or config["delegated_scopes"]
    config["oidc_config_url"] = args.oidc_config_url or config["oidc_config_url"]
    config["oidc_client_id"] = args.oidc_client_id or config["oidc_client_id"]
    config["oidc_client_secret"] = (
        args.oidc_client_secret or config["oidc_client_secret"]
    )

    if config["enable_delegation"]:
        if args.auth_type != "oidc-proxy":
            logger.error("Token delegation requires auth-type=oidc-proxy")
            sys.exit(1)
        if not config["audience"]:
            logger.error("audience is required for delegation")
            sys.exit(1)
        if not all(
            [
                config["oidc_config_url"],
                config["oidc_client_id"],
                config["oidc_client_secret"],
            ]
        ):
            logger.error(
                "Delegation requires complete OIDC configuration (oidc-config-url, oidc-client-id, oidc-client-secret)"
            )
            sys.exit(1)

        try:
            logger.info(
                "Fetching OIDC configuration",
                extra={"oidc_config_url": config["oidc_config_url"]},
            )
            oidc_config_resp = requests.get(config["oidc_config_url"])
            oidc_config_resp.raise_for_status()
            oidc_config = oidc_config_resp.json()
            config["token_endpoint"] = oidc_config.get("token_endpoint")
            if not config["token_endpoint"]:
                logger.error("No token_endpoint found in OIDC configuration")
                raise ValueError("No token_endpoint found in OIDC configuration")
            logger.info(
                "OIDC configuration fetched successfully",
                extra={"token_endpoint": config["token_endpoint"]},
            )
        except Exception as e:
            print(f"Failed to fetch OIDC configuration: {e}")
            logger.error(
                "Failed to fetch OIDC configuration",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            sys.exit(1)

    auth = None
    allowed_uris = (
        args.allowed_client_redirect_uris.split(",")
        if args.allowed_client_redirect_uris
        else None
    )

    if args.auth_type == "none":
        auth = None
    elif args.auth_type == "static":
        auth = StaticTokenVerifier(
            tokens={
                "test-token": {"client_id": "test-user", "scopes": ["read", "write"]},
                "admin-token": {"client_id": "admin", "scopes": ["admin"]},
            }
        )
    elif args.auth_type == "jwt":
        jwks_uri = args.token_jwks_uri or os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI")
        issuer = args.token_issuer or os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER")
        audience = args.token_audience or os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE")
        algorithm = args.token_algorithm
        secret_or_key = args.token_secret or args.token_public_key
        public_key_pem = None

        if not (jwks_uri or secret_or_key):
            logger.error(
                "JWT auth requires either --token-jwks-uri or --token-secret/--token-public-key"
            )
            sys.exit(1)
        if not (issuer and audience):
            logger.error("JWT requires --token-issuer and --token-audience")
            sys.exit(1)

        if args.token_public_key and os.path.isfile(args.token_public_key):
            try:
                with open(args.token_public_key, "r") as f:
                    public_key_pem = f.read()
                logger.info(f"Loaded static public key from {args.token_public_key}")
            except Exception as e:
                print(f"Failed to read public key file: {e}")
                logger.error(f"Failed to read public key file: {e}")
                sys.exit(1)
        elif args.token_public_key:
            public_key_pem = args.token_public_key

        if jwks_uri and (algorithm or secret_or_key):
            logger.warning(
                "JWKS mode ignores --token-algorithm and --token-secret/--token-public-key"
            )

        if algorithm and algorithm.startswith("HS"):
            if not secret_or_key:
                logger.error(f"HMAC algorithm {algorithm} requires --token-secret")
                sys.exit(1)
            if jwks_uri:
                logger.error("Cannot use --token-jwks-uri with HMAC")
                sys.exit(1)
            public_key = secret_or_key
        else:
            public_key = public_key_pem

        required_scopes = None
        if args.required_scopes:
            required_scopes = [
                s.strip() for s in args.required_scopes.split(",") if s.strip()
            ]

        try:
            auth = JWTVerifier(
                jwks_uri=jwks_uri,
                public_key=public_key,
                issuer=issuer,
                audience=audience,
                algorithm=(
                    algorithm if algorithm and algorithm.startswith("HS") else None
                ),
                required_scopes=required_scopes,
            )
            logger.info(
                "JWTVerifier configured",
                extra={
                    "mode": (
                        "JWKS"
                        if jwks_uri
                        else (
                            "HMAC"
                            if algorithm and algorithm.startswith("HS")
                            else "Static Key"
                        )
                    ),
                    "algorithm": algorithm,
                    "required_scopes": required_scopes,
                },
            )
        except Exception as e:
            print(f"Failed to initialize JWTVerifier: {e}")
            logger.error(f"Failed to initialize JWTVerifier: {e}")
            sys.exit(1)
    elif args.auth_type == "oauth-proxy":
        if not (
            args.oauth_upstream_auth_endpoint
            and args.oauth_upstream_token_endpoint
            and args.oauth_upstream_client_id
            and args.oauth_upstream_client_secret
            and args.oauth_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            print(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience"
            )
            logger.error(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience",
                extra={
                    "auth_endpoint": args.oauth_upstream_auth_endpoint,
                    "token_endpoint": args.oauth_upstream_token_endpoint,
                    "client_id": args.oauth_upstream_client_id,
                    "base_url": args.oauth_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = OAuthProxy(
            upstream_authorization_endpoint=args.oauth_upstream_auth_endpoint,
            upstream_token_endpoint=args.oauth_upstream_token_endpoint,
            upstream_client_id=args.oauth_upstream_client_id,
            upstream_client_secret=args.oauth_upstream_client_secret,
            token_verifier=token_verifier,
            base_url=args.oauth_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "oidc-proxy":
        if not (
            args.oidc_config_url
            and args.oidc_client_id
            and args.oidc_client_secret
            and args.oidc_base_url
        ):
            logger.error(
                "oidc-proxy requires oidc-config-url, oidc-client-id, oidc-client-secret, oidc-base-url",
                extra={
                    "config_url": args.oidc_config_url,
                    "client_id": args.oidc_client_id,
                    "base_url": args.oidc_base_url,
                },
            )
            sys.exit(1)
        auth = OIDCProxy(
            config_url=args.oidc_config_url,
            client_id=args.oidc_client_id,
            client_secret=args.oidc_client_secret,
            base_url=args.oidc_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "remote-oauth":
        if not (
            args.remote_auth_servers
            and args.remote_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            logger.error(
                "remote-oauth requires remote-auth-servers, remote-base-url, token-jwks-uri, token-issuer, token-audience",
                extra={
                    "auth_servers": args.remote_auth_servers,
                    "base_url": args.remote_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        auth_servers = [url.strip() for url in args.remote_auth_servers.split(",")]
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=auth_servers,
            base_url=args.remote_base_url,
        )

    middlewares: List[
        Union[
            UserTokenMiddleware,
            ErrorHandlingMiddleware,
            RateLimitingMiddleware,
            TimingMiddleware,
            LoggingMiddleware,
            JWTClaimsLoggingMiddleware,
            EunomiaMcpMiddleware,
        ]
    ] = [
        ErrorHandlingMiddleware(include_traceback=True, transform_errors=True),
        RateLimitingMiddleware(max_requests_per_second=10.0, burst_capacity=20),
        TimingMiddleware(),
        LoggingMiddleware(),
        JWTClaimsLoggingMiddleware(),
    ]
    if config["enable_delegation"] or args.auth_type == "jwt":
        middlewares.insert(0, UserTokenMiddleware(config=config))

    if args.eunomia_type in ["embedded", "remote"]:
        try:
            from eunomia_mcp import create_eunomia_middleware

            policy_file = args.eunomia_policy_file or "mcp_policies.json"
            eunomia_endpoint = (
                args.eunomia_remote_url if args.eunomia_type == "remote" else None
            )
            eunomia_mw = create_eunomia_middleware(
                policy_file=policy_file, eunomia_endpoint=eunomia_endpoint
            )
            middlewares.append(eunomia_mw)
            logger.info(f"Eunomia middleware enabled ({args.eunomia_type})")
        except Exception as e:
            print(f"Failed to load Eunomia middleware: {e}")
            logger.error("Failed to load Eunomia middleware", extra={"error": str(e)})
            sys.exit(1)

    mcp = FastMCP("AdguardHome", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"AdguardHome Tower MCP v{__version__}")
    print("\nStarting AdguardHome Tower MCP Server")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Delegation: {'ON' if config['enable_delegation'] else 'OFF'}")
    print(f"  Eunomia: {args.eunomia_type}")

    mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    mcp_server()
