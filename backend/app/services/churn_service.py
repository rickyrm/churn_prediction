import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join("models", "modelo_churn.joblib")

modelo = joblib.load(MODEL_PATH)

def predecir_churn(data: dict):
    try:
        # Convertimos el diccionario a DataFrame
        df = pd.DataFrame([data])

        # Validamos columnas esperadas
        columnas_esperadas = ["edad", "ingresos", "antiguedad_meses", "num_productos"]
        if not all(col in df.columns for col in columnas_esperadas):
            raise ValueError(f"Faltan columnas. Se esperaban: {columnas_esperadas}")

        pred = modelo.predict(df)[0]
        prob = modelo.predict_proba(df)[0][1]

        resultado = "Abandona" if pred == 1 else "Permanece"
        return resultado, float(prob)

    except Exception as e:
        raise RuntimeError(f"Error al predecir churn: {str(e)}")






