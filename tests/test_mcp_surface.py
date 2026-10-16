"""The MCP surface: action-routed tools, version single-source, dispatch."""

import asyncio

import pytest
from fastmcp import Client, FastMCP

from adguard_home_agent import _version, mcp as tools
from adguard_home_agent.mcp import mcp_dns


def _server() -> FastMCP:
    server: FastMCP = FastMCP("test")
    for name in tools.__all__:
        getattr(tools, name)(server)
    return server


def test_every_domain_registers_one_tool():
    async def _names():
        async with Client(_server()) as client:
            return {t.name for t in await client.list_tools()}

    names = asyncio.run(_names())
    assert len(names) == len(tools.__all__) == 14
    assert "adguard_home_dns" in names


def test_action_is_an_enum_in_the_schema():
    async def _schema():
        async with Client(_server()) as client:
            return next(
                t for t in await client.list_tools() if t.name == "adguard_home_dns"
            )

    tool = asyncio.run(_schema())
    assert set(tool.inputSchema["properties"]["action"]["enum"]) == set(
        mcp_dns.ACTIONS
    )


def test_dispatch_calls_the_client(monkeypatch):
    class Fake:
        def get_dns_info(self):
            return {"ok": True}

    monkeypatch.setattr(mcp_dns, "get_client", lambda: Fake())

    async def _call():
        async with Client(_server()) as client:
            return await client.call_tool(
                "adguard_home_dns", {"action": "get_dns_info"}
            )

    result = asyncio.run(_call())
    assert result.data == {"ok": True}


def test_unknown_action_is_rejected():
    async def _call():
        async with Client(_server()) as client:
            return await client.call_tool("adguard_home_dns", {"action": "nope"})

    with pytest.raises(Exception):
        asyncio.run(_call())


def test_version_single_source():
    from adguard_home_agent import api_client

    assert api_client.__version__ == _version.__version__
