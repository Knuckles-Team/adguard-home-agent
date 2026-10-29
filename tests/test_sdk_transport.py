"""Transport through the SDK (CONN-ADGUARD-HOME-AGENT-R002 to R004)."""

import json
import pathlib
import tomllib

import httpx
import pytest
from agent_connector_sdk.http.support import BaseApiClient

import adguard_home_agent
from adguard_home_agent.api_client import Api

ID = "CONN-ADGUARD-HOME-AGENT"
ROOT = pathlib.Path(__file__).resolve().parents[1]


def _api(handler) -> Api:
    return Api(
        "http://adguard.test", "user", "pass", transport=httpx.MockTransport(handler)
    )


@pytest.mark.spec(f"{ID}-R002")
def test_client_is_the_sdk_base_client():
    assert issubclass(Api, BaseApiClient)
    for path in (ROOT / "adguard_home_agent").rglob("*.py"):
        text = path.read_text()
        assert "import requests" not in text, path
        assert "urllib3" not in text, path


@pytest.mark.spec(f"{ID}-R001")
def test_verification_cannot_be_disabled():
    with pytest.raises(ValueError):
        BaseApiClient("http://adguard.test", verify=False)
    assert (
        "ADGUARD_SSL_VERIFY"
        not in (ROOT / "adguard_home_agent" / "auth.py").read_text()
    )
    assert "verify" not in Api.__init__.__code__.co_varnames


@pytest.mark.spec(f"{ID}-R001")
def test_tls_profile_is_resolved_for_the_adguard_prefix(monkeypatch):
    seen = []
    import agent_connector_sdk.tls.resolve as resolve

    real = resolve.resolve_tls_profile

    def spy(service, **kw):
        seen.append(service)
        return real(service, **kw)

    monkeypatch.setattr(resolve, "resolve_tls_profile", spy)
    _api(lambda _r: httpx.Response(200, json={})).close()
    assert seen == ["ADGUARD"]


@pytest.mark.spec(f"{ID}-R003")
def test_request_shapes_are_unchanged():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("Authorization")
        seen["path"] = request.url.path
        seen["body"] = json.loads(request.content) if request.content else None
        return httpx.Response(200, json={"ok": True})

    api = _api(handler)
    assert api.set_protection(True, 5) == {"ok": True}
    assert seen["auth"].startswith("Basic ")
    assert seen["path"] == "/control/protection"
    assert seen["body"] == {"enabled": True, "duration": 5}

    assert _api(lambda _r: httpx.Response(204)).clear_cache() == {"status": "success"}
    assert (
        _api(lambda _r: httpx.Response(200, text=" ")).get_stats()["message"]
        == "Empty response"
    )
    with pytest.raises(Exception, match=r"AdGuard API error: 400 - bad"):
        _api(lambda _r: httpx.Response(400, text="bad")).get_stats()


@pytest.mark.spec(f"{ID}-R002")
def test_rate_limit_backoff_comes_from_the_sdk(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda _s: None)
    calls = []

    def handler(request):
        calls.append(1)
        if len(calls) == 1:
            return httpx.Response(429, headers={"Retry-After": "1"})
        return httpx.Response(200, json={"n": 1})

    assert _api(handler).get_stats() == {"n": 1}
    assert len(calls) == 2


@pytest.mark.spec(f"{ID}-R004")
def test_dependencies_come_from_the_sdk():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    deps = project["dependencies"]
    assert not any(d.startswith("requests") for d in deps)
    sdk = next(d for d in deps if d.startswith("scion-sdk"))
    assert ">=0.5.4" in sdk
    assert adguard_home_agent
