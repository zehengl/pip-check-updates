from types import SimpleNamespace

from pip_check_updates.version import (
    _get_latest_version_cached,
    get_latest_version,
)


def test_get_latest_version_caches_pypi_requests(monkeypatch):
    calls = []

    def fake_get(url, verify=True):
        calls.append((url, verify))
        return SimpleNamespace(
            status_code=200,
            json=lambda: {"info": {"version": "2.0.0"}, "releases": {}},
        )

    monkeypatch.setattr("pip_check_updates.version.requests.get", fake_get)
    _get_latest_version_cached.cache_clear()

    assert get_latest_version("demo-package", "pypi", False, False) == "2.0.0"
    assert get_latest_version("demo-package", "pypi", False, False) == "2.0.0"
    assert len(calls) == 1


def test_get_latest_version_caches_conda_requests(monkeypatch):
    calls = []

    def fake_get(url, verify=True):
        calls.append((url, verify))
        return SimpleNamespace(
            status_code=200,
            content=b'<html><small class="subheader">1.4.0</small></html>',
        )

    monkeypatch.setattr("pip_check_updates.version.requests.get", fake_get)
    _get_latest_version_cached.cache_clear()

    source = ["conda-forge", "defaults"]
    assert get_latest_version("demo-package", source, False, False) == "1.4.0"
    assert get_latest_version("demo-package", source, False, False) == "1.4.0"
    assert len(calls) == 1