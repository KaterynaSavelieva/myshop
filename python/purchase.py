# створює одну закупку (простий варіант)
import random
from datetime import datetime
from db import get_conn

def create_purchase():
    conn = get_conn()
    cur = conn.cursor()

    try:
        # 1) вибрати випадкового постачальника
        cur.execute("SELECT lieferant_id FROM lieferanten")
        liefer = cur.fetchall()
        if not liefer:
            print("Немає постачальників.")
            return
        lieferant_id = random.choice(liefer)[0]

        # 2) вибрати декілька товарів з каталогу
        cur.execute("SELECT artikel_id, preis FROM artikel")
        artikels = cur.fetchall()
        if not artikels:
            print("Немає товарів у таблиці artikel.")
            return

        # 1..3 різні товари
        chosen = random.sample(artikels, k=min(3, len(artikels)))

        # 3) шапка закупки
        rechnung = f"EK-{int(datetime.now().timestamp())}"
        bemerkung = "Auto"
        cur.execute(
            "INSERT INTO einkauf (lieferant_id, datum, rechnung_nr, bemerkung) "
            "VALUES (%s, NOW(), %s, %s)",
            (lieferant_id, rechnung, bemerkung)
        )
        einkauf_id = cur.lastrowid

        # 4) позиції закупки + оновлення складу
        for art_id, verkaufspreis in chosen:
            menge = random.randint(3, 20)  # скільки прийшло
            # закупівельна ціна – нижча, ніж продажна
            ek_preis = round(float(verkaufspreis) * random.uniform(0.5, 0.9), 2)

            # вставка позиції
            cur.execute(
                "INSERT INTO einkauf_artikel (einkauf_id, artikel_id, menge, einkaufspreis) "
                "VALUES (%s, %s, %s, %s)",
                (einkauf_id, art_id, menge, ek_preis)
            )

            # збільшити залишок
            cur.execute(
                "UPDATE artikel SET lagerbestand = lagerbestand + %s WHERE artikel_id = %s",
                (menge, art_id)
            )

        conn.commit()
        print(f"✅ Закупка #{einkauf_id} створена. Позицій: {len(chosen)}.")

    except Exception as e:
        conn.rollback()
        print("❌ Помилка під час закупки:", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_purchase()
