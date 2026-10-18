"""The MCP surface: one typed tool per API operation, version single-source."""

import asyncio
import importlib
import sys
from unittest.mock import patch

from fastmcp import Client

from adguard_home_agent import _version
from adguard_home_agent.api_client import Api

server_module = importlib.import_module("adguard_home_agent.mcp_server")


def _server():
    with patch.object(sys, "argv", ["adguard-mcp", "--transport", "stdio"]):
        return server_module.get_mcp_instance()[0]


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

    monkeypatch.setattr(sys.modules["adguard_home_agent.mcp_server"], "get_client", lambda: Fake())

    async def _call():
        async with Client(_server()) as client:
            return await client.call_tool("adguard_home_get_dns_info", {})

    assert asyncio.run(_call()).data == {"ok": True}


def test_version_single_source():
    from adguard_home_agent import api_client

    assert api_client.__version__ == _version.__version__
