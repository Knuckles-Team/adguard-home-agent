#!/usr/bin/env python


import json
from typing import Any
from urllib.parse import urljoin

import requests
import urllib3

__version__ = "0.2.57"


class Api:
    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
        verify: bool = True,
        proxies: dict[str, str] | None = None,
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self._session = requests.Session()
        self._session.verify = verify
        self.proxies = proxies

        if proxies:
            self._session.proxies = proxies

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if self.username and self.password:
            self._session.auth = (self.username, self.password)

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> Any:
        """Make a request to the AdGuard Home API."""
        if endpoint.startswith("http"):
            url = endpoint
        else:
            url = urljoin(self.base_url, endpoint)

        headers = {"Content-Type": "application/json"}

        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data,
        )

        if response.status_code >= 400:
            try:
                error_data = response.text
                error_message = (
                    f"AdGuard API error: {response.status_code} - {error_data}"
                )
            except Exception:
                error_message = (
                    f"AdGuard API error: {response.status_code} - {response.text}"
                )
            raise Exception(error_message)

        if response.status_code == 204:
            return {"status": "success"}

        if not response.text.strip():
            return {"status": "success", "message": "Empty response"}

        try:
            return response.json()
        except json.JSONDecodeError:
            return {
                "status": "success",
                "content_type": response.headers.get("Content-Type", "unknown"),
                "text": response.text[:1000],
            }

    def get_version(self) -> dict[str, Any]:
        """Get AdGuard Home status/version."""
        return self.request("GET", "/control/status")

    def get_stats(self) -> dict[str, Any]:
        """Get overall statistics."""
        return self.request("GET", "/control/stats")

    def get_dns_info(self) -> dict[str, Any]:
        """Get general DNS parameters."""
        return self.request("GET", "/control/dns_info")

    def set_dns_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Set general DNS parameters."""
        return self.request("POST", "/control/dns_config", data=config)

    def set_protection(
        self, enabled: bool, duration: int | None = None
    ) -> dict[str, Any]:
        """Set protection state and duration."""
        data: dict[str, Any] = {"enabled": enabled}
        if duration is not None:
            data["duration"] = duration
        return self.request("POST", "/control/protection", data=data)

    def clear_cache(self) -> dict[str, Any]:
        """Clear DNS cache."""
        return self.request("POST", "/control/cache_clear")

    def test_upstream_dns(self, upstreams: list[str]) -> dict[str, Any]:
        """Test upstream configuration."""
        data = {"upstream_dns": upstreams}
        return self.request("POST", "/control/test_upstream_dns", data=data)

    def list_clients(self) -> dict[str, Any]:
        """List clients."""
        return self.request("GET", "/control/clients")

    def add_client(self, name: str, ids: list[str], **kwargs: Any) -> dict[str, Any]:
        """Add a new client.

        Args:
            name: Client name
            ids: List of IP, CIDR, MAC, or ClientIDs
            kwargs: Other client settings (use_global_settings, filtering_enabled, etc)
        """
        data = {
            "name": name,
            "ids": ids,
            "use_global_settings": kwargs.get("use_global_settings", True),
            "filtering_enabled": kwargs.get("filtering_enabled", True),
            "parental_enabled": kwargs.get("parent_access", False),
            "safebrowsing_enabled": kwargs.get("safe_browsing_enabled", False),
            "safesearch_enabled": kwargs.get("safe_search_enabled", False),
            "tags": kwargs.get("tags", []),
            "upstreams": kwargs.get("upstreams", []),
        }
        return self.request("POST", "/control/clients/add", data=data)

    def update_client(self, name: str, data: dict[str, Any]) -> dict[str, Any]:
        """Update a client."""
        data["name"] = name
        return self.request("POST", "/control/clients/update", data=data)

    def delete_client(self, name: str) -> dict[str, Any]:
        """Delete a client."""
        return self.request("POST", "/control/clients/delete", data={"name": name})

    def get_filtering_status(self) -> dict[str, Any]:
        """Get filtering status."""
        return self.request("GET", "/control/filtering/status")

    def set_filtering_config(self, enabled: bool, interval: int) -> dict[str, Any]:
        """Set filtering configuration."""
        return self.request(
            "POST",
            "/control/filtering/config",
            data={"enabled": enabled, "interval": interval},
        )

    def add_filter_url(
        self, name: str, url: str, whitelist: bool = False
    ) -> dict[str, Any]:
        """Add a filter URL."""
        return self.request(
            "POST",
            "/control/filtering/add_url",
            data={"name": name, "url": url, "whitelist": whitelist},
        )

    def remove_filter_url(self, url: str, whitelist: bool = False) -> dict[str, Any]:
        """Remove a filter URL."""
        return self.request(
            "POST",
            "/control/filtering/remove_url",
            data={"url": url, "whitelist": whitelist},
        )

    def refresh_filters(self, whitelist: bool = False) -> dict[str, Any]:
        """Refresh all filters."""
        return self.request(
            "POST", "/control/filtering/refresh", data={"whitelist": whitelist}
        )

    def get_all_blocked_services(self) -> list[dict[str, Any]]:
        """Get available services to use for blocking."""
        return self.request("GET", "/control/blocked_services/all")

    def get_blocked_services_list(self) -> list[str]:
        """Get blocked services list."""
        return self.request("GET", "/control/blocked_services/get")

    def update_blocked_services(self, services: list[str]) -> dict[str, Any]:
        """Update blocked services list."""
        return self.request("PUT", "/control/blocked_services/update", data=services)

    def set_filtering_rules(self, rules: list[str]) -> dict[str, Any]:
        """Set user-defined filter rules."""
        return self.request(
            "POST", "/control/filtering/set_rules", data={"rules": rules}
        )

    def check_host_filtering(self, name: str) -> dict[str, Any]:
        """Check if host name is filtered."""
        return self.request(
            "GET", "/control/filtering/check_host", params={"name": name}
        )

    def set_filter_url_params(
        self, url: str, name: str, whitelist: bool
    ) -> dict[str, Any]:
        """Set URL parameters."""
        data = {"url": url, "name": name, "whitelist": whitelist}
        return self.request("POST", "/control/filtering/set_url", data=data)

    def get_parental_status(self) -> dict[str, Any]:
        """Get parental control status."""
        return self.request("GET", "/control/parental/status")

    def enable_parental_control(self) -> dict[str, Any]:
        """Enable parental control."""
        return self.request("POST", "/control/parental/enable")

    def disable_parental_control(self) -> dict[str, Any]:
        """Disable parental control."""
        return self.request("POST", "/control/parental/disable")

    def get_safebrowsing_status(self) -> dict[str, Any]:
        """Get safe browsing status."""
        return self.request("GET", "/control/safebrowsing/status")

    def enable_safebrowsing(self) -> dict[str, Any]:
        """Enable safe browsing."""
        return self.request("POST", "/control/safebrowsing/enable")

    def disable_safebrowsing(self) -> dict[str, Any]:
        """Disable safe browsing."""
        return self.request("POST", "/control/safebrowsing/disable")

    def get_safesearch_status(self) -> dict[str, Any]:
        """Get safe search status."""
        return self.request("GET", "/control/safesearch/status")

    def update_safesearch_settings(
        self,
        enabled: bool,
        bing: bool = False,
        duckduckgo: bool = False,
        google: bool = False,
        pixabay: bool = False,
        yandex: bool = False,
        youtube: bool = False,
    ) -> dict[str, Any]:
        """Update safe search settings."""
        data = {
            "enabled": enabled,
            "bing": bing,
            "duckduckgo": duckduckgo,
            "google": google,
            "pixabay": pixabay,
            "yandex": yandex,
            "youtube": youtube,
        }
        return self.request("PUT", "/control/safesearch/settings", data=data)

    def get_query_log(
        self,
        limit: int = 20,
        older_than: str = "",
        response_status: str = "",
        search: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Gets query log."""

        params: dict[str, Any] = {
            "limit": limit,
        }
        if older_than:
            params["older_than"] = older_than
        if response_status:
            params["response_status"] = response_status
        if search:
            params["search"] = search

        # Support extra parameters like time_from_millis, time_to_millis
        params.update(kwargs)

        return self.request("GET", "/control/querylog", params=params)

    def get_query_log_config(self) -> dict[str, Any]:
        """Get query log configuration."""
        return self.request("GET", "/control/querylog/config")

    def set_query_log_config(
        self, enabled: bool, interval: int, anonymize_client_ip: bool
    ) -> dict[str, Any]:
        """Set query log configuration."""
        data = {
            "enabled": enabled,
            "interval": interval,
            "anonymize_client_ip": anonymize_client_ip,
        }
        return self.request("POST", "/control/querylog/config", data=data)

    def reset_stats(self) -> dict[str, Any]:
        """Reset all statistics to zeroes."""
        return self.request("POST", "/control/stats_reset")

    def get_stats_config(self) -> dict[str, Any]:
        """Get statistics parameters."""
        return self.request("GET", "/control/stats/config")

    def set_stats_config(self, interval: int) -> dict[str, Any]:
        """Set statistics parameters."""
        return self.request(
            "PUT", "/control/stats/config/update", data={"interval": interval}
        )

    def clear_query_log(self) -> dict[str, Any]:
        """Clear query log."""
        return self.request("POST", "/control/querylog_clear")

    def list_rewrites(self) -> list[dict[str, Any]]:
        """List DNS rewrites."""
        return self.request("GET", "/control/rewrite/list")

    def add_rewrite(self, domain: str, answer: str) -> dict[str, Any]:
        """Add a DNS rewrite."""
        return self.request(
            "POST", "/control/rewrite/add", data={"domain": domain, "answer": answer}
        )

    def delete_rewrite(self, domain: str, answer: str) -> dict[str, Any]:
        """Delete a DNS rewrite."""
        return self.request(
            "POST", "/control/rewrite/delete", data={"domain": domain, "answer": answer}
        )

    def update_rewrite(
        self, target: dict[str, Any], update: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a DNS rewrite."""
        return self.request(
            "POST", "/control/rewrite/update", data={"target": target, "update": update}
        )

    def get_dhcp_status(self) -> dict[str, Any]:
        """Get DHCP status."""
        return self.request("GET", "/control/dhcp/status")

    def set_dhcp_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Set DHCP configuration."""
        return self.request("POST", "/control/dhcp/set_config", data=config)

    def add_dhcp_static_lease(self, mac: str, ip: str, hostname: str) -> dict[str, Any]:
        """Add a static DHCP lease."""
        return self.request(
            "POST",
            "/control/dhcp/add_static_lease",
            data={"mac": mac, "ip": ip, "hostname": hostname},
        )

    def remove_dhcp_static_lease(
        self, mac: str, ip: str, hostname: str
    ) -> dict[str, Any]:
        """Remove a static DHCP lease."""
        return self.request(
            "POST",
            "/control/dhcp/remove_static_lease",
            data={"mac": mac, "ip": ip, "hostname": hostname},
        )

    def access_list(self) -> dict[str, Any]:
        """Get access list."""
        return self.request("GET", "/control/access/list")

    def set_access_list(
        self,
        allowed_clients: list[str] | None = None,
        disallowed_clients: list[str] | None = None,
        blocked_hosts: list[str] | None = None,
    ) -> dict[str, Any]:
        """Set access list."""
        data = {
            "allowed_clients": allowed_clients if allowed_clients is not None else [],
            "disallowed_clients": (
                disallowed_clients if disallowed_clients is not None else []
            ),
            "blocked_hosts": blocked_hosts if blocked_hosts is not None else [],
        }
        return self.request("POST", "/control/access/set", data=data)

    def search_clients(self, query: str) -> list[dict[str, Any]]:
        """Search for clients."""

        return self.request("POST", "/control/clients/search", data={"name": query})

    def get_profile(self) -> dict[str, Any]:
        """Get current user info."""
        return self.request("GET", "/control/profile")

    def update_profile(self, profile_data: dict[str, Any]) -> dict[str, Any]:
        """Update current user info."""
        return self.request("PUT", "/control/profile/update", data=profile_data)

    def login(self, user: str, password: str) -> dict[str, Any]:
        """Perform administrator log-in."""
        return self.request(
            "POST", "/control/login", data={"name": user, "password": password}
        )

    def logout(self) -> dict[str, Any]:
        """Perform administrator log-out."""
        return self.request("GET", "/control/logout")

    def get_dhcp_interfaces(self) -> dict[str, Any]:
        """Get available interfaces."""
        return self.request("GET", "/control/dhcp/interfaces")

    def find_active_dhcp(self, interface: str) -> dict[str, Any]:
        """Search for an active DHCP server on the network."""
        return self.request(
            "POST", "/control/dhcp/find_active_dhcp", data={"interface": interface}
        )

    def update_dhcp_static_lease(
        self, mac: str, ip: str, hostname: str
    ) -> dict[str, Any]:
        """Update a static DHCP lease."""
        return self.request(
            "POST",
            "/control/dhcp/update_static_lease",
            data={"mac": mac, "ip": ip, "hostname": hostname},
        )

    def reset_dhcp(self) -> dict[str, Any]:
        """Reset DHCP configuration."""
        return self.request("POST", "/control/dhcp/reset")

    def reset_dhcp_leases(self) -> dict[str, Any]:
        """Reset DHCP leases."""
        return self.request("POST", "/control/dhcp/reset_leases")

    def get_rewrite_settings(self) -> dict[str, Any]:
        """Get rewrite settings."""
        return self.request("GET", "/control/rewrite/settings")

    def update_rewrite_settings(self, enabled: bool) -> dict[str, Any]:
        """Update rewrite settings."""
        return self.request(
            "PUT", "/control/rewrite/settings/update", data={"enabled": enabled}
        )

    def get_tls_status(self) -> dict[str, Any]:
        """Returns TLS configuration and its status."""
        return self.request("GET", "/control/tls/status")

    def configure_tls(self, config: dict[str, Any]) -> dict[str, Any]:
        """Updates current TLS configuration."""
        return self.request("POST", "/control/tls/configure", data=config)

    def validate_tls(self, config: dict[str, Any]) -> dict[str, Any]:
        """Checks if the current TLS configuration is valid."""
        return self.request("POST", "/control/tls/validate", data=config)

    def get_doh_mobile_config(self, host: str, client_id: str) -> Any:
        """Get DNS over HTTPS .mobileconfig."""

        params = {"host": host, "client_id": client_id}

        return self.request("GET", "/control/apple/doh.mobileconfig", params=params)

    def get_dot_mobile_config(self, host: str, client_id: str) -> Any:
        """Get DNS over TLS .mobileconfig."""
        params = {"host": host, "client_id": client_id}
        return self.request("GET", "/control/apple/dot.mobileconfig", params=params)
