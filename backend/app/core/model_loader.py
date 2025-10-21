import joblib
from pathlib import Path

def cargar_modelo(ruta: str):
    ruta_modelo = Path(ruta)
    if not ruta_modelo.exists():
        raise FileNotFoundError(f"No se encontró el modelo en {ruta_modelo}")
    try:
        return joblib.load(ruta_modelo)
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")

