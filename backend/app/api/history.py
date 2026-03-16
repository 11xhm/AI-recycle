from fastapi import APIRouter, Depends
import sqlite3

from app.api.deps import UserRow, get_current_user
from app.core.db import get_db

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
def history(db: sqlite3.Connection = Depends(get_db), user: UserRow = Depends(get_current_user)):
    uid = int(user["id"])
    recognitions = db.execute(
        "SELECT id, item, price, currency, created_at FROM recognition_history WHERE user_id = ? ORDER BY id DESC LIMIT 50",
        (uid,),
    ).fetchall()

    purchases = db.execute(
        "SELECT id, listing_id, price, currency, created_at FROM orders WHERE buyer_id = ? ORDER BY id DESC LIMIT 50",
        (uid,),
    ).fetchall()

    sales = db.execute(
        """
        SELECT o.id, o.listing_id, o.price, o.currency, o.created_at
        FROM orders o
        JOIN listings l ON l.id = o.listing_id
        WHERE l.seller_id = ?
        ORDER BY o.id DESC
        LIMIT 50
        """,
        (uid,),
    ).fetchall()

    my_listings = db.execute(
        "SELECT id, item, description, price, currency, image_url, is_sold, created_at FROM listings WHERE seller_id = ? ORDER BY id DESC LIMIT 50",
        (uid,),
    ).fetchall()

    return {
        "recognitions": [
            {"id": r["id"], "item": r["item"], "price": r["price"], "currency": r["currency"], "created_at": r["created_at"]}
            for r in recognitions
        ],
        "purchases": [
            {
                "id": o["id"],
                "listing_id": o["listing_id"],
                "price": o["price"],
                "currency": o["currency"],
                "created_at": o["created_at"],
            }
            for o in purchases
        ],
        "sales": [
            {
                "id": o["id"],
                "listing_id": o["listing_id"],
                "price": o["price"],
                "currency": o["currency"],
                "created_at": o["created_at"],
            }
            for o in sales
        ],
        "my_listings": [
            {
                "id": l["id"],
                "item": l["item"],
                "description": l["description"],
                "price": l["price"],
                "currency": l["currency"],
                "image_url": l["image_url"],
                "is_sold": bool(l["is_sold"]),
                "created_at": l["created_at"],
            }
            for l in my_listings
        ],
    }

