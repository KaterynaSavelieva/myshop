# app/db.py
import os
from pathlib import Path
from typing import Iterable, Optional, Tuple, Any, List

import pymysql
from dotenv import load_dotenv

# .env лежить у корені репозиторію (папка myshop)
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)

def _hosts() -> Iterable[str]:
    """Читаємо DB_HOSTS або DB_HOST; підтримка кількох хостів через кому."""
    hosts = os.getenv("DB_HOSTS") or os.getenv("DB_HOST") or "localhost"
    return [h.strip() for h in hosts.split(",") if h.strip()]

def get_conn() -> Optional[pymysql.connections.Connection]:
    """Пробуємо під’єднатись до кожного хоста послідовно."""
    for host in _hosts():
        try:
            return pymysql.connect(
                host=host,
                user=os.getenv("DB_USER", "kateryna"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "myshopdb"),
                charset="utf8mb4",
                autocommit=False,
                cursorclass=pymysql.cursors.DictCursor,  # словники з ключами-колонками
            )
        except Exception:
            continue
    return None

def fetch_all(cur, sql: str, params: Tuple[Any, ...] = ()) -> List[dict]:
    cur.execute(sql, params)
    return cur.fetchall()

def fetch_one(cur, sql: str, params: Tuple[Any, ...] = ()) -> Optional[dict]:
    cur.execute(sql, params)
    return cur.fetchone()
