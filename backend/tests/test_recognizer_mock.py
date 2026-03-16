from app.services.recognizer.mock import MockRecognizer


def test_mock_recognizer_is_deterministic():
    r = MockRecognizer()
    data = b"abc" * 100
    a = r.recognize(data, "image/jpeg")
    b = r.recognize(data, "image/jpeg")
    assert a == b
