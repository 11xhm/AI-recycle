import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from app.services.pricing import PricingService


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent), suffix=".tmp") as f:
        tmp = Path(f.name)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(str(tmp), str(path))


def test_pricing_fuzzy_match_and_max(tmp_path: Path):
    pricing_path = tmp_path / "pricing.json"
    _atomic_write(pricing_path, {"纸": 1.0, "纸箱": 2.0, "箱": 1.5})

    svc = PricingService(pricing_path)
    assert svc.get_price("纸箱") == 2.0
    assert svc.get_price("纸箱子") == 2.0
    assert svc.get_price("箱子") == 1.5
    assert svc.get_price("未知") == 0.0


def test_pricing_hot_reload_by_mtime(tmp_path: Path):
    pricing_path = tmp_path / "pricing.json"
    _atomic_write(pricing_path, {"纸箱": 1.0})

    svc = PricingService(pricing_path)
    assert svc.get_price("纸箱") == 1.0

    _atomic_write(pricing_path, {"纸箱": 3.5})
    assert svc.get_price("纸箱") == 3.5
