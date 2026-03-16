import hashlib

from app.services.recognizer.base import RecognizerAdapter


class MockRecognizer(RecognizerAdapter):
    def __init__(self) -> None:
        self._candidates = [
            "纸箱",
            "塑料瓶",
            "旧手机",
            "旧衣服",
            "易拉罐",
            "废纸",
            "玻璃瓶",
            "电池",
            "金属",
            "书本",
        ]

    def recognize(self, image_bytes: bytes, content_type: str) -> str:
        h = hashlib.sha1(image_bytes).digest()
        idx = int.from_bytes(h[:2], "big") % len(self._candidates)
        return self._candidates[idx]
