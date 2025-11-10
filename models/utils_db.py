import sqlite3
from tkinter import messagebox

def manejar_error_db(e, accion="operación en la base de datos"):
    if isinstance(e, sqlite3.OperationalError):
        messagebox.showerror("Error de conexión", "⚠️ No se pudo completar la operación con la base de datos.\nRevisa el esquema/consulta.")
    elif isinstance(e, sqlite3.IntegrityError):
        messagebox.showwarning("Dato duplicado/conflicto", "Este registro vulnera una restricción (¿único/foránea?).")
    else:
        messagebox.showerror("Error", f"❌ Error durante {accion}:\n{e}")
