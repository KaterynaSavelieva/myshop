from db import get_conn

conn = get_conn()
if conn:
    print("✅ Підключення успішне!")
    conn.close()
else:
    print("❌ Не вдалося підключитись до бази.")
