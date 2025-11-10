from models.db_connection import DB_PATH
import sqlite3, os

print("Ruta real que está usando la app:")
print(DB_PATH)
print("¿Existe?:", os.path.exists(DB_PATH))

if os.path.exists(DB_PATH):
    print("Tamaño:", os.path.getsize(DB_PATH), "bytes")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tablas disponibles:", cur.fetchall())
        cur.execute("SELECT usuario, rol FROM usuarios;")
        print("Usuarios:", cur.fetchall())
    except Exception as e:
        print("Error al leer:", e)
    finally:
        conn.close()
input("Pulsa Enter para salir...")
