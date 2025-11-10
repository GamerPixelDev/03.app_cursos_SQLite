# models/matriculas.py
from models.db_connection import get_connection
from models.utils_db import manejar_error_db
from datetime import datetime

# === Crear matrícula ===
def crear_matricula(nif_alumno, codigo_curso, fecha_matricula=None):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            if fecha_matricula is None:
                fecha_matricula = datetime.now().strftime("%Y-%m-%d")
            # ¿Ya está matriculado?
            cur.execute("""
                SELECT COUNT(*) FROM matriculas
                WHERE nif_alumno = ? AND codigo_curso = ?
            """, (nif_alumno, codigo_curso))
            if cur.fetchone()[0] > 0:
                print(f"⚠️  El alumno {nif_alumno} ya está matriculado en el curso {codigo_curso}.")
                return False
            # Insert
            cur.execute("""
                INSERT INTO matriculas (nif_alumno, codigo_curso, fecha_matricula)
                VALUES (?, ?, ?)
            """, (nif_alumno, codigo_curso, fecha_matricula))
        print(f"✅ Matrícula creada para alumno {nif_alumno} en el curso {codigo_curso}.")
        return True
    except Exception as e:
        manejar_error_db(e, "crear matrícula")
        return False

# === Obtener todas las matrículas ===
def obtener_matriculas():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    a.nif,
                    a.nombre || ' ' || a.apellidos AS alumno,
                    c.codigo_curso,
                    c.nombre AS curso,
                    m.fecha_matricula
                FROM matriculas m
                JOIN alumnos a ON m.nif_alumno = a.nif
                JOIN cursos c ON m.codigo_curso = c.codigo_curso
                ORDER BY m.fecha_matricula DESC
            """)
            datos = cur.fetchall()
            print(f"📋 {len(datos)} matrículas obtenidas.")
            return datos
    except Exception as e:
        manejar_error_db(e, "obtener matrículas")
        return []

# === Eliminar matrícula ===
def eliminar_matricula(id_matricula):
    """
    Elimina una matrícula según su ID.
    """
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM matriculas WHERE id = ?", (id_matricula,))
        print(f"🗑️ Matrícula con ID {id_matricula} eliminada correctamente.")
    except Exception as e:
        manejar_error_db(e, "eliminar matrícula")

# === Buscar cursos por alumno ===
def obtener_cursos_por_alumno(nif_alumno):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    c.codigo_curso,
                    c.nombre,
                    c.fecha_inicio,
                    c.fecha_fin,
                    CASE 
                        WHEN c.fecha_fin < DATE('now') THEN 'Finalizado'
                        WHEN c.fecha_inicio > DATE('now') THEN 'Abierto'
                        ELSE 'En curso'
                    END AS estado
                FROM matriculas m
                JOIN cursos c ON m.codigo_curso = c.codigo_curso
                WHERE m.nif_alumno = ?
                ORDER BY c.fecha_inicio DESC
            """, (nif_alumno,))
            datos = cur.fetchall()
            print(f"🎓 {len(datos)} cursos encontrados para el alumno {nif_alumno}.")
            return datos
    except Exception as e:
        manejar_error_db(e, "obtener cursos por alumno")
        return []

# === Buscar alumnos por curso ===
def obtener_alumnos_por_curso(codigo_curso):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    a.nif,
                    a.nombre || ' ' || a.apellidos AS alumno,
                    a.telefono,
                    a.email,
                    CASE 
                        WHEN c.fecha_fin < DATE('now') THEN 'Finalizado'
                        WHEN c.fecha_inicio > DATE('now') THEN 'Pendiente'
                        ELSE 'En curso'
                    END AS estado_curso
                FROM matriculas m
                JOIN alumnos a ON m.nif_alumno = a.nif
                JOIN cursos c ON m.codigo_curso = c.codigo_curso
                WHERE m.codigo_curso = ?
                ORDER BY a.apellidos, a.nombre
            """, (codigo_curso,))
            datos = cur.fetchall()
            print(f"👥 {len(datos)} alumnos encontrados para el curso {codigo_curso}.")
            return datos
    except Exception as e:
        manejar_error_db(e, "obtener alumnos por curso")
        return []