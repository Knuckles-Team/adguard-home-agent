"""TLS comes from the SDK profile: verified by default, CA carried, never silenced."""

import ssl
import warnings
from pathlib import Path
from unittest.mock import patch

import pytest
from scion_sdk.http.support import BaseApiClient

from adguard_home_agent.api_client import Api
from adguard_home_agent.auth import get_client


def _self_signed_ca() -> bytes:
    from datetime import datetime, timedelta, timezone

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "test-ca")])
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=30))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )
    return cert.public_bytes(serialization.Encoding.PEM)


@pytest.mark.spec("CONN-ADGUARD-HOME-AGENT-R001")
def test_default_verifies(monkeypatch):
    monkeypatch.setenv("ADGUARD_URL", "https://dns.test")
    client = get_client()
    assert client._trust.verify_enabled
    assert client._trust.ssl_context.verify_mode == ssl.CERT_REQUIRED


@pytest.mark.spec("CONN-ADGUARD-HOME-AGENT-R001")
def test_ca_bundle_is_carried(monkeypatch, tmp_path: Path):
    bundle = tmp_path / "ca.pem"
    bundle.write_bytes(_self_signed_ca())
    monkeypatch.setenv("ADGUARD_URL", "https://dns.test")
    monkeypatch.setenv("ADGUARD_CA_BUNDLE", str(bundle))
    client = get_client()
    assert client._trust.verify_enabled
    assert str(bundle) in str(client._trust.requests_kwargs().get("verify"))


@pytest.mark.spec("CONN-ADGUARD-HOME-AGENT-R001")
def test_verify_switch_is_gone(monkeypatch):
    monkeypatch.setenv("ADGUARD_SSL_VERIFY", "false")
    client = Api(base_url="https://dns.test")
    assert isinstance(client, BaseApiClient)
    assert client._trust.verify_enabled
    with pytest.raises(ValueError):
        BaseApiClient("https://dns.test", verify=False)


@pytest.mark.spec("CONN-ADGUARD-HOME-AGENT-R001")
def test_warning_never_silenced():
    try:  # urllib3 is no longer pulled in by the SDK transport; check it only when present
        import urllib3  # noqa: F401
    except ImportError:
        pass
    else:
        with patch("urllib3.disable_warnings") as silence:
            Api(base_url="https://dns.test")
        silence.assert_not_called()
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        Api(base_url="https://dns.test")
