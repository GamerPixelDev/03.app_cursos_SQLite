# models/cursos.py
from models.db_connection import get_connection
from models.utils_db import manejar_error_db

# Campos válidos que pueden actualizarse (para evitar inyección SQL)
CAMPOS_CURSO = {
    "nombre", "fecha_inicio", "fecha_fin", "lugar",
    "modalidad", "horas", "responsable"
}

# === Crear curso ===
def crear_curso(codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM cursos WHERE codigo_curso = ?", (codigo_curso,))
            if cur.fetchone()[0] > 0:
                print(f"⚠️  El curso con código {codigo_curso} ya existe.")
                return False
            cur.execute("""
                INSERT INTO cursos (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (codigo_curso, nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable))
        print(f"✅ Curso '{nombre}' creado correctamente.")
        return True
    except Exception as e:
        manejar_error_db(e, "crear curso")
        return False

# === Obtener todos los cursos ===
def obtener_cursos():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM cursos ORDER BY codigo_curso DESC")
            datos = cur.fetchall()
            print(f"📋 {len(datos)} cursos recuperados.")
            return datos
    except Exception as e:
        manejar_error_db(e, "obtener cursos")
        return []

# === Eliminar curso por código ===
def eliminar_curso(codigo_curso):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM cursos WHERE codigo_curso = ?", (codigo_curso,))
        print(f"🗑️ Curso con código {codigo_curso} eliminado correctamente.")
    except Exception as e:
        manejar_error_db(e, "eliminar curso")

# === Actualizar curso ===
def actualizar_curso(codigo_curso, campo, nuevo_valor):
    if campo not in CAMPOS_CURSO:
        print(f"❌ Campo no permitido: {campo}")
        return
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"UPDATE cursos SET {campo} = ? WHERE codigo_curso = ?"
            cur.execute(sql, (nuevo_valor, codigo_curso))
        print(f"✏️ Curso {codigo_curso} actualizado: {campo} = {nuevo_valor}")
    except Exception as e:
        manejar_error_db(e, "actualizar curso")

# === Obtener datos de un curso ===
def obtener_datos_curso(codigo_curso):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT nombre, fecha_inicio, fecha_fin, lugar, modalidad, horas, responsable
                FROM cursos
                WHERE codigo_curso = ?
            """, (codigo_curso,))
            datos = cur.fetchone()
            if datos:
                print(f"📚 Datos obtenidos para el curso {codigo_curso}.")
            else:
                print(f"⚠️ No se encontró el curso con código {codigo_curso}.")
            return datos
    except Exception as e:
        manejar_error_db(e, "obtener datos de un curso")
        return None