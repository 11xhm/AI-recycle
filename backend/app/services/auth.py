from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import os

from jose import jwt, JWTError

from app.core.config import settings
from app.core.errors import AppError

_ALG = "HS256"
_PBKDF2_ITERS = 210_000


def hash_password(password: str) -> str:
    if not password or len(password) < 6:
        raise AppError.invalid_request("密码至少 6 位")
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERS)
    return "pbkdf2_sha256$%d$%s$%s" % (
        _PBKDF2_ITERS,
        base64.urlsafe_b64encode(salt).decode("ascii").rstrip("="),
        base64.urlsafe_b64encode(dk).decode("ascii").rstrip("="),
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        parts = (password_hash or "").split("$")
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            return False
        iters = int(parts[1])
        salt = base64.urlsafe_b64decode(parts[2] + "==")
        expected = base64.urlsafe_b64decode(parts[3] + "==")
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iters)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def create_access_token(user_id: int, username: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "username": username, "iat": int(now.timestamp()), "exp": exp}
    return jwt.encode(payload, settings.jwt_secret, algorithm=_ALG)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[_ALG])
    except JWTError:
        raise AppError.unauthorized("登录已失效")

