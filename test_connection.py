import os, sys, traceback
from dotenv import load_dotenv
import mysql.connector

print("Python:", sys.version)
print("mysql-connector-python:", mysql.connector.__version__)

load_dotenv()

cfg = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": 3306,
    "connection_timeout": 5,
    "auth_plugin": "mysql_native_password",
    "use_pure": True,              # <-- важливо: вимикає C-extension
    "raise_on_warnings": True,
    "get_warnings": True,
}

print("CFG:", {k: ("***" if k=="password" else v) for k,v in cfg.items()})

try:
    print("Connecting…")
    conn = mysql.connector.connect(**cfg)
    print("After connect()")           # маркер
    if conn.is_connected():
        print("✅ Verbunden!")
        cur = conn.cursor()
        cur.execute("SELECT DATABASE()")
        print("Current DB:", cur.fetchone()[0])
        cur.close()
    conn.close()
except Exception as e:
    print("Fehler:", repr(e))
    traceback.print_exc()
finally:
    print("Script finished")
