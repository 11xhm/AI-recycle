from abc import ABC, abstractmethod


class RecognizerAdapter(ABC):
    @abstractmethod
    def recognize(self, image_bytes: bytes, content_type: str) -> str: ...
