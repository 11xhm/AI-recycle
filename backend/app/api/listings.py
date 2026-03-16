import uuid
import sqlite3

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.api.deps import UserRow, get_current_user
from app.core.config import settings
from app.core.db import get_db, utc_now_iso
from app.core.errors import AppError
from app.services.pricing import PricingService
from app.services.recognizer.factory import get_recognizer

router = APIRouter(prefix="/listings", tags=["listings"])

_pricing = PricingService(settings.pricing_path)


def _save_upload(file: UploadFile, data: bytes) -> str:
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    ext = ""
    if file.content_type == "image/jpeg":
        ext = ".jpg"
    elif file.content_type == "image/png":
        ext = ".png"
    elif file.content_type == "image/webp":
        ext = ".webp"
    name = f"{uuid.uuid4().hex}{ext}"
    path = (settings.upload_dir / name).resolve()
    path.write_bytes(data)
    return f"/uploads/{name}"


@router.get("")
def list_listings(db: sqlite3.Connection = Depends(get_db), include_sold: bool = False):
    if include_sold:
        rows = db.execute(
            """
            SELECT l.*, u.username AS seller_username, u.display_name AS seller_display_name
            FROM listings l
            JOIN users u ON u.id = l.seller_id
            ORDER BY l.id DESC
            LIMIT 100
            """
        ).fetchall()
    else:
        rows = db.execute(
            """
            SELECT l.*, u.username AS seller_username, u.display_name AS seller_display_name
            FROM listings l
            JOIN users u ON u.id = l.seller_id
            WHERE l.is_sold = 0
            ORDER BY l.id DESC
            LIMIT 100
            """
        ).fetchall()

    return [
        {
            "id": r["id"],
            "item": r["item"],
            "description": r["description"],
            "price": r["price"],
            "currency": r["currency"],
            "image_url": r["image_url"],
            "is_sold": bool(r["is_sold"]),
            "created_at": r["created_at"],
            "seller": {"id": r["seller_id"], "display_name": r["seller_display_name"], "username": r["seller_username"]},
        }
        for r in rows
    ]


@router.get("/{listing_id}")
def get_listing(listing_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute(
        """
        SELECT l.*, u.username AS seller_username, u.display_name AS seller_display_name
        FROM listings l
        JOIN users u ON u.id = l.seller_id
        WHERE l.id = ?
        """,
        (listing_id,),
    ).fetchone()
    if not row:
        raise AppError.not_found("商品不存在")
    return {
        "id": row["id"],
        "item": row["item"],
        "description": row["description"],
        "price": row["price"],
        "currency": row["currency"],
        "image_url": row["image_url"],
        "is_sold": bool(row["is_sold"]),
        "created_at": row["created_at"],
        "seller": {"id": row["seller_id"], "display_name": row["seller_display_name"], "username": row["seller_username"]},
    }


@router.post("")
def create_listing(
    file: UploadFile = File(...),
    description: str = Form(""),
    price: str | None = Form(None),
    db: sqlite3.Connection = Depends(get_db),
    user: UserRow = Depends(get_current_user),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise AppError.unsupported_file("仅支持图片文件", details={"content_type": file.content_type})

    data = file.file.read()
    if not data:
        raise AppError.invalid_request("文件为空")
    if len(data) > settings.max_upload_bytes:
        raise AppError.invalid_request(
            "文件过大", details={"max_bytes": settings.max_upload_bytes, "size_bytes": len(data)}
        )

    recognizer = get_recognizer(settings)
    item = recognizer.recognize(image_bytes=data, content_type=file.content_type)
    default_price = _pricing.get_price(item)
    if price is None or not str(price).strip():
        final_price = float(default_price)
    else:
        try:
            final_price = float(str(price).strip())
        except Exception:
            raise AppError.invalid_request("价格格式不正确")
    if final_price < 0:
        raise AppError.invalid_request("价格不能为负数")

    image_url = _save_upload(file, data)
    created_at = utc_now_iso()

    cur = db.execute(
        "INSERT INTO listings(seller_id, item, description, price, currency, image_url, is_sold, buyer_id, created_at) VALUES(?,?,?,?,?,?,?,?,?)",
        (
            int(user["id"]),
            item,
            description.strip(),
            float(final_price),
            "CNY",
            image_url,
            0,
            None,
            created_at,
        ),
    )
    db.commit()
    listing_id = int(cur.lastrowid)
    return {
        "id": listing_id,
        "item": item,
        "description": description.strip(),
        "price": float(final_price),
        "currency": "CNY",
        "image_url": image_url,
        "is_sold": False,
        "created_at": created_at,
    }


@router.post("/{listing_id}/purchase")
def purchase(listing_id: int, db: sqlite3.Connection = Depends(get_db), user: UserRow = Depends(get_current_user)):
    uid = int(user["id"])
    row = db.execute(
        "SELECT id, seller_id, price, currency, is_sold FROM listings WHERE id = ?",
        (listing_id,),
    ).fetchone()
    if not row:
        raise AppError.not_found("商品不存在")
    if int(row["is_sold"]) == 1:
        raise AppError.conflict("商品已售出")
    if int(row["seller_id"]) == uid:
        raise AppError.invalid_request("不能购买自己发布的商品")

    try:
        db.execute("BEGIN")
        db.execute("UPDATE listings SET is_sold = 1, buyer_id = ? WHERE id = ? AND is_sold = 0", (uid, listing_id))
        cur = db.execute(
            "INSERT INTO orders(listing_id, buyer_id, price, currency, created_at) VALUES(?,?,?,?,?)",
            (listing_id, uid, float(row["price"]), str(row["currency"]), utc_now_iso()),
        )
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        raise AppError.conflict("商品已售出")

    return {"order_id": int(cur.lastrowid)}

