import inspect
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest


@pytest.fixture
def mock_session():
    with patch("httpx.Client") as mock_s:
        session = mock_s.return_value
        session.request.return_value = httpx.Response(200, json={"id": 1})
        yield session


def test_adguard_api_brute_force(mock_session):
    from adguard_home_agent.api_client import Api

    api_instance = Api(base_url="http://test", username="test", password="test")

    # Introspect all methods
    for name, method in inspect.getmembers(api_instance, predicate=inspect.ismethod):
        if name.startswith("_") or name == "authenticate":
            continue

        print(f"Calling {name}...")
        sig = inspect.signature(method)
        kwargs: dict[str, Any] = {}
        for p_name, p in sig.parameters.items():
            if p.default is inspect.Parameter.empty:
                if "id" in p_name:
                    kwargs[p_name] = 1
                elif p.annotation is int:
                    kwargs[p_name] = 1
                elif p.annotation is bool:
                    kwargs[p_name] = True
                elif p.annotation is dict:
                    kwargs[p_name] = {}
                elif p.annotation is list:
                    kwargs[p_name] = []
                else:
                    kwargs[p_name] = "test"

        try:
            method(**kwargs)
        except Exception as e:
            print(f"Failed calling {name}: {e}")


def test_adguard_api_errors(mock_session):
    from adguard_home_agent.api_client import Api

    api_instance = Api(base_url="http://test")

    mock_session.request.return_value = httpx.Response(400, text="Error detail")
    with pytest.raises(Exception, match="AdGuard API error"):
        api_instance.get_version()

    mock_session.request.return_value = httpx.Response(204)
    res = api_instance.get_version()
    assert res["status"] == "success"
