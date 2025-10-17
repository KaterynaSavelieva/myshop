# db.py
"""
Модуль для підключення до бази даних MySQL (MyShopDB)
та виконання простих SELECT-запитів.
"""

import os
import pymysql
from pymysql.cursors import Cursor
from dotenv import load_dotenv
from pathlib import Path


# 🔹 Завантажуємо .env (лежить у корені myshop)
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


def get_conn():
    """
    Створює та повертає підключення до бази даних.
    Дані беруться з .env або значення за замовчуванням.
    """
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "kateryna"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "myshopdb"),
            charset="utf8mb4",
            autocommit=False,
            cursorclass=Cursor  # якщо треба словники → DictCursor
        )
        return conn

    except Exception as e:
        print("❌ Помилка підключення до бази даних:", e)
        return None


def fetch_one(cur, sql, params=None):
    """Повертає один запис (tuple або None)."""
    cur.execute(sql, params or ())
    return cur.fetchone()


def fetch_all(cur, sql, params=None):
    """Повертає всі записи (список tuple)."""
    cur.execute(sql, params or ())
    return cur.fetchall()


if __name__ == "__main__":
    conn = get_conn()
    if conn:
        print("✅ Підключення успішне!")
        conn.close()
    else:
        print("❌ Не вдалося підключитись до бази.")
