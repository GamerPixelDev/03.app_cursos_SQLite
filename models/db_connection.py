# models/db_connection.py
import os
import sys
import sqlite3
from contextlib import contextmanager

def get_app_dir():
    """
    Devuelve la ruta raíz donde buscar la carpeta 'data'.
    - Si se ejecuta como .exe, usa la carpeta del ejecutable.
    - Si no, usa la carpeta raíz del proyecto.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_DIR = get_app_dir()
EXTERNAL_DATA_DIR = os.path.join(APP_DIR, "data")  # carpeta real junto al .exe
INTERNAL_DATA_DIR = os.path.join(getattr(sys, '_MEIPASS', APP_DIR), "data")  # copia temporal del .exe

# Si existe la base externa, se usa esa (persistente).
# Si no, se usa la interna (solo lectura, empaquetada).
if os.path.exists(EXTERNAL_DATA_DIR):
    DATA_DIR = EXTERNAL_DATA_DIR
else:
    DATA_DIR = INTERNAL_DATA_DIR

DB_PATH = os.path.join(DATA_DIR, "database.db")

# Crear carpeta externa si no existe (para primera ejecución)
os.makedirs(EXTERNAL_DATA_DIR, exist_ok=True)

def _connect():
    """Abre conexión SQLite con la base de datos persistente."""
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_connection():
    """Maneja la conexión automáticamente con commit/rollback."""
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
