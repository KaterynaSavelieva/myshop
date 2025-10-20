# app/db.py
import os
import pymysql
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

def get_conn():
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "dashboard"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "myshopdb"),
            charset="utf8mb4",
            autocommit=False,
        )
    except Exception as e:
        print("DB connect error:", e)
        return None

def fetch_all(cur, sql, params=None):
    cur.execute(sql, params or ())
    return cur.fetchall()
