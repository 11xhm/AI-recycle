from app.core.config import Settings
from app.services.recognizer.baidu import BaiduRecognizer
from app.services.recognizer.base import RecognizerAdapter
from app.services.recognizer.mock import MockRecognizer

_recognizer: RecognizerAdapter | None = None


def get_recognizer(settings: Settings) -> RecognizerAdapter:
    global _recognizer
    if settings.ai_mock or settings.ai_provider == "mock":
        if not isinstance(_recognizer, MockRecognizer):
            _recognizer = MockRecognizer()
        return _recognizer

    if settings.ai_provider == "baidu":
        if not isinstance(_recognizer, BaiduRecognizer):
            _recognizer = BaiduRecognizer(
                api_key=settings.baidu_api_key,
                secret_key=settings.baidu_secret_key,
                endpoint=settings.baidu_endpoint,
                oauth_endpoint=settings.baidu_oauth_endpoint,
                timeout_seconds=settings.ai_timeout_seconds,
            )
        return _recognizer

    _recognizer = MockRecognizer()
    return _recognizer
