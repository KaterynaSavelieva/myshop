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
    Пробує всі IP з DB_HOSTS по черзі.
    """
    hosts = os.getenv("DB_HOSTS", "localhost").split(",")

    for host in hosts:
        host = host.strip()
        try:
            conn = pymysql.connect(
                host=host,
                user=os.getenv("DB_USER", "kateryna"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "myshopdb"),
                charset="utf8mb4",
                autocommit=False,
                cursorclass=Cursor,
                connect_timeout=3
            )
            print(f"✅ Підключення успішне: {host}")
            return conn

        except Exception as e:
            print(f"⚠️ Не вдалося підключитись до {host}: {e}")

    print("❌ Не вдалося підключитись до жодного сервера.")
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
        print("✅ База даних доступна!")
        conn.close()
    else:
        print("❌ Підключення відсутнє.")
