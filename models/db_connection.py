# models/db_connection.py
import os
import sys
import sqlite3
from contextlib import contextmanager

def get_app_dir():
    if getattr(sys, 'frozen', False):  # ejecutándose como .exe
        return os.path.dirname(os.path.abspath(sys.executable))
    else:  # ejecutándose como script normal
        return os.path.dirname(os.path.abspath(__file__))

# === CONFIGURACIÓN DE LA BASE DE DATOS ===
APP_DIR = get_app_dir()
DATA_DIR = os.path.join(APP_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "database.db")

# Crea la carpeta 'data' si no existe
os.makedirs(DATA_DIR, exist_ok=True)

def _connect():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # permite acceder por nombre de columna
    conn.execute("PRAGMA foreign_keys = ON;")  # activa claves foráneas
    return conn

@contextmanager
def get_connection():
    """
    Context manager para abrir y cerrar la conexión automáticamente.
    Hace commit si todo va bien, rollback si hay error.
    """
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()