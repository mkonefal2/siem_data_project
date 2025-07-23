import pytest
from ioc_feeds.fetchers.threatfox import fetch_threatfox


class DummyResp:
    def __init__(self, status=200, data=None):
        self.status_code = status
        self._data = data or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError('bad status')

    def json(self):
        return self._data


def test_fetch_threatfox_return_empty(monkeypatch):
    def fail_post(*args, **kwargs):
        raise RuntimeError('network')

    monkeypatch.setattr('ioc_feeds.fetchers.threatfox.requests.post', fail_post)
    # should not raise when raise_on_fail=False
    result = fetch_threatfox('u', {}, retries=1, raise_on_fail=False)
    assert result == []

