"""The MCP surface: one typed tool per API operation, version single-source."""

import asyncio
import sys
from unittest.mock import patch

import adguard_home_agent.auth
from fastmcp import Client

from adguard_home_agent.api_client import Api
from agent_connector_sdk.connector import build_server



def _server():
    with patch.object(sys, "argv", ["adguard-home-agent", "--transport", "stdio"]):
        return build_server("adguard_home_agent", command_args=['--transport', 'stdio'])[1]


def _tools():
    async def _list():
        async with Client(_server()) as client:
            return await client.list_tools()

    return asyncio.run(_list())


def test_every_api_operation_is_a_tool():
    names = {t.name for t in _tools()}
    operations = {
        n
        for n, f in vars(Api).items()
        if callable(f) and not n.startswith("_") and n != "request"
    }
    assert {f"adguard_home_{op}" for op in operations} <= names


def test_no_action_routed_tools():
    for tool in _tools():
        assert "action" not in tool.inputSchema.get("properties", {})
        assert set(tool.inputSchema.get("properties", {})) != {"params_json"}


def test_read_operations_are_annotated_read_only():
    tool = next(t for t in _tools() if t.name == "adguard_home_get_dns_info")
    assert tool.annotations.readOnlyHint is True


def test_dispatch_calls_the_client(monkeypatch):
    class Fake:
        def get_dns_info(self):
            return {"ok": True}

    monkeypatch.setenv("ADGUARD_URL", "http://adguard.example")
    monkeypatch.setattr(adguard_home_agent.auth, "Api", lambda *a, **k: Fake())

    async def _call():
        async with Client(_server()) as client:
            return await client.call_tool("adguard_home_get_dns_info", {})

    assert asyncio.run(_call()).data == {"ok": True}
