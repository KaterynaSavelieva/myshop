"""
Генератор закупок:
- створює шапку закупки в `einkauf`
- додає 1..5 позицій у `einkauf_artikel`
- ціна береться з artikel_lieferant (для вибраного постачальника)
- склади збільшуються відразу (UPDATE artikel.lagerbestand = lagerbestand + qty)
"""

import random
from datetime import datetime
from db import get_conn, fetch_all, fetch_one

# параметри генерації
MIN_LINES = 1
MAX_LINES = 5
QTY_RANGE = (20, 120)  # скільки штук на позицію
SUPPLIER_HINT = None   # якщо хочеш примусово постачальника: наприклад 4, або None для випадкового

def create_purchase():
    conn = get_conn()
    cur = conn.cursor()

    try:
        # 1) список постачальників
        lieferanten = fetch_all(cur, "SELECT lieferant_id FROM lieferanten")
        if not lieferanten:
            print("Немає постачальників.")
            return
        if SUPPLIER_HINT:
            lieferant_id = SUPPLIER_HINT
        else:
            lieferant_id = random.choice(lieferanten)[0]

        # 2) створюємо шапку закупки
        cur.execute(
            "INSERT INTO einkauf (lieferant_id, einkauf_datum, rechnung_nr, bemerkung) "
            "VALUES (%s, NOW(), %s, %s)",
            (lieferant_id, f"EK-{datetime.now():%Y%m%d-%H%M%S}", "Auto-generator")
        )
        einkauf_id = cur.lastrowid

        # 3) перелік товарів, які цей постачальник може постачати (з цінами)
        artikel_preise = fetch_all(
            cur,
            "SELECT al.artikel_id, al.einkaufspreis "
            "FROM artikel_lieferant al "
            "WHERE al.lieferant_id = %s",
            (lieferant_id,)
        )
        if not artikel_preise:
            raise RuntimeError(f"У постачальника {lieferant_id} немає прив’язаних товарів у artikel_lieferant.")

        # вибираємо 1..5 унікальних товарів
        lines = random.sample(artikel_preise, k=min(random.randint(MIN_LINES, MAX_LINES), len(artikel_preise)))

        inserted = 0
        for art_id, ek_preis in lines:
            qty = random.randint(*QTY_RANGE)

            # додаємо позицію закупки
            cur.execute(
                "INSERT INTO einkauf_artikel (einkauf_id, artikel_id, einkauf_menge, einkaufspreis) "
                "VALUES (%s, %s, %s, %s)",
                (einkauf_id, art_id, qty, ek_preis)
            )

            # збільшуємо склад
            cur.execute(
                "UPDATE artikel SET lagerbestand = lagerbestand + %s WHERE artikel_id = %s",
                (qty, art_id)
            )
            inserted += 1

        if inserted == 0:
            raise RuntimeError("Жодної позиції не додано — скасовую закупку.")

        conn.commit()
        print(f"Einkauf #{einkauf_id} створено. Позицій: {inserted}. Lieferant: {lieferant_id}.")
        print(f"Einkauf згенеровано: {datetime.now():%Y-%m-%d %H:%M:%S}")
    except Exception as e:
        conn.rollback()
        print("Помилка при створенні закупки:", e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("="*70)
    print(f"🕒 Neuer Einkauf gestartet um {datetime.now():%Y-%m-%d %H:%M:%S}")
    create_purchase()
