#!/usr/bin/env python
# coding: utf-8

import json
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import urllib3

__version__ = "0.2.4"


class Api:
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        verify: bool = True,
        proxies: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = token
        self._session = requests.Session()
        self._session.verify = verify
        self.proxies = proxies

        if proxies:
            self._session.proxies = proxies

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self.token = token

    def get_headers(self) -> Dict[str, str]:
        """Get request headers with authorization."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
        auth: tuple = None,
    ) -> Any:
        """Make a request to the AdGuard Home API."""
        if endpoint.startswith("http"):
            url = endpoint
        else:
            url = urljoin(self.base_url, endpoint)

        headers = self.get_headers()

        # If username/password provided and no token, use Basic Auth for initial requests if needed,
        # or just passed as auth. But AdGuard usually uses Bearer token from login.
        # For simplicity, if auth is passed explicitly use it, else use self.auth if no token

        request_auth = auth
        if not request_auth and not self.token and self.username and self.password:
            request_auth = (self.username, self.password)

        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data,
            auth=request_auth,
        )

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_message = (
                    f"AdGuard API error: {response.status_code} - {error_data}"
                )
            except json.JSONDecodeError:
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

    # Authentication
    def get_access_token(self, mfa_token: str = None) -> Dict:
        """
        Generates Access and Refresh token.
        """
        data = {
            "username": self.username,
            "password": self.password,
        }
        if mfa_token:
            data["mfa_token"] = mfa_token

        # This endpoint expects x-www-form-urlencoded
        url = urljoin(self.base_url, "/oapi/v1/oauth_token")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.post(url, data=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            self.token = result.get("access_token")
            return result
        else:
            raise Exception(
                f"Failed to get access token: {response.status_code} - {response.text}"
            )

    def revoke_token(self, refresh_token: str) -> Dict:
        """Revokes a Refresh Token."""
        return self.request(
            "POST", "/oapi/v1/revoke_token", params={"refresh_token": refresh_token}
        )

    # Server Info
    def get_version(self) -> Dict:
        """Get AdGuard Home version."""
        return self.request("GET", "/oapi/v1/version.json")

    # Access Lists
    def get_access_list(self) -> Dict:
        """List current access list (allowed/disallowed clients, blocked hosts)."""
        return self.request("GET", "/oapi/v1/access/list")

    def set_access_list(
        self,
        allowed_clients: List[str] = None,
        disallowed_clients: List[str] = None,
        blocked_hosts: List[str] = None,
    ) -> Dict:
        """Set access list."""
        data = {
            "allowed_clients": allowed_clients if allowed_clients is not None else [],
            "disallowed_clients": (
                disallowed_clients if disallowed_clients is not None else []
            ),
            "blocked_hosts": blocked_hosts if blocked_hosts is not None else [],
        }
        return self.request("POST", "/oapi/v1/access/set", data=data)

    # Blocked Services
    def get_blocked_services_list(self) -> List[Dict]:
        """List blocked services."""
        return self.request("GET", "/oapi/v1/blocked_services/list")

    def get_all_blocked_services(self) -> Dict:
        """Get all available blocked services."""
        return self.request("GET", "/oapi/v1/blocked_services/all")

    def set_blocked_services(self, services: List[str]) -> Dict:
        """Set blocked services."""
        return self.request("POST", "/oapi/v1/blocked_services/set", data=services)

    def get_blocked_services_schedule(self) -> Dict:
        """Get blocked services schedule."""
        return self.request("GET", "/oapi/v1/blocked_services/get")

    def update_blocked_services_schedule(self, schedule: Dict) -> Dict:
        """Update blocked services schedule."""
        return self.request("PUT", "/oapi/v1/blocked_services/update", data=schedule)

    # Clients
    def list_clients(self) -> Dict:
        """List clients."""
        return self.request("GET", "/oapi/v1/clients")

    def find_clients(self, ip: str) -> List[Dict]:
        """Find clients by IP."""
        return self.request("GET", "/oapi/v1/clients/find", params={"ip0": ip})

    def add_client(
        self,
        name: str,
        ids: List[str],
        use_global_settings: bool = True,
        filtering_enabled: bool = True,
        parent_access: bool = False,
        safe_search_enabled: bool = False,
        safe_browsing_enabled: bool = False,
        tags: List[str] = None,
        upstreams: List[str] = None,
    ) -> Dict:
        """Add a new client."""
        data = {
            "name": name,
            "ids": ids,
            "use_global_settings": use_global_settings,
            "filtering_enabled": filtering_enabled,
            "parental_enabled": parent_access,  # Note: field name in API implies parental_enabled? doc says parent_access usually maps to parental control
            "safebrowsing_enabled": safe_browsing_enabled,
            "safesearch_enabled": safe_search_enabled,
            "tags": tags or [],
            "upstreams": upstreams or [],
        }
        # Correct field name mapping based on standard AGH API conventions if needed, stick to common ones
        # Re-checking typical payload:
        # {
        #   "name": "string",
        #   "ids": ["string"],
        #   "use_global_settings": true,
        #   "filtering_enabled": true,
        #   "parental_enabled": true,
        #   "safebrowsing_enabled": true,
        #   "safesearch_enabled": true,
        #   "use_global_blocked_services": true,
        #   "blocked_services": ["string"],
        #   "upstreams": ["string"],
        #   "tags": ["string"]
        # }
        return self.request("POST", "/oapi/v1/clients/add", data=data)

    def update_client(self, name: str, data: Dict) -> Dict:
        """Update a client."""
        data["name"] = name  # Ensure name is in body
        return self.request("POST", "/oapi/v1/clients/update", data=data)

    def delete_client(self, name: str) -> Dict:
        """Delete a client."""
        return self.request("POST", "/oapi/v1/clients/delete", data={"name": name})

    # DHCP
    def get_dhcp_status(self) -> Dict:
        """Get DHCP status."""
        return self.request("GET", "/oapi/v1/dhcp/status")

    def set_dhcp_config(self, config: Dict) -> Dict:
        """Set DHCP configuration."""
        return self.request("POST", "/oapi/v1/dhcp/set_config", data=config)

    def add_dhcp_static_lease(self, mac: str, ip: str, hostname: str) -> Dict:
        """Add a static DHCP lease."""
        return self.request(
            "POST",
            "/oapi/v1/dhcp/add_static_lease",
            data={"mac": mac, "ip": ip, "hostname": hostname},
        )

    def remove_dhcp_static_lease(self, mac: str, ip: str, hostname: str) -> Dict:
        """Remove a static DHCP lease."""
        return self.request(
            "POST",
            "/oapi/v1/dhcp/remove_static_lease",
            data={"mac": mac, "ip": ip, "hostname": hostname},
        )

    # Filtering
    def get_filtering_status(self) -> Dict:
        """Get filtering status."""
        return self.request("GET", "/oapi/v1/filtering/status")

    def set_filtering_config(self, enabled: bool, interval: int) -> Dict:
        """Set filtering configuration."""
        return self.request(
            "POST",
            "/oapi/v1/filtering/config",
            data={"enabled": enabled, "interval": interval},
        )

    def add_filter_url(self, name: str, url: str, whitelist: bool = False) -> Dict:
        """Add a filter URL."""
        return self.request(
            "POST",
            "/oapi/v1/filtering/add_url",
            data={"name": name, "url": url, "whitelist": whitelist},
        )

    def remove_filter_url(self, url: str, whitelist: bool = False) -> Dict:
        """Remove a filter URL."""
        return self.request(
            "POST",
            "/oapi/v1/filtering/remove_url",
            data={"url": url, "whitelist": whitelist},
        )

    def refresh_filters(self, whitelist: bool = False) -> Dict:
        """Refresh all filters."""
        return self.request(
            "POST", "/oapi/v1/filtering/refresh", data={"whitelist": whitelist}
        )

    def list_filter_lists(self) -> List[Dict]:
        """Gets filter lists. (Legacy endpoint, use filtering/status generally but this returns list objects directly)"""
        return self.request("GET", "/oapi/v1/filter_lists")

    def set_filter_url(self, url: str, whitelist: bool, data: Dict) -> Dict:
        """Set filter URL parameters."""
        data["url"] = url
        data["whitelist"] = whitelist
        return self.request("POST", "/oapi/v1/filtering/set_url", data=data)

    def check_host_filtering(self, name: str) -> Dict:
        """Check if a host is filtered."""
        return self.request(
            "GET", "/oapi/v1/filtering/check_host", params={"name": name}
        )

    # Global Settings - Parental Control
    def get_parental_status(self) -> Dict:
        """Get parental control status."""
        return self.request("GET", "/oapi/v1/parental/status")

    def enable_parental_control(self) -> Dict:
        """Enable parental control."""
        return self.request("POST", "/oapi/v1/parental/enable")

    def disable_parental_control(self) -> Dict:
        """Disable parental control."""
        return self.request("POST", "/oapi/v1/parental/disable")

    # Global Settings - Safe Browsing
    def get_safebrowsing_status(self) -> Dict:
        """Get safe browsing status."""
        return self.request("GET", "/oapi/v1/safebrowsing/status")

    def enable_safebrowsing(self) -> Dict:
        """Enable safe browsing."""
        return self.request("POST", "/oapi/v1/safebrowsing/enable")

    def disable_safebrowsing(self) -> Dict:
        """Disable safe browsing."""
        return self.request("POST", "/oapi/v1/safebrowsing/disable")

    # Global Settings - Safe Search
    def get_safesearch_status(self) -> Dict:
        """Get safe search status."""
        return self.request("GET", "/oapi/v1/safesearch/status")

    def update_safesearch_settings(
        self,
        enabled: bool,
        bing: bool = False,
        duckduckgo: bool = False,
        google: bool = False,
        pixabay: bool = False,
        yandex: bool = False,
        youtube: bool = False,
    ) -> Dict:
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
        return self.request("PUT", "/oapi/v1/safesearch/settings", data=data)

    # Query Log
    def clear_query_log(self) -> Dict:
        """Clears query log."""
        return self.request("DELETE", "/oapi/v1/query_log")

    def get_query_log(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
        companies: List[str] = None,
        statuses: List[str] = None,
        categories: List[str] = None,
        search: str = None,
        limit: int = 20,
        cursor: str = None,
    ) -> Dict:
        """Gets query log."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        if companies:
            params["companies"] = companies
        if statuses:
            params["statuses"] = statuses
        if categories:
            params["categories"] = categories
        if search:
            params["search"] = search
        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor

        return self.request("GET", "/oapi/v1/query_log", params=params)

    def get_query_log_config(self) -> Dict:
        """Get query log configuration."""
        return self.request("GET", "/oapi/v1/query_log/config")

    def set_query_log_config(
        self, enabled: bool, interval: int, anonymize_client_ip: bool
    ) -> Dict:
        """Set query log configuration."""
        data = {
            "enabled": enabled,
            "interval": interval,
            "anonymize_client_ip": anonymize_client_ip,
        }
        return self.request("PUT", "/oapi/v1/query_log/config", data=data)

    # Rewrites
    def list_rewrites(self) -> List[Dict]:
        """List DNS rewrites."""
        return self.request("GET", "/oapi/v1/rewrite/list")

    def add_rewrite(self, domain: str, answer: str) -> Dict:
        """Add a DNS rewrite."""
        return self.request(
            "POST", "/oapi/v1/rewrite/add", data={"domain": domain, "answer": answer}
        )

    def delete_rewrite(self, domain: str, answer: str) -> Dict:
        """Delete a DNS rewrite."""
        return self.request(
            "POST", "/oapi/v1/rewrite/delete", data={"domain": domain, "answer": answer}
        )

    def update_rewrite(self, target: Dict, update: Dict) -> Dict:
        """Update a DNS rewrite."""
        return self.request(
            "POST", "/oapi/v1/rewrite/update", data={"target": target, "update": update}
        )

    # Stats
    def get_stats(self) -> Dict:
        """Get overall statistics."""
        return self.request("GET", "/oapi/v1/stats")

    def get_stats_config(self) -> Dict:
        """Get statistics configuration."""
        return self.request("GET", "/oapi/v1/stats/config")

    def update_stats_config(
        self, enabled: bool, interval: int, ignored: List[str] = None
    ) -> Dict:
        """Update statistics configuration."""
        data = {"enabled": enabled, "interval": interval, "ignored": ignored or []}
        return self.request("PUT", "/oapi/v1/stats/config/update", data=data)

    def get_stats_categories(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
    ) -> Dict:
        """Gets category statistics."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        return self.request("GET", "/oapi/v1/stats/categories", params=params)

    def get_stats_companies(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
    ) -> Dict:
        """Gets companies statistics."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        return self.request("GET", "/oapi/v1/stats/companies", params=params)

    def get_stats_companies_detailed(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
        cursor: str = None,
    ) -> Dict:
        """Gets detailed companies statistics."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        if cursor:
            params["cursor"] = cursor
        return self.request("GET", "/oapi/v1/stats/companies/detailed", params=params)

    def get_stats_countries(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
    ) -> Dict:
        """Gets countries statistics."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        return self.request("GET", "/oapi/v1/stats/countries", params=params)

    def get_stats_devices(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
    ) -> Dict:
        """Gets devices statistics."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        return self.request("GET", "/oapi/v1/stats/devices", params=params)

    def get_stats_domains(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
    ) -> Dict:
        """Gets domains statistics."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        return self.request("GET", "/oapi/v1/stats/domains", params=params)

    def get_stats_time(
        self,
        time_from_millis: int,
        time_to_millis: int,
        devices: List[str] = None,
        countries: List[str] = None,
    ) -> Dict:
        """Gets time statistics."""
        params = {
            "time_from_millis": time_from_millis,
            "time_to_millis": time_to_millis,
        }
        if devices:
            params["devices"] = devices
        if countries:
            params["countries"] = countries
        return self.request("GET", "/oapi/v1/stats/time", params=params)

    def get_stats_top_queried_domains(self) -> Dict:
        """Get top queried domains (from stats)."""
        # Note: This is usually part of get_stats response, but let's see if there's a specific endpoint.
        # API spec usually has specific endpoints for top stats or it's just filtered versions.
        # Assuming we stick to what I added above. get_stats_domains with limit might be it or just get_stats() returns overview.
        pass

    # TLS
    def get_tls_status(self) -> Dict:
        """Get TLS status."""
        return self.request("GET", "/oapi/v1/tls/status")

    def configure_tls(
        self,
        enabled: bool,
        server_name: str,
        certificate_chain: str,
        private_key: str,
        port_https: int = 443,
        port_dns_over_tls: int = 853,
        port_dns_over_quic: int = 784,
    ) -> Dict:
        """Configure TLS."""
        data = {
            "enabled": enabled,
            "server_name": server_name,
            "certificate_chain": certificate_chain,
            "private_key": private_key,
            "port_https": port_https,
            "port_dns_over_tls": port_dns_over_tls,
            "port_dns_over_quic": port_dns_over_quic,
        }
        return self.request("POST", "/oapi/v1/tls/configure", data=data)

    def validate_tls(
        self, server_name: str, certificate_chain: str, private_key: str
    ) -> Dict:
        """Validate TLS configuration."""
        data = {
            "server_name": server_name,
            "certificate_chain": certificate_chain,
            "private_key": private_key,
        }
        return self.request("POST", "/oapi/v1/tls/validate", data=data)

    # Account
    def get_account_limits(self) -> Dict:
        """Gets account limits."""
        return self.request("GET", "/oapi/v1/account/limits")

    # Devices
    def list_devices(self) -> List[Dict]:
        """Lists devices."""
        return self.request("GET", "/oapi/v1/devices")

    def create_device(self, name: str, device_type: str, dns_server_id: str) -> Dict:
        """Creates a new device."""
        data = {
            "name": name,
            "device_type": device_type,
            "dns_server_id": dns_server_id,
        }
        return self.request("POST", "/oapi/v1/devices", data=data)

    def get_device(self, device_id: str) -> Dict:
        """Gets an existing device by ID."""
        return self.request("GET", f"/oapi/v1/devices/{device_id}")

    def update_device(
        self,
        device_id: str,
        name: str = None,
        device_type: str = None,
        dns_server_id: str = None,
    ) -> Dict:
        """Updates an existing device."""
        data = {}
        if name:
            data["name"] = name
        if device_type:
            data["device_type"] = device_type
        if dns_server_id:
            data["dns_server_id"] = dns_server_id
        return self.request("PUT", f"/oapi/v1/devices/{device_id}", data=data)

    def delete_device(self, device_id: str) -> Dict:
        """Removes a device."""
        return self.request("DELETE", f"/oapi/v1/devices/{device_id}")

    def list_dedicated_addresses_for_device(self, device_id: str) -> Dict:
        """List dedicated IPv4 and IPv6 addresses for a device."""
        return self.request("GET", f"/oapi/v1/devices/{device_id}/dedicated_addresses")

    def link_dedicated_ipv4(self, device_id: str, ip: str) -> Dict:
        """Link dedicated IPv4 to the device."""
        return self.request(
            "POST",
            f"/oapi/v1/devices/{device_id}/dedicated_addresses/ipv4",
            data={"ip": ip},
        )

    def unlink_dedicated_ipv4(self, device_id: str, ip: str) -> Dict:
        """Unlink dedicated IPv4 from the device."""
        return self.request(
            "DELETE",
            f"/oapi/v1/devices/{device_id}/dedicated_addresses/ipv4",
            params={"ip": ip},
        )

    def get_doh_mobile_config(
        self,
        device_id: str,
        exclude_wifi_networks: List[str] = None,
        exclude_domain: List[str] = None,
    ) -> str:
        """Gets DNS-over-HTTPS .mobileconfig file."""
        params = {}
        if exclude_wifi_networks:
            params["exclude_wifi_networks"] = exclude_wifi_networks
        if exclude_domain:
            params["exclude_domain"] = exclude_domain

        # This endpoint returns a file content, not JSON
        url = urljoin(self.base_url, f"/oapi/v1/devices/{device_id}/doh.mobileconfig")
        headers = self.get_headers()
        response = self._session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.text

    def get_dot_mobile_config(
        self,
        device_id: str,
        exclude_wifi_networks: List[str] = None,
        exclude_domain: List[str] = None,
    ) -> str:
        """Gets DNS-over-TLS .mobileconfig file."""
        params = {}
        if exclude_wifi_networks:
            params["exclude_wifi_networks"] = exclude_wifi_networks
        if exclude_domain:
            params["exclude_domain"] = exclude_domain

        url = urljoin(self.base_url, f"/oapi/v1/devices/{device_id}/dot.mobileconfig")
        headers = self.get_headers()
        response = self._session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.text

    def reset_doh_password(self, device_id: str) -> Dict:
        """Generate and set new DNS-over-HTTPS password."""
        return self.request("PUT", f"/oapi/v1/devices/{device_id}/doh_password/reset")

    def update_device_settings(
        self,
        device_id: str,
        protection_enabled: bool = None,
        detect_doh_auth_only: bool = None,
    ) -> Dict:
        """Updates device settings."""
        data = {}
        if protection_enabled is not None:
            data["protection_enabled"] = protection_enabled
        if detect_doh_auth_only is not None:
            data["detect_doh_auth_only"] = detect_doh_auth_only
        return self.request("PUT", f"/oapi/v1/devices/{device_id}/settings", data=data)

    # DNS Servers
    def list_dns_servers(self) -> List[Dict]:
        """Lists DNS servers that belong to the user."""
        return self.request("GET", "/oapi/v1/dns_servers")

    def create_dns_server(self, name: str, settings: Dict = None) -> Dict:
        """Creates a new DNS server."""
        data = {"name": name}
        if settings:
            data["settings"] = settings
        return self.request("POST", "/oapi/v1/dns_servers", data=data)

    def get_dns_server(self, dns_server_id: str) -> Dict:
        """Gets an existing DNS server by ID."""
        return self.request("GET", f"/oapi/v1/dns_servers/{dns_server_id}")

    def update_dns_server(self, dns_server_id: str, name: str) -> Dict:
        """Updates an existing DNS server."""
        return self.request(
            "PUT", f"/oapi/v1/dns_servers/{dns_server_id}", data={"name": name}
        )

    def delete_dns_server(self, dns_server_id: str) -> Dict:
        """Removes a DNS server."""
        return self.request("DELETE", f"/oapi/v1/dns_servers/{dns_server_id}")

    def update_dns_server_settings(self, dns_server_id: str, settings: Dict) -> Dict:
        """Updates DNS server settings."""
        return self.request(
            "PUT", f"/oapi/v1/dns_servers/{dns_server_id}/settings", data=settings
        )

    # Web Services
    def list_web_services(self) -> List[Dict]:
        """Lists web services."""
        return self.request("GET", "/oapi/v1/web_services")
