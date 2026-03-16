from pydantic import BaseModel
from fastapi import APIRouter, Depends
import sqlite3

from app.api.deps import UserRow, get_current_user
from app.core.db import get_db

router = APIRouter(prefix="", tags=["users"])


@router.get("/me")
def me(user: UserRow = Depends(get_current_user)):
    return {
        "id": user["id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "created_at": user["created_at"],
    }


class UpdateMeIn(BaseModel):
    display_name: str


@router.patch("/me")
def update_me(payload: UpdateMeIn, db: sqlite3.Connection = Depends(get_db), user: UserRow = Depends(get_current_user)):
    display_name = payload.display_name.strip()
    db.execute("UPDATE users SET display_name = ? WHERE id = ?", (display_name, int(user["id"])))
    db.commit()
    return {"ok": True}

