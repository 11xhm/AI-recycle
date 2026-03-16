from pydantic import BaseModel
from fastapi import APIRouter, Depends
import sqlite3

from app.core.db import get_db
from app.core.db import utc_now_iso
from app.core.errors import AppError
from app.services.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    username: str
    password: str
    display_name: str | None = None


class LoginIn(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(payload: RegisterIn, db: sqlite3.Connection = Depends(get_db)):
    username = payload.username.strip()
    if not username or len(username) < 3:
        raise AppError.invalid_request("用户名至少 3 位")

    existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if existing:
        raise AppError.conflict("用户名已存在")

    display_name = (payload.display_name or "").strip()
    pwd_hash = hash_password(payload.password)
    created_at = utc_now_iso()
    cur = db.execute(
        "INSERT INTO users(username, password_hash, display_name, created_at) VALUES(?,?,?,?)",
        (username, pwd_hash, display_name, created_at),
    )
    db.commit()
    user_id = int(cur.lastrowid)
    token = create_access_token(user_id, username)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(payload: LoginIn, db: sqlite3.Connection = Depends(get_db)):
    username = payload.username.strip()
    row = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if not row or not verify_password(payload.password, row["password_hash"]):
        raise AppError.unauthorized("用户名或密码错误")
    token = create_access_token(int(row["id"]), str(row["username"]))
    return {"access_token": token, "token_type": "bearer"}

