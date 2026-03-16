from pathlib import Path

from fastapi.testclient import TestClient

from app.api import routes
from app.core.config import settings
from app.services.pricing import PricingService
from app.services.recognizer.mock import MockRecognizer
from main import create_app


def _patch_pricing(tmp_path: Path, keyword: str, price: float) -> None:
    pricing_path = tmp_path / "pricing.json"
    pricing_path.write_text(f'{{"{keyword}": {price}}}\n', encoding="utf-8")
    routes._pricing = PricingService(pricing_path)


def test_recognize_success_mock(tmp_path: Path):
    old_max = settings.max_upload_bytes
    old_mock = settings.ai_mock
    old_provider = settings.ai_provider
    settings.ai_mock = True
    settings.ai_provider = "mock"
    settings.max_upload_bytes = 10 * 1024 * 1024

    data = b"xyz" * 2000
    expected_item = MockRecognizer().recognize(data, "image/jpeg")
    _patch_pricing(tmp_path, expected_item, 9.9)

    app = create_app()
    client = TestClient(app)
    res = client.post("/api/recognize", files={"file": ("t.jpg", data, "image/jpeg")})
    assert res.status_code == 200
    body = res.json()
    assert body["item"] == expected_item
    assert body["price"] == 9.9
    assert body["currency"] == "CNY"
    settings.max_upload_bytes = old_max
    settings.ai_mock = old_mock
    settings.ai_provider = old_provider


def test_recognize_rejects_non_image():
    app = create_app()
    client = TestClient(app)
    res = client.post("/api/recognize", files={"file": ("t.txt", b"hi", "text/plain")})
    assert res.status_code == 415
    body = res.json()
    assert body["error"]["code"] == "UNSUPPORTED_FILE"


def test_recognize_rejects_too_large(tmp_path: Path):
    old_max = settings.max_upload_bytes
    old_mock = settings.ai_mock
    old_provider = settings.ai_provider
    settings.ai_mock = True
    settings.ai_provider = "mock"
    settings.max_upload_bytes = 10

    routes._pricing = PricingService(tmp_path / "pricing.json")

    app = create_app()
    client = TestClient(app)
    res = client.post("/api/recognize", files={"file": ("t.jpg", b"x" * 100, "image/jpeg")})
    assert res.status_code == 400
    body = res.json()
    assert body["error"]["code"] == "INVALID_REQUEST"
    settings.max_upload_bytes = old_max
    settings.ai_mock = old_mock
    settings.ai_provider = old_provider
