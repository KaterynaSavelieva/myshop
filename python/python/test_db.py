from db import get_conn

def main():
    try:
        cn = get_conn()
        cur = cn.cursor()
        cur.execute("SELECT DATABASE(), VERSION()")
        print("DB OK:", cur.fetchone())
        cur.close(); cn.close()
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    main()
