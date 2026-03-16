import json
import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile


def update_price(pricing_path: Path, keyword: str, price: float) -> None:
    keyword = (keyword or "").strip()
    if not keyword:
        raise ValueError("keyword 不能为空")
    if not isinstance(price, (int, float)) or not (price >= 0):
        raise ValueError("price 必须为非负数")

    pricing_path.parent.mkdir(parents=True, exist_ok=True)
    if pricing_path.exists():
        data = json.loads(pricing_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            data = {}
    else:
        data = {}

    data[keyword] = float(price)

    with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(pricing_path.parent), suffix=".tmp") as f:
        tmp_path = Path(f.name)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    os.replace(str(tmp_path), str(pricing_path))


def _main(argv: list[str]) -> int:
    if len(argv) != 3:
        sys.stderr.write("Usage: python scripts/update-price.py <keyword> <price>\n")
        return 2

    keyword = argv[1]
    try:
        price = float(argv[2])
    except Exception:
        sys.stderr.write("price 必须为数字\n")
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    pricing_path = (repo_root / "shared" / "pricing.json").resolve()

    try:
        update_price(pricing_path, keyword, price)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        return 1

    sys.stdout.write(f"Updated {keyword} => {price:.2f}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
