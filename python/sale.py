# створює один продаж (простий варіант)
import random
from db import get_conn

def create_sale():
    conn = get_conn()
    cur = conn.cursor()

    try:
        # 1) випадковий клієнт
        cur.execute("SELECT kunden_id FROM kunden")
        kunden = cur.fetchall()
        if not kunden:
            print("Немає клієнтів.")
            return
        kunden_id = random.choice(kunden)[0]

        # 2) товари з додатнім залишком
        cur.execute("SELECT artikel_id, preis, lagerbestand FROM artikel WHERE lagerbestand > 0")
        artikels = cur.fetchall()
        if not artikels:
            print("Немає товарів з доступним залишком.")
            return

        # 3) шапка продажу
        cur.execute(
            "INSERT INTO verkauf (kunden_id, datum) VALUES (%s, NOW())",
            (kunden_id,)
        )
        verkauf_id = cur.lastrowid

        # 4) 1..3 позиції (тільки з наявних)
        items_to_sell = random.sample(artikels, k=min(3, len(artikels)))

        for art_id, preis, lager in items_to_sell:
            if lager <= 0:
                continue

            qty = random.randint(1, min(5, int(lager)))

            # безпечно зменшуємо залишок (умова AND lagerbestand >= qty)
            cur.execute(
                "UPDATE artikel SET lagerbestand = lagerbestand - %s "
                "WHERE artikel_id = %s AND lagerbestand >= %s",
                (qty, art_id, qty)
            )
            if cur.rowcount == 0:
                # не вистачило товару саме зараз
                raise RuntimeError(f"Недостатній залишок для artikel_id={art_id}")

            # запис у таблицю зв'язку
            cur.execute(
                "INSERT INTO verkauf_artikel (verkauf_id, artikel_id, menge) "
                "VALUES (%s, %s, %s)",
                (verkauf_id, art_id, qty)
            )

        conn.commit()
        print(f"✅ Продаж #{verkauf_id} створено.")

    except Exception as e:
        conn.rollback()
        print("❌ Помилка при створенні продажу:", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_sale()
