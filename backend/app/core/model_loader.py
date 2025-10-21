import joblib

def cargar_modelo(ruta: str):
    try:
        modelo = joblib.load(ruta)
        return modelo
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")
