from fastapi import APIRouter, Depends, File, UploadFile
import sqlite3

from app.api import auth, history, listings, users
from app.api.deps import UserRow, get_optional_user
from app.core.config import settings
from app.core.db import get_db, utc_now_iso
from app.core.errors import AppError
from app.services.pricing import PricingService
from app.services.recognizer.factory import get_recognizer

router = APIRouter(prefix="/api")

_pricing = PricingService(settings.pricing_path)

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(history.router)
router.include_router(listings.router)


@router.post("/recognize")
def recognize(
    file: UploadFile = File(...),
    db: sqlite3.Connection = Depends(get_db),
    user: UserRow | None = Depends(get_optional_user),
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
    price = _pricing.get_price(item)
    if user:
        db.execute(
            "INSERT INTO recognition_history(user_id, item, price, currency, created_at) VALUES(?,?,?,?,?)",
            (int(user["id"]), item, float(price), "CNY", utc_now_iso()),
        )
        db.commit()
    return {"item": item, "price": float(price), "currency": "CNY"}
