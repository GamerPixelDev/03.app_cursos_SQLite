from models.db_connection import DB_PATH
import os

print("Ruta actual de la base usada por login:")
print(DB_PATH)
print("¿Existe?:", os.path.exists(DB_PATH))
if os.path.exists(DB_PATH):
    print("Tamaño:", os.path.getsize(DB_PATH), "bytes")
input("Pulsa Enter para salir...")
