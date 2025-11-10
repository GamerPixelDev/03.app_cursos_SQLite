import os
import sqlite3
from contextlib import contextmanager

# Ruta a data/database.db (junto al repo)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "database.db")

os.makedirs(DATA_DIR, exist_ok=True)

def _connect():
    # check_same_thread=False si usas hilos (Tkinter a veces lo agradece)
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    # rows por nombre de columna
    conn.row_factory = sqlite3.Row
    # activar integridad referencial
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_connection():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
