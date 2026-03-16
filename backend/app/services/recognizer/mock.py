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
        h = hashlib.sha256(image_bytes).digest()
        seed = int.from_bytes(h[:8], "big") ^ int.from_bytes(h[8:16], "big") ^ len(image_bytes)
        idx = seed % len(self._candidates)
        return self._candidates[idx]
