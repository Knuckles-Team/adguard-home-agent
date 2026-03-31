#!/usr/bin/env python
               

import importlib
import inspect
from typing import List

__all__: List[str] = []

CORE_MODULES = [
    "adguard_home_agent.api_wrapper",
]

OPTIONAL_MODULES = {
    "adguard_home_agent.agent_server": "agent",
    "adguard_home_agent.mcp_server": "mcp",
}


def _import_module_safely(module_name: str):
    """Try to import a module and return it, or None if not available."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def _expose_members(module):
    """Expose public classes and functions from a module into globals and __all__."""
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) or inspect.isfunction(obj)) and not name.startswith(
            "_"
        ):
                                                                                
            if hasattr(obj, "__module__") and obj.__module__ == module.__name__:
                if name not in globals():
                    globals()[name] = obj
                    __all__.append(name)


for module_name in CORE_MODULES:
    module = importlib.import_module(module_name)
    _expose_members(module)

for module_name, extra_name in OPTIONAL_MODULES.items():
    module = _import_module_safely(module_name)
    if module is not None:
        _expose_members(module)
        globals()[f"_{extra_name.upper()}_AVAILABLE"] = True
    else:
        globals()[f"_{extra_name.upper()}_AVAILABLE"] = False

_MCP_AVAILABLE = OPTIONAL_MODULES.get("adguard_home_agent.mcp_server") in [
    m.__name__ for m in globals().values() if hasattr(m, "__name__")
]
_AGENT_AVAILABLE = "adguard_home_agent.agent_server" in globals()

__all__.extend(["_MCP_AVAILABLE", "_AGENT_AVAILABLE"])


"""
Adguard Home Agent

Manage your Adguard Home instance
"""
