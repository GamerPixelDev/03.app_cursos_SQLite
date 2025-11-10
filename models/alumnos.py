# models/alumnos.py
import sqlite3
from models.db_connection import get_connection
from models.utils_db import manejar_error_db

# Columnas permitidas para UPDATE (whitelist)
CAMPOS_ALUMNO = {
    "nombre", "apellidos", "localidad", "codigo_postal",
    "telefono", "email", "sexo", "edad", "estudios", "estado_laboral"
}

# === Crear alumno ===
def crear_alumno(nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            # ¿Existe ya?
            cur.execute("SELECT COUNT(*) FROM alumnos WHERE nif = ?", (nif,))
            if cur.fetchone()[0] > 0:
                print(f"⚠️  El alumno con NIF {nif} ya existe.")
                return False
            # Insert
            cur.execute("""
                INSERT INTO alumnos
                    (nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nif, nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral))
        print(f"✅ Alumno {nombre} {apellidos} añadido correctamente.")
        return True
    except Exception as e:
        manejar_error_db(e, "crear alumno")
        return False

# === Obtener todos los alumnos ===
def obtener_alumnos():
    #Recupera todos los registros de alumnos ordenados por apellidos y nombre.
    #Devuelve una lista de filas (sqlite3.Row), indexables por nombre o posición.
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM alumnos ORDER BY apellidos, nombre")
            alumnos = cur.fetchall()
            print(f"📋 {len(alumnos)} alumnos recuperados.")
            return alumnos
    except Exception as e:
        manejar_error_db(e, "obtener alumnos")
        return []

# === Eliminar alumno por NIF ===
def eliminar_alumno(nif_alumno):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM alumnos WHERE nif = ?", (nif_alumno,))
        print(f"🗑️ Alumno con NIF {nif_alumno} eliminado.")
    except Exception as e:
        manejar_error_db(e, "eliminar alumno")

# === Actualizar alumno ===
def actualizar_alumno(nif_alumno, campo, nuevo_valor):
    #Actualiza un campo específico del alumno identificado por su NIF.
    #'campo' debe estar en la whitelist CAMPOS_ALUMNO para evitar inyección SQL.
    if campo not in CAMPOS_ALUMNO:
        print(f"❌ Campo no permitido: {campo}")
        return
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            # No se pueden usar placeholders para nombres de columna: validamos y formateamos.
            sql = f"UPDATE alumnos SET {campo} = ? WHERE nif = ?"
            cur.execute(sql, (nuevo_valor, nif_alumno))
        print(f"✏️ Alumno {nif_alumno} actualizado: {campo} = {nuevo_valor}")
    except Exception as e:
        manejar_error_db(e, "actualizar alumno")

# === Obtener datos de un alumno ===
def obtener_datos_alumno(nif):
    #Devuelve los datos detallados de un alumno según su NIF.
    #Si no existe, devuelve None.
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT nombre, apellidos, localidad, codigo_postal, telefono, email, sexo, edad, estudios, estado_laboral
                FROM alumnos
                WHERE nif = ?
            """, (nif,))
            datos = cur.fetchone()
            if datos:
                print(f"👤 Datos obtenidos para NIF {nif}.")
            else:
                print(f"⚠️ No se encontró el alumno con NIF {nif}.")
            return datos
    except Exception as e:
        manejar_error_db(e, "obtener datos de un alumno")
        return None
