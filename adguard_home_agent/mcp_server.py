#!/usr/bin/python
import warnings

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
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from adguard_home_agent.auth import get_client

__version__ = "0.12.0"

logger = get_logger(name="adguard-home-agent")
logger.setLevel(logging.INFO)


def register_system_tools(mcp: FastMCP):
    @mcp.tool(tags={"system"})
    async def adguard_home_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_version', 'set_protection', 'clear_cache'"
        ),
        enabled: bool | None = Field(default=None, description="enabled"),
        duration: int | None = Field(default=None, description="duration"),
        client=Depends(get_client),
    ) -> dict:
        """Manage system operations.

        Actions:
          - 'get_version': Get AdGuard Home status/version.
          - 'set_protection': Set protection state and duration.
          - 'clear_cache': Clear DNS cache.
        """
        kwargs: dict[str, Any]
        if action == "get_version":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_version(**kwargs)
        if action == "set_protection":
            kwargs = {"enabled": enabled, "duration": duration}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_protection(**kwargs)
        if action == "clear_cache":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.clear_cache(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_version', 'set_protection', 'clear_cache"
        )


def register_access_tools(mcp: FastMCP):
    @mcp.tool(tags={"access"})
    async def adguard_home_access(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_access_list', 'set_access_list'"
        ),
        allowed_clients: list[str] | None = Field(
            default=None, description="allowed clients"
        ),
        disallowed_clients: list[str] | None = Field(
            default=None, description="disallowed clients"
        ),
        blocked_hosts: list[str] | None = Field(
            default=None, description="blocked hosts"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage access operations.

        Actions:
          - 'get_access_list': Call get_access_list
          - 'set_access_list': Set access list.
        """
        kwargs: dict[str, Any]
        if action == "get_access_list":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_access_list(**kwargs)
        if action == "set_access_list":
            kwargs = {
                "allowed_clients": allowed_clients,
                "disallowed_clients": disallowed_clients,
                "blocked_hosts": blocked_hosts,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_access_list(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_access_list', 'set_access_list"
        )


def register_blocked_services_tools(mcp: FastMCP):
    @mcp.tool(tags={"blocked-services"})
    async def adguard_home_blocked_services(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_blocked_services_list', 'get_all_blocked_services', 'update_blocked_services'"
        ),
        services: list[str] | None = Field(default=None, description="services"),
        client=Depends(get_client),
    ) -> dict:
        """Manage blocked services operations.

        Actions:
          - 'get_blocked_services_list': Get blocked services list.
          - 'get_all_blocked_services': Get available services to use for blocking.
          - 'update_blocked_services': Update blocked services list.
        """
        kwargs: dict[str, Any]
        if action == "get_blocked_services_list":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_blocked_services_list(**kwargs)
        if action == "get_all_blocked_services":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_blocked_services(**kwargs)
        if action == "update_blocked_services":
            kwargs = {"services": services}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_blocked_services(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_blocked_services_list', 'get_all_blocked_services', 'update_blocked_services"
        )


def register_filtering_tools(mcp: FastMCP):
    @mcp.tool(tags={"filtering"})
    async def adguard_home_filtering(
        action: str = Field(
            description="Action to perform. Must be one of: 'set_filtering_rules', 'check_host_filtering', 'set_filter_url_params', 'get_filtering_status', 'set_filtering_config', 'add_filter_url', 'remove_filter_url', 'refresh_filters'"
        ),
        enabled: bool | None = Field(default=None, description="enabled"),
        interval: int | None = Field(default=None, description="interval"),
        name: str | None = Field(default=None, description="name"),
        url: str | None = Field(default=None, description="url"),
        whitelist: bool | None = Field(default=None, description="whitelist"),
        rules: list[str] | None = Field(default=None, description="rules"),
        client=Depends(get_client),
    ) -> dict:
        """Manage filtering operations.

        Actions:
          - 'set_filtering_rules': Set user-defined filter rules.
          - 'check_host_filtering': Check if host name is filtered.
          - 'set_filter_url_params': Set URL parameters.
          - 'get_filtering_status': Get filtering status.
          - 'set_filtering_config': Set filtering configuration.
          - 'add_filter_url': Add a filter URL.
          - 'remove_filter_url': Remove a filter URL.
          - 'refresh_filters': Refresh all filters.
        """
        kwargs: dict[str, Any]
        if action == "set_filtering_rules":
            kwargs = {"rules": rules}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_filtering_rules(**kwargs)
        if action == "check_host_filtering":
            kwargs = {"name": name}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.check_host_filtering(**kwargs)
        if action == "set_filter_url_params":
            kwargs = {"url": url, "name": name, "whitelist": whitelist}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_filter_url_params(**kwargs)
        if action == "get_filtering_status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_filtering_status(**kwargs)
        if action == "set_filtering_config":
            kwargs = {"enabled": enabled, "interval": interval}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_filtering_config(**kwargs)
        if action == "add_filter_url":
            kwargs = {"name": name, "url": url, "whitelist": whitelist}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_filter_url(**kwargs)
        if action == "remove_filter_url":
            kwargs = {"url": url, "whitelist": whitelist}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_filter_url(**kwargs)
        if action == "refresh_filters":
            kwargs = {"whitelist": whitelist}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.refresh_filters(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: set_filtering_rules', 'check_host_filtering', 'set_filter_url_params', 'get_filtering_status', 'set_filtering_config', 'add_filter_url', 'remove_filter_url', 'refresh_filters"
        )


def register_clients_tools(mcp: FastMCP):
    @mcp.tool(tags={"clients"})
    async def adguard_home_clients(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_clients', 'search_clients', 'add_client', 'update_client', 'delete_client'"
        ),
        name: str | None = Field(default=None, description="name"),
        ids: list[str] | None = Field(default=None, description="ids"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        query: str | None = Field(default=None, description="query"),
        client=Depends(get_client),
    ) -> dict:
        """Manage clients operations.

        Actions:
          - 'list_clients': List clients.
          - 'search_clients': Search for clients.
          - 'add_client': Add a new client.
          - 'update_client': Update a client.
          - 'delete_client': Delete a client.
        """
        kwargs: dict[str, Any]
        if action == "list_clients":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_clients(**kwargs)
        if action == "search_clients":
            kwargs = {"query": query}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.search_clients(**kwargs)
        if action == "add_client":
            kwargs = {"name": name, "ids": ids}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_client(**kwargs)
        if action == "update_client":
            kwargs = {"name": name, "data": data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_client(**kwargs)
        if action == "delete_client":
            kwargs = {"name": name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_client(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_clients', 'search_clients', 'add_client', 'update_client', 'delete_client"
        )


def register_profile_tools(mcp: FastMCP):
    @mcp.tool(tags={"profile"})
    async def adguard_home_profile(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_profile', 'update_profile'"
        ),
        profile_data: dict[str, Any] | None = Field(
            default=None, description="profile data"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage profile operations.

        Actions:
          - 'get_profile': Get current user info.
          - 'update_profile': Update current user info.
        """
        kwargs: dict[str, Any]
        if action == "get_profile":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_profile(**kwargs)
        if action == "update_profile":
            kwargs = {"profile_data": profile_data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_profile(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_profile', 'update_profile"
        )


def register_dhcp_tools(mcp: FastMCP):
    @mcp.tool(tags={"dhcp"})
    async def adguard_home_dhcp(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_dhcp_status', 'get_dhcp_interfaces', 'set_dhcp_config', 'find_active_dhcp', 'add_dhcp_static_lease', 'remove_dhcp_static_lease', 'update_dhcp_static_lease', 'reset_dhcp', 'reset_dhcp_leases'"
        ),
        config: dict[str, Any] | None = Field(default=None, description="config"),
        mac: str | None = Field(default=None, description="mac"),
        ip: str | None = Field(default=None, description="ip"),
        hostname: str | None = Field(default=None, description="hostname"),
        interface: str | None = Field(default=None, description="interface"),
        client=Depends(get_client),
    ) -> dict:
        """Manage dhcp operations.

        Actions:
          - 'get_dhcp_status': Get DHCP status.
          - 'get_dhcp_interfaces': Get available interfaces.
          - 'set_dhcp_config': Set DHCP configuration.
          - 'find_active_dhcp': Search for an active DHCP server on the network.
          - 'add_dhcp_static_lease': Add a static DHCP lease.
          - 'remove_dhcp_static_lease': Remove a static DHCP lease.
          - 'update_dhcp_static_lease': Update a static DHCP lease.
          - 'reset_dhcp': Reset DHCP configuration.
          - 'reset_dhcp_leases': Reset DHCP leases.
        """
        kwargs: dict[str, Any]
        if action == "get_dhcp_status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_dhcp_status(**kwargs)
        if action == "get_dhcp_interfaces":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_dhcp_interfaces(**kwargs)
        if action == "set_dhcp_config":
            kwargs = {"config": config}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_dhcp_config(**kwargs)
        if action == "find_active_dhcp":
            kwargs = {"interface": interface}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.find_active_dhcp(**kwargs)
        if action == "add_dhcp_static_lease":
            kwargs = {"mac": mac, "ip": ip, "hostname": hostname}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_dhcp_static_lease(**kwargs)
        if action == "remove_dhcp_static_lease":
            kwargs = {"mac": mac, "ip": ip, "hostname": hostname}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_dhcp_static_lease(**kwargs)
        if action == "update_dhcp_static_lease":
            kwargs = {"mac": mac, "ip": ip, "hostname": hostname}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_dhcp_static_lease(**kwargs)
        if action == "reset_dhcp":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.reset_dhcp(**kwargs)
        if action == "reset_dhcp_leases":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.reset_dhcp_leases(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_dhcp_status', 'get_dhcp_interfaces', 'set_dhcp_config', 'find_active_dhcp', 'add_dhcp_static_lease', 'remove_dhcp_static_lease', 'update_dhcp_static_lease', 'reset_dhcp', 'reset_dhcp_leases"
        )


def register_settings_tools(mcp: FastMCP):
    @mcp.tool(tags={"settings"})
    async def adguard_home_settings(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_parental_status', 'enable_parental_control', 'disable_parental_control', 'get_safebrowsing_status', 'enable_safebrowsing', 'disable_safebrowsing', 'get_safesearch_status'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage settings operations.

        Actions:
          - 'get_parental_status': Get parental control status.
          - 'enable_parental_control': Enable parental control.
          - 'disable_parental_control': Disable parental control.
          - 'get_safebrowsing_status': Get safe browsing status.
          - 'enable_safebrowsing': Enable safe browsing.
          - 'disable_safebrowsing': Disable safe browsing.
          - 'get_safesearch_status': Get safe search status.
        """
        kwargs: dict[str, Any]
        if action == "get_parental_status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_parental_status(**kwargs)
        if action == "enable_parental_control":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.enable_parental_control(**kwargs)
        if action == "disable_parental_control":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.disable_parental_control(**kwargs)
        if action == "get_safebrowsing_status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_safebrowsing_status(**kwargs)
        if action == "enable_safebrowsing":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.enable_safebrowsing(**kwargs)
        if action == "disable_safebrowsing":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.disable_safebrowsing(**kwargs)
        if action == "get_safesearch_status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_safesearch_status(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_parental_status', 'enable_parental_control', 'disable_parental_control', 'get_safebrowsing_status', 'enable_safebrowsing', 'disable_safebrowsing', 'get_safesearch_status"
        )


def register_query_log_tools(mcp: FastMCP):
    @mcp.tool(tags={"query-log"})
    async def adguard_home_query_log(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_query_log', 'clear_query_log'"
        ),
        limit: int | None = Field(default=None, description="limit"),
        older_than: str | None = Field(default=None, description="older than"),
        response_status: str | None = Field(
            default=None, description="response status"
        ),
        search: str | None = Field(default=None, description="search"),
        client=Depends(get_client),
    ) -> dict:
        """Manage query log operations.

        Actions:
          - 'get_query_log': Gets query log.
          - 'clear_query_log': Clear query log.
        """
        kwargs: dict[str, Any]
        if action == "get_query_log":
            kwargs = {
                "limit": limit,
                "older_than": older_than,
                "response_status": response_status,
                "search": search,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_query_log(**kwargs)
        if action == "clear_query_log":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.clear_query_log(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_query_log', 'clear_query_log"
        )


def register_rewrites_tools(mcp: FastMCP):
    @mcp.tool(tags={"rewrites"})
    async def adguard_home_rewrites(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_rewrites', 'add_rewrite', 'delete_rewrite', 'update_rewrite', 'get_rewrite_settings', 'update_rewrite_settings'"
        ),
        domain: str | None = Field(default=None, description="domain"),
        answer: str | None = Field(default=None, description="answer"),
        target: dict[str, Any] | None = Field(default=None, description="target"),
        update: dict[str, Any] | None = Field(default=None, description="update"),
        enabled: bool | None = Field(default=None, description="enabled"),
        client=Depends(get_client),
    ) -> dict:
        """Manage rewrites operations.

        Actions:
          - 'list_rewrites': List DNS rewrites.
          - 'add_rewrite': Add a DNS rewrite.
          - 'delete_rewrite': Delete a DNS rewrite.
          - 'update_rewrite': Update a DNS rewrite.
          - 'get_rewrite_settings': Get rewrite settings.
          - 'update_rewrite_settings': Update rewrite settings.
        """
        kwargs: dict[str, Any]
        if action == "list_rewrites":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_rewrites(**kwargs)
        if action == "add_rewrite":
            kwargs = {"domain": domain, "answer": answer}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_rewrite(**kwargs)
        if action == "delete_rewrite":
            kwargs = {"domain": domain, "answer": answer}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_rewrite(**kwargs)
        if action == "update_rewrite":
            kwargs = {"target": target, "update": update}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_rewrite(**kwargs)
        if action == "get_rewrite_settings":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_rewrite_settings(**kwargs)
        if action == "update_rewrite_settings":
            kwargs = {"enabled": enabled}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_rewrite_settings(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_rewrites', 'add_rewrite', 'delete_rewrite', 'update_rewrite', 'get_rewrite_settings', 'update_rewrite_settings"
        )


def register_tls_tools(mcp: FastMCP):
    @mcp.tool(tags={"tls"})
    async def adguard_home_tls(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_tls_status', 'configure_tls', 'validate_tls'"
        ),
        config: dict[str, Any] | None = Field(default=None, description="config"),
        client=Depends(get_client),
    ) -> dict:
        """Manage tls operations.

        Actions:
          - 'get_tls_status': Returns TLS configuration and its status.
          - 'configure_tls': Updates current TLS configuration.
          - 'validate_tls': Checks if the current TLS configuration is valid.
        """
        kwargs: dict[str, Any]
        if action == "get_tls_status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_tls_status(**kwargs)
        if action == "configure_tls":
            kwargs = {"config": config}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.configure_tls(**kwargs)
        if action == "validate_tls":
            kwargs = {"config": config}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.validate_tls(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_tls_status', 'configure_tls', 'validate_tls"
        )


def register_mobile_tools(mcp: FastMCP):
    @mcp.tool(tags={"mobile"})
    async def adguard_home_mobile(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_doh_mobile_config', 'get_dot_mobile_config'"
        ),
        host: str | None = Field(default=None, description="host"),
        client_id: str | None = Field(default=None, description="client id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage mobile operations.

        Actions:
          - 'get_doh_mobile_config': Get DNS over HTTPS .mobileconfig.
          - 'get_dot_mobile_config': Get DNS over TLS .mobileconfig.
        """
        kwargs: dict[str, Any]
        if action == "get_doh_mobile_config":
            kwargs = {"host": host, "client_id": client_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_doh_mobile_config(**kwargs)
        if action == "get_dot_mobile_config":
            kwargs = {"host": host, "client_id": client_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_dot_mobile_config(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_doh_mobile_config', 'get_dot_mobile_config"
        )


def register_stats_tools(mcp: FastMCP):
    @mcp.tool(tags={"stats"})
    async def adguard_home_stats(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_stats', 'reset_stats', 'get_stats_config', 'set_stats_config'"
        ),
        interval: int | None = Field(default=None, description="interval"),
        client=Depends(get_client),
    ) -> dict:
        """Manage stats operations.

        Actions:
          - 'get_stats': Get overall statistics.
          - 'reset_stats': Reset all statistics to zeroes.
          - 'get_stats_config': Get statistics parameters.
          - 'set_stats_config': Set statistics parameters.
        """
        kwargs: dict[str, Any]
        if action == "get_stats":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_stats(**kwargs)
        if action == "reset_stats":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.reset_stats(**kwargs)
        if action == "get_stats_config":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_stats_config(**kwargs)
        if action == "set_stats_config":
            kwargs = {"interval": interval}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_stats_config(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_stats', 'reset_stats', 'get_stats_config', 'set_stats_config"
        )


def register_dns_tools(mcp: FastMCP):
    @mcp.tool(tags={"dns"})
    async def adguard_home_dns(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_dns_info', 'set_dns_config', 'test_upstream_dns'"
        ),
        config: dict[str, Any] | None = Field(default=None, description="config"),
        upstreams: list[str] | None = Field(default=None, description="upstreams"),
        client=Depends(get_client),
    ) -> dict:
        """Manage dns operations.

        Actions:
          - 'get_dns_info': Get general DNS parameters.
          - 'set_dns_config': Set general DNS parameters.
          - 'test_upstream_dns': Test upstream configuration.
        """
        kwargs: dict[str, Any]
        if action == "get_dns_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_dns_info(**kwargs)
        if action == "set_dns_config":
            kwargs = {"config": config}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_dns_config(**kwargs)
        if action == "test_upstream_dns":
            kwargs = {"upstreams": upstreams}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.test_upstream_dns(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_dns_info', 'set_dns_config', 'test_upstream_dns"
        )


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
