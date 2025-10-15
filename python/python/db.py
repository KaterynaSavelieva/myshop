# просте підключення (поточна функція для імпорту)

import os
from dotenv import load_dotenv
import mysql.connector

# читаємо .env з кореня репозиторію
load_dotenv()

def get_conn():
    """
    Повертає з'єднання з MariaDB / MySQL, налаштоване стабільно для Windows.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        auth_plugin="mysql_native_password",
        use_pure=True,             # важливо для стабільності на нових Python
        connection_timeout=5
    )
