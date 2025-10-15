import os, traceback
import mysql.connector
from dotenv import load_dotenv

def main():
    load_dotenv()

    cfg = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": 3306,
        "auth_plugin": "mysql_native_password",
        "connection_timeout": 5,
        "use_pure": True,   # стабільніший конектор
    }

    # показати, що саме підставилося (без пароля)
    dbg = dict(cfg); dbg["password"] = "***"
    print("CFG:", dbg)

    print("🔌 Connecting...")
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**cfg)
        cur = conn.cursor()
        print("✅ Connected!")
        print("Current DB:", conn.database)

        # очистка (без FK конфліктів)
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        for t in ("verkauf_artikel", "verkauf", "kunden", "artikel"):
            cur.execute(f"DELETE FROM {t};")
            # опціонально скинути лічильник
            cur.execute(f"ALTER TABLE {t} AUTO_INCREMENT = 1;")
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()

        # -----------------------------
        # вставка тестових даних
        # -----------------------------
        print("Inserting test data…")

        # 1) товари
        cur.executemany(
            "INSERT INTO artikel (name, preis) VALUES (%s, %s);",
            [("Apfel", 0.99), ("Banane", 1.10)]
        )
        conn.commit()

        # мапа назв → id для зручності
        cur.execute("SELECT artikel_id, name FROM artikel;")
        artikel_map = {name: aid for (aid, name) in cur.fetchall()}

        # 2) покупець
        cur.execute(
            "INSERT INTO kunden (vorname, nachname, email, telefon) "
            "VALUES (%s, %s, %s, %s);",
            ("Anna", "Müller", "anna@example.com", "0660123456")
        )
        kunde_id = cur.lastrowid
        conn.commit()

        # 3) продаж (шапка)
        cur.execute(
            "INSERT INTO verkauf (kunden_id, datum) VALUES (%s, NOW());",
            (kunde_id,)
        )
        verkauf_id = cur.lastrowid
        conn.commit()

        # 4) позиції продажу
        cur.executemany(
            "INSERT INTO verkauf_artikel (verkauf_id, artikel_id, menge) "
            "VALUES (%s, %s, %s);",
            [
                (verkauf_id, artikel_map["Apfel"], 2),
                (verkauf_id, artikel_map["Banane"], 3),
            ]
        )
        conn.commit()

        print("Data inserted successfully!")

        # -----------------------------
        # SELECT-перевірка
        # -----------------------------
        print("\n🧾 Verkaufsdaten:")
        cur.execute("""
            SELECT k.vorname AS kunde,
                   a.name    AS artikel,
                   v.datum,
                   va.menge
            FROM verkauf v
            JOIN kunden k           ON v.kunden_id   = k.kunden_id
            JOIN verkauf_artikel va ON v.verkauf_id  = va.verkauf_id
            JOIN artikel a          ON va.artikel_id = a.artikel_id
            ORDER BY v.verkauf_id, a.artikel_id;
        """)
        for row in cur.fetchall():
            print(row)

    except Exception as e:
        print(" Fehler:", repr(e))
        traceback.print_exc()
    finally:
        try:
            if cur: cur.close()
            if conn: conn.close()
        except Exception:
            pass
        print("Verbindung geschlossen.")

if __name__ == "__main__":
    main()
