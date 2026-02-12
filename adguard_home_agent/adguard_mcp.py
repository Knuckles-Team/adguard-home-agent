#!/usr/bin/env python
# coding: utf-8

import os
import argparse
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
from adguard_home_agent.adguard_api import Api
from adguard_home_agent.utils import to_boolean, to_integer
from adguard_home_agent.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.2.7"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)

config = {
    "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
    "audience": os.environ.get("AUDIENCE", None),
    "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
    "token_endpoint": None,
    "oidc_client_id": os.environ.get("OIDC_CLIENT_ID", None),
    "oidc_client_secret": os.environ.get("OIDC_CLIENT_SECRET", None),
    "oidc_config_url": os.environ.get("OIDC_CONFIG_URL", None),
    "jwt_jwks_uri": os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI", None),
    "jwt_issuer": os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER", None),
    "jwt_audience": os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE", None),
    "jwt_algorithm": os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM", None),
    "jwt_secret": os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY", None),
    "jwt_required_scopes": os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES", None),
}

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "8000"))


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

    @mcp.tool(tags=["account"])
    async def get_account_limits(
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
        """Get account limits."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_account_limits()

    @mcp.tool(tags=["system"])
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

    @mcp.tool(tags=["access"])
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

    @mcp.tool(tags=["access"])
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

    @mcp.tool(tags=["blocked_services"])
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

    @mcp.tool(tags=["blocked_services"])
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

    @mcp.tool(tags=["blocked_services"])
    async def set_blocked_services(
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
        """Set blocked services."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.set_blocked_services(services=services)

    @mcp.tool(tags=["clients"])
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

    @mcp.tool(tags=["clients"])
    async def find_clients(
        ip: str = Field(..., description="IP address to search for"),
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
        """Find clients by IP."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.find_clients(ip=ip)

    @mcp.tool(tags=["clients"])
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

    @mcp.tool(tags=["clients"])
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

    @mcp.tool(tags=["clients"])
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

    @mcp.tool(tags=["dhcp"])
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

    @mcp.tool(tags=["filtering"])
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

    @mcp.tool(tags=["filtering"])
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

    @mcp.tool(tags=["filtering"])
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

    @mcp.tool(tags=["filtering"])
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

    @mcp.tool(tags=["filtering"])
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

    @mcp.tool(tags=["filtering"])
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

    @mcp.tool(tags=["settings"])
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

    @mcp.tool(tags=["settings"])
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

    @mcp.tool(tags=["settings"])
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

    @mcp.tool(tags=["settings"])
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

    @mcp.tool(tags=["settings"])
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

    @mcp.tool(tags=["settings"])
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

    @mcp.tool(tags=["settings"])
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

    @mcp.tool(tags=["query_log"])
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

    @mcp.tool(tags=["rewrites"])
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

    @mcp.tool(tags=["rewrites"])
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

    @mcp.tool(tags=["rewrites"])
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

    @mcp.tool(tags=["stats"])
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

    @mcp.tool(tags=["devices"])
    async def list_devices(
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
        """List all devices."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.list_devices()

    @mcp.tool(tags=["devices"])
    async def create_device(
        name: str = Field(..., description="Name of the device"),
        device_type: str = Field(..., description="Type of the device"),
        dns_server_id: str = Field(..., description="ID of the DNS server to assign"),
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
        """Create a new device."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.create_device(
            name=name, device_type=device_type, dns_server_id=dns_server_id
        )

    @mcp.tool(tags=["devices"])
    async def get_device(
        device_id: str = Field(..., description="ID of the device"),
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
        """Get a device by ID."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_device(device_id=device_id)

    @mcp.tool(tags=["devices"])
    async def update_device(
        device_id: str = Field(..., description="ID of the device"),
        name: Optional[str] = Field(None, description="New name of the device"),
        device_type: Optional[str] = Field(None, description="New type of the device"),
        dns_server_id: Optional[str] = Field(
            None, description="New DNS server ID to assign"
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
        """Update a device."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.update_device(
            device_id=device_id,
            name=name,
            device_type=device_type,
            dns_server_id=dns_server_id,
        )

    @mcp.tool(tags=["devices"])
    async def delete_device(
        device_id: str = Field(..., description="ID of the device"),
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
        """Delete a device."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.delete_device(device_id=device_id)

    @mcp.tool(tags=["dns"])
    async def list_dns_servers(
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
        """List all DNS servers."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.list_dns_servers()

    @mcp.tool(tags=["filtering"])
    async def list_filter_lists(
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
        """List all filter lists."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.list_filter_lists()

    @mcp.tool(tags=["stats"])
    async def get_stats_categories(
        time_from_millis: int = Field(..., description="Start time in milliseconds"),
        time_to_millis: int = Field(..., description="End time in milliseconds"),
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
        """Get category statistics."""
        client = Api(base_url=base_url, username=username, password=password)
        return client.get_stats_categories(
            time_from_millis=time_from_millis, time_to_millis=time_to_millis
        )


def adguard_home_mcp():
    print(f"Adguard Home MCP v{__version__}")
    parser = argparse.ArgumentParser(add_help=False, description="Adguard Home MCP")

    parser.add_argument(
        "-t",
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "streamable-http", "sse"],
        help="Transport method: 'stdio', 'streamable-http', or 'sse' [legacy] (default: stdio)",
    )
    parser.add_argument(
        "-s",
        "--host",
        default=DEFAULT_HOST,
        help="Host address for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port number for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--auth-type",
        default="none",
        choices=["none", "static", "jwt", "oauth-proxy", "oidc-proxy", "remote-oauth"],
        help="Authentication type for MCP server: 'none' (disabled), 'static' (internal), 'jwt' (external token verification), 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (external) (default: none)",
    )
    parser.add_argument(
        "--token-jwks-uri", default=None, help="JWKS URI for JWT verification"
    )
    parser.add_argument(
        "--token-issuer", default=None, help="Issuer for JWT verification"
    )
    parser.add_argument(
        "--token-audience", default=None, help="Audience for JWT verification"
    )
    parser.add_argument(
        "--token-algorithm",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM"),
        choices=[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
        ],
        help="JWT signing algorithm (required for HMAC or static key). Auto-detected for JWKS.",
    )
    parser.add_argument(
        "--token-secret",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Shared secret for HMAC (HS*) or PEM public key for static asymmetric verification.",
    )
    parser.add_argument(
        "--token-public-key",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Path to PEM public key file or inline PEM string (for static asymmetric keys).",
    )
    parser.add_argument(
        "--required-scopes",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES"),
        help="Comma-separated list of required scopes (e.g., adguard.read,adguard.write).",
    )
    parser.add_argument(
        "--oauth-upstream-auth-endpoint",
        default=None,
        help="Upstream authorization endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-token-endpoint",
        default=None,
        help="Upstream token endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-id",
        default=None,
        help="Upstream client ID for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-secret",
        default=None,
        help="Upstream client secret for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-base-url", default=None, help="Base URL for OAuth Proxy"
    )
    parser.add_argument(
        "--oidc-config-url", default=None, help="OIDC configuration URL"
    )
    parser.add_argument("--oidc-client-id", default=None, help="OIDC client ID")
    parser.add_argument("--oidc-client-secret", default=None, help="OIDC client secret")
    parser.add_argument("--oidc-base-url", default=None, help="Base URL for OIDC Proxy")
    parser.add_argument(
        "--remote-auth-servers",
        default=None,
        help="Comma-separated list of authorization servers for Remote OAuth",
    )
    parser.add_argument(
        "--remote-base-url", default=None, help="Base URL for Remote OAuth"
    )
    parser.add_argument(
        "--allowed-client-redirect-uris",
        default=None,
        help="Comma-separated list of allowed client redirect URIs",
    )
    parser.add_argument(
        "--eunomia-type",
        default="none",
        choices=["none", "embedded", "remote"],
        help="Eunomia authorization type: 'none' (disabled), 'embedded' (built-in), 'remote' (external) (default: none)",
    )
    parser.add_argument(
        "--eunomia-policy-file",
        default="mcp_policies.json",
        help="Policy file for embedded Eunomia (default: mcp_policies.json)",
    )
    parser.add_argument(
        "--eunomia-remote-url", default=None, help="URL for remote Eunomia server"
    )
    parser.add_argument(
        "--enable-delegation",
        action="store_true",
        default=to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
        help="Enable OIDC token delegation",
    )
    parser.add_argument(
        "--audience",
        default=os.environ.get("AUDIENCE", None),
        help="Audience for the delegated token",
    )
    parser.add_argument(
        "--delegated-scopes",
        default=os.environ.get("DELEGATED_SCOPES", "api"),
        help="Scopes for the delegated token (space-separated)",
    )
    parser.add_argument(
        "--openapi-file",
        default=None,
        help="Path to the OpenAPI JSON file to import additional tools from",
    )
    parser.add_argument(
        "--openapi-base-url",
        default=None,
        help="Base URL for the OpenAPI client (overrides instance URL)",
    )
    parser.add_argument(
        "--openapi-use-token",
        action="store_true",
        help="Use the incoming Bearer token (from MCP request) to authenticate OpenAPI import",
    )

    parser.add_argument(
        "--openapi-username",
        default=os.getenv("OPENAPI_USERNAME"),
        help="Username for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-password",
        default=os.getenv("OPENAPI_PASSWORD"),
        help="Password for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-id",
        default=os.getenv("OPENAPI_CLIENT_ID"),
        help="OAuth client ID for OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-secret",
        default=os.getenv("OPENAPI_CLIENT_SECRET"),
        help="OAuth client secret for OpenAPI import",
    )

    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        usage()

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


def usage():
    print("""
Adguard Home MCP Server

Usage:
  adguard-home-mcp [options]

Options:
  -t, --transport <method>       Transport method: 'stdio' (default), 'streamable-http', or 'sse'
  -s, --host <host>              Host address for HTTP transport (default: 0.0.0.0)
  -p, --port <port>              Port number for HTTP transport (default: 8000)
  --auth-type <type>             Authentication type: 'none', 'static', 'jwt', 'oauth-proxy', 'oidc-proxy', 'remote-oauth'
  --enable-delegation            Enable OIDC token delegation
  --audience <audience>          Audience for delegated token
  --delegated-scopes <scopes>    Scopes for delegated token
  --eunomia-type <type>          Eunomia type: 'none', 'embedded', 'remote'
  --help                         Show this help message

Environment Variables:
  ADGUARD_URL                    URL of AdGuard Home instance
  ADGUARD_USERNAME               Username for AdGuard Home
  ADGUARD_PASSWORD               Password for AdGuard Home
""")


if __name__ == "__main__":
    adguard_home_mcp()
