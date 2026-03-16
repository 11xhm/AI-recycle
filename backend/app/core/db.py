from collections.abc import Generator
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from app.core.config import settings


def _connect() -> sqlite3.Connection:
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(settings.db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables() -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE,
              password_hash TEXT NOT NULL,
              display_name TEXT NOT NULL DEFAULT '',
              created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS recognition_history (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              item TEXT NOT NULL,
              price REAL NOT NULL,
              currency TEXT NOT NULL DEFAULT 'CNY',
              created_at TEXT NOT NULL,
              FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS listings (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              seller_id INTEGER NOT NULL,
              item TEXT NOT NULL,
              description TEXT NOT NULL DEFAULT '',
              price REAL NOT NULL,
              currency TEXT NOT NULL DEFAULT 'CNY',
              image_url TEXT NOT NULL DEFAULT '',
              is_sold INTEGER NOT NULL DEFAULT 0,
              buyer_id INTEGER,
              created_at TEXT NOT NULL,
              FOREIGN KEY(seller_id) REFERENCES users(id),
              FOREIGN KEY(buyer_id) REFERENCES users(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              listing_id INTEGER NOT NULL UNIQUE,
              buyer_id INTEGER NOT NULL,
              price REAL NOT NULL,
              currency TEXT NOT NULL DEFAULT 'CNY',
              created_at TEXT NOT NULL,
              FOREIGN KEY(listing_id) REFERENCES listings(id),
              FOREIGN KEY(buyer_id) REFERENCES users(id)
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = _connect()
    try:
        yield conn
    finally:
        conn.close()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

