# models/db_connection.py
import os
import sys
import sqlite3

def get_app_dir():
    # Si es .exe -> carpeta del ejecutable; si no, raíz del proyecto
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_DIR = get_app_dir()
DATA_DIR = os.path.join(APP_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "database.db")

# Asegura que la carpeta 'data' exista
os.makedirs(DATA_DIR, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
