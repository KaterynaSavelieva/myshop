# app/routes.py
from flask import Blueprint, render_template, request
from app.db import get_conn, fetch_all
from app import require_auth

bp = Blueprint("main", __name__)

@bp.get("/health")
def health():
    return {"status": "ok"}

@bp.get("/")
@require_auth
def home():
    # фільтри з URL: ?from=2025-10-01&to=2025-10-20&kunde=11&limit=20
    date_from = request.args.get("from")
    date_to   = request.args.get("to")
    kunde_id  = request.args.get("kunde", type=int)
    limit     = request.args.get("limit", default=10, type=int)
    limit = max(1, min(limit, 100))  # обмежуємо 1..100

    where = []
    params = []

    if date_from:
        where.append("v.verkauf_datum >= %s")
        params.append(date_from)
    if date_to:
        where.append("v.verkauf_datum <= %s")
        params.append(date_to)
    if kunde_id:
        where.append("v.kunden_id = %s")
        params.append(kunde_id)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    sql = f"""
        SELECT v.verkauf_id,
               v.verkauf_datum,
               CONCAT(k.nachname, ', ', k.vorname) AS kunde
        FROM verkauf v
        JOIN kunden k ON v.kunden_id = k.kunden_id
        {where_sql}
        ORDER BY v.verkauf_datum DESC
        LIMIT %s
    """
    params.append(limit)

    rows = []
    conn = get_conn()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

    return render_template("index.html", sales=rows)
