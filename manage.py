import argparse
from pathlib import Path

from scripts.update_price import update_price


def main() -> int:
    parser = argparse.ArgumentParser(prog="manage.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("update-price")
    p.add_argument("keyword", type=str)
    p.add_argument("price", type=float)

    args = parser.parse_args()

    if args.command == "update-price":
        repo_root = Path(__file__).resolve().parent
        pricing_path = (repo_root / "shared" / "pricing.json").resolve()
        update_price(pricing_path, args.keyword, args.price)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
