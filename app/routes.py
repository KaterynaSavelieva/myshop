# app/routes.py
from flask import Blueprint, render_template
from app.db import get_conn

bp = Blueprint("main", __name__)

@bp.get("/health")
def health():
    return {"status": "ok"}

@bp.get("/")
def home():
    rows = []
    conn = get_conn()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT v.verkauf_id,
                       v.verkauf_datum AS verkauf_datum,           -- <- правильна колонка
                       CONCAT(k.nachname, ' ', k.vorname) AS kunde
                FROM verkauf v
                JOIN kunden k ON v.kunden_id = k.kunden_id
                ORDER BY v.verkauf_datum DESC
                LIMIT 10
            """)
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

    return render_template("index.html", sales=rows)
