# models/debug_ruta_db.py
from models.db_connection import DB_PATH
import os

print("Ruta actual de la base de datos:")
print(DB_PATH)
print("¿Existe el archivo?:", os.path.exists(DB_PATH))
input("\nPulsa Enter para salir...")
