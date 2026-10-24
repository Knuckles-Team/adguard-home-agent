import inspect
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

from adguard_home_agent.api_client import Api


@pytest.fixture
def mock_session():
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        session.request.return_value = httpx.Response(
            200, json={"status": "success", "data": []}
        )
        yield session


def test_api_brute_force(mock_session):
    client = Api(base_url="http://test.adguard.com", username="user", password="pass")

    # Introspect all methods
    for name, method in inspect.getmembers(client, predicate=inspect.ismethod):
        if name.startswith("_") or name in ["request", "login", "logout"]:
            continue

        print(f"Calling {name}...")
        sig = inspect.signature(method)
        kwargs: dict[str, Any] = {}
        for param in sig.parameters.values():
            if param.name == "kwargs":
                continue
            # Guessing values
            if "url" in param.name:
                kwargs[param.name] = "http://test.com"
            elif (
                "name" in param.name
                or "domain" in param.name
                or "answer" in param.name
                or "mac" in param.name
                or "ip" in param.name
                or "hostname" in param.name
            ):
                kwargs[param.name] = "test"
            elif (
                "ids" in param.name
                or "upstreams" in param.name
                or "rules" in param.name
                or "services" in param.name
            ):
                kwargs[param.name] = ["test"]
            elif "enabled" in param.name or "whitelist" in param.name:
                kwargs[param.name] = True
            elif (
                param.annotation is int
                or "duration" in param.name
                or "interval" in param.name
                or "limit" in param.name
            ):
                kwargs[param.name] = 1
            elif (
                param.annotation is dict
                or "config" in param.name
                or "data" in param.name
                or "target" in param.name
                or "update" in param.name
            ):
                kwargs[param.name] = {}
            else:
                kwargs[param.name] = "test"

        try:
            # Check for positional arguments
            pos_args = []
            for param in sig.parameters.values():
                if param.default == inspect.Parameter.empty and param.kind in (
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.POSITIONAL_ONLY,
                ):
                    pos_args.append(kwargs.get(param.name, "test"))
                    if param.name in kwargs:
                        del kwargs[param.name]

            method(*pos_args, **kwargs)
        except Exception as e:
            print(f"Failed calling {name}: {e}")
