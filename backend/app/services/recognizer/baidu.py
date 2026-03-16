import base64
import time
from dataclasses import dataclass

import httpx

from app.core.errors import AppError
from app.services.recognizer.base import RecognizerAdapter


@dataclass
class _Token:
    value: str
    expires_at: float


class BaiduRecognizer(RecognizerAdapter):
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        endpoint: str,
        oauth_endpoint: str,
        timeout_seconds: float,
    ) -> None:
        self._api_key = api_key
        self._secret_key = secret_key
        self._endpoint = endpoint
        self._oauth_endpoint = oauth_endpoint
        self._timeout = timeout_seconds
        self._token: _Token | None = None

    def _get_access_token(self) -> str:
        now = time.time()
        if self._token and self._token.expires_at - now > 30:
            return self._token.value

        if not self._api_key or not self._secret_key:
            raise AppError.ai_provider_error("百度 API 密钥未配置")

        params = {"grant_type": "client_credentials", "client_id": self._api_key, "client_secret": self._secret_key}
        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(self._oauth_endpoint, params=params)
        except Exception as e:
            raise AppError.ai_provider_error("获取百度 access_token 失败", details=str(e))

        try:
            payload = resp.json()
        except Exception:
            raise AppError.ai_provider_error("获取百度 access_token 失败", details={"status_code": resp.status_code})

        token = payload.get("access_token")
        expires_in = payload.get("expires_in")
        if not token:
            raise AppError.ai_provider_error("获取百度 access_token 失败", details=payload)

        try:
            expires_in_s = float(expires_in) if expires_in is not None else 3600.0
        except Exception:
            expires_in_s = 3600.0
        self._token = _Token(value=str(token), expires_at=now + expires_in_s)
        return self._token.value

    def recognize(self, image_bytes: bytes, content_type: str) -> str:
        token = self._get_access_token()
        image_b64 = base64.b64encode(image_bytes).decode("ascii")
        params = {"access_token": token}
        data = {"image": image_b64}

        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(self._endpoint, params=params, data=data)
        except Exception as e:
            raise AppError.ai_provider_error("调用百度图像识别失败", details=str(e))

        try:
            payload = resp.json()
        except Exception:
            raise AppError.ai_provider_error("百度图像识别返回非 JSON", details={"status_code": resp.status_code})

        if "error_code" in payload:
            raise AppError.ai_provider_error("百度图像识别失败", details=payload)

        result = payload.get("result") or []
        if isinstance(result, list) and result:
            first = result[0]
            if isinstance(first, dict) and first.get("keyword"):
                return str(first["keyword"])

        return "未知物品"
