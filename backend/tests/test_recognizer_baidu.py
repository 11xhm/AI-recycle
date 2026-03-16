import types

import httpx
import pytest

from app.core.errors import AppError
from app.services.recognizer.baidu import BaiduRecognizer, _Token


class _Resp:
    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200

    def json(self):
        return self._payload


class _Client:
    def __init__(self, resp):
        self._resp = resp

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def post(self, *_args, **_kwargs):
        return self._resp


def test_baidu_token_missing_keys():
    r = BaiduRecognizer(
        api_key="",
        secret_key="",
        endpoint="https://example.com",
        oauth_endpoint="https://example.com",
        timeout_seconds=1,
    )
    with pytest.raises(AppError) as ei:
        r._get_access_token()
    assert ei.value.code == "AI_PROVIDER_ERROR"


def test_baidu_token_fetch_success_and_cache(monkeypatch):
    calls = {"n": 0}

    def client_factory(*_args, **_kwargs):
        calls["n"] += 1
        return _Client(_Resp({"access_token": "t", "expires_in": 3600}))

    monkeypatch.setattr(httpx, "Client", client_factory)

    r = BaiduRecognizer(
        api_key="k",
        secret_key="s",
        endpoint="https://example.com",
        oauth_endpoint="https://example.com",
        timeout_seconds=1,
    )
    assert r._get_access_token() == "t"
    assert r._get_access_token() == "t"
    assert calls["n"] == 1


def test_baidu_recognize_parses_keyword(monkeypatch):
    def client_factory(*_args, **_kwargs):
        return _Client(_Resp({"result": [{"keyword": "纸箱", "score": 0.9}]}))

    monkeypatch.setattr(httpx, "Client", client_factory)

    r = BaiduRecognizer(
        api_key="k",
        secret_key="s",
        endpoint="https://example.com",
        oauth_endpoint="https://example.com",
        timeout_seconds=1,
    )
    r._token = _Token(value="t", expires_at=10**12)
    assert r.recognize(b"abc", "image/jpeg") == "纸箱"


def test_baidu_recognize_error_code(monkeypatch):
    def client_factory(*_args, **_kwargs):
        return _Client(_Resp({"error_code": 17, "error_msg": "bad"}))

    monkeypatch.setattr(httpx, "Client", client_factory)

    r = BaiduRecognizer(
        api_key="k",
        secret_key="s",
        endpoint="https://example.com",
        oauth_endpoint="https://example.com",
        timeout_seconds=1,
    )
    r._token = _Token(value="t", expires_at=10**12)
    with pytest.raises(AppError) as ei:
        r.recognize(b"abc", "image/jpeg")
    assert ei.value.code == "AI_PROVIDER_ERROR"
