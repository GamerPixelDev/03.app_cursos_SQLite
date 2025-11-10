# models/logs.py
from models.db_connection import get_connection

def registrar_evento(usuario, accion, detalle=""):
    #Registra un evento en la tabla logs.
    #Si la tabla no existe, se crea automáticamente.
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            # Crear tabla si no existe (solo la primera vez)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    accion TEXT,
                    detalle TEXT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Insertar evento
            cur.execute(
                "INSERT INTO logs (usuario, accion, detalle) VALUES (?, ?, ?)",
                (usuario, accion, detalle)
            )
        print(f"🪶 Log registrado: {usuario} - {accion}")
    except Exception as e:
        print(f"⚠️ Error al registrar log: {e}")

def obtener_logs(limit=100):
    #Devuelve los últimos 'limit' registros de logs ordenados por fecha descendente.
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT usuario, accion, detalle, fecha FROM logs ORDER BY fecha DESC LIMIT ?",
                (limit,)
            )
            datos = cur.fetchall()
        print(f"📜 {len(datos)} logs recuperados.")
        return datos
    except Exception as e:
        print(f"⚠️ Error al obtener logs: {e}")
        return []