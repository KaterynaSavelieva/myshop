# sale.py
"""
Генератор продажів:
- випадковий клієнт
- товари тільки з додатнім залишком (lagerbestand > 0)
- безпечне списання складу (WHERE lagerbestand >= qty)
- ціна продажу: остання закупка (einkauf_artikel.einkaufspreis) + націнка 10..50%
  (якщо закупки не було – беремо artikel.preis)
- знижка на позицію: 0 / 5 / 10 %
- транзакція, відкат шапки, якщо жодної позиції не вдалося вставити
"""

import random
from datetime import datetime, timedelta
from db import get_conn, fetch_all, fetch_one

# Параметри генерації
MIN_LINES = 1              # мінімум різних товарів у чеку
MAX_LINES = 3              # максимум різних товарів у чеку
SALE_QTY_MAX = 5           # максимум штук одного товару
MARGIN_MIN = 0.10          # мінімальна націнка (10%)
MARGIN_MAX = 0.50          # максимальна націнка (50%)
DISCOUNT_CHOICES = [0, 0, 0, 5, 10]  # частіше без знижки


def last_purchase_price(cur, artikel_id):
    """
    Повертає останню закупівельну ціну (float) або None, якщо закупок не було.
    """
    row = fetch_one(
        cur,
        """
        SELECT ea.einkaufspreis
        FROM einkauf_artikel ea
        JOIN einkauf e ON e.einkauf_id = ea.einkauf_id
        WHERE ea.artikel_id = %s
        ORDER BY e.datum DESC, ea.einkauf_id DESC
        LIMIT 1
        """,
        (artikel_id,)
    )
    return float(row[0]) if row else None


def create_sale():
    conn = get_conn()
    if conn is None:
        print("❌ Немає підключення до БД.")
        return

    cur = conn.cursor()
    try:
        # 1) випадковий клієнт
        kunden = fetch_all(cur, "SELECT kunden_id FROM kunden")
        if not kunden:
            print("❌ Немає клієнтів — спочатку заповни таблицю 'kunden'.")
            return
        kunden_id = random.choice(kunden)[0]

        # 2) товари з додатнім залишком
        artikels = fetch_all(
            cur, "SELECT artikel_id, lagerbestand FROM artikel WHERE lagerbestand > 0"
        )
        if not artikels:
            print("ℹ️ Немає товарів на складі — спочатку зроби закупку.")
            return

        # 3) створюємо шапку продажу (час трохи випадковий у межах 2 годин)
        cur.execute(
            "INSERT INTO verkauf (kunden_id, datum) VALUES (%s, %s)",
            (kunden_id, datetime.now() - timedelta(minutes=random.randint(0, 120))),
        )
        verkauf_id = cur.lastrowid

        # 4) формуємо позиції
        picked = random.sample(
            artikels, k=min(random.randint(MIN_LINES, MAX_LINES), len(artikels))
        )
        inserted = 0

        for art_id, stock in picked:
            if stock <= 0:
                continue

            qty = random.randint(1, min(SALE_QTY_MAX, int(stock)))

            # безпечне списання складу
            cur.execute(
                """
                UPDATE artikel
                   SET lagerbestand = lagerbestand - %s
                 WHERE artikel_id = %s
                   AND lagerbestand >= %s
                """,
                (qty, art_id, qty),
            )
            if cur.rowcount == 0:
                # не вистачило прямо зараз — пропускаємо позицію
                continue

            # базова ціна: остання закупка або artikel.preis
            ek_preis = last_purchase_price(cur, art_id)
            if ek_preis is None:
                ek_preis = fetch_one(
                    cur, "SELECT preis FROM artikel WHERE artikel_id = %s", (art_id,)
                )[0]

            # важливо: привести до float, щоб уникнути помилок Decimal * float
            ek_preis = float(ek_preis)

            margin = float(random.uniform(MARGIN_MIN, MARGIN_MAX))
            verkaufspreis = round(ek_preis * (1 + margin), 2)
            rabatt = int(random.choice(DISCOUNT_CHOICES))

            # вставляємо позицію з ціною та знижкою
            cur.execute(
                """
                INSERT INTO verkauf_artikel
                    (verkauf_id, artikel_id, menge, verkaufspreis, rabatt_pct)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (verkauf_id, art_id, qty, verkaufspreis, rabatt),
            )
            inserted += 1

        # якщо нічого не продали — видаляємо шапку і фіксуємо відміну
        if inserted == 0:
            cur.execute("DELETE FROM verkauf WHERE verkauf_id = %s", (verkauf_id,))
            conn.commit()
            print("ℹ️ Продаж відмінено — не вдалося списати жодної позиції.")
            return

        conn.commit()
        print(f"✅ Verkauf #{verkauf_id} створено. Позицій: {inserted}.")
        print(f"Verkauf згенеровано: {datetime.now():%Y-%m-%d %H:%M:%S}")

    except Exception as e:
        conn.rollback()
        print("❌ Помилка при створенні продажу:", e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("=" * 70)
    print(f"🕒 Neuer Verkaufslauf gestartet um {datetime.now():%Y-%m-%d %H:%M:%S}")
    create_sale()
