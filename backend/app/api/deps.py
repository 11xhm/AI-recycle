import sqlite3

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.db import get_db
from app.core.errors import AppError
from app.services.auth import decode_access_token

_bearer = HTTPBearer(auto_error=False)

UserRow = dict


def _get_user(db: sqlite3.Connection, user_id: int) -> UserRow | None:
    row = db.execute(
        "SELECT id, username, display_name, password_hash, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if not row:
        return None
    return dict(row)


def get_optional_user(
    db: sqlite3.Connection = Depends(get_db), creds: HTTPAuthorizationCredentials | None = Depends(_bearer)
) -> UserRow | None:
    if creds is None or not creds.credentials:
        return None
    payload = decode_access_token(creds.credentials)
    user_id = payload.get("sub")
    if not user_id:
        return None
    return _get_user(db, int(user_id))


def get_current_user(
    db: sqlite3.Connection = Depends(get_db), creds: HTTPAuthorizationCredentials | None = Depends(_bearer)
) -> UserRow:
    if creds is None or not creds.credentials:
        raise AppError.unauthorized()
    payload = decode_access_token(creds.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise AppError.unauthorized()
    user = _get_user(db, int(user_id))
    if user is None:
        raise AppError.unauthorized()
    return user
