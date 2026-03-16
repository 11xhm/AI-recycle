import json
from pathlib import Path
from threading import RLock


class PricingService:
    def __init__(self, pricing_path: Path) -> None:
        self._path = pricing_path
        self._lock = RLock()
        self._stat_key: tuple[int, int, int] | None = None
        self._pricing: dict[str, float] = {}

    def _load_if_needed(self) -> None:
        with self._lock:
            try:
                stat = self._path.stat()
            except FileNotFoundError:
                self._stat_key = None
                self._pricing = {}
                return

            stat_key = (stat.st_mtime_ns, getattr(stat, "st_ctime_ns", stat.st_mtime_ns), stat.st_size)
            if self._stat_key == stat_key:
                return

            data = json.loads(self._path.read_text(encoding="utf-8"))
            pricing: dict[str, float] = {}
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(k, str):
                        try:
                            pricing[k] = float(v)
                        except Exception:
                            continue
            self._pricing = pricing
            self._stat_key = stat_key

    def get_price(self, item_name: str) -> float:
        self._load_if_needed()
        name = (item_name or "").strip()
        if not name:
            return 0.0

        best = 0.0
        for keyword, price in self._pricing.items():
            if keyword and keyword in name:
                if price > best:
                    best = price
        return float(best)
