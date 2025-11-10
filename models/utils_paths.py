import os, sys

def get_export_path(nombre_archivo):
    #Devuelve una ruta segura y persistente (junto al .exe o al proyecto)
    #para guardar exportaciones como PDF o Excel.
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    export_dir = os.path.join(base_dir, "exportaciones")
    os.makedirs(export_dir, exist_ok=True)
    return os.path.join(export_dir, nombre_archivo)
