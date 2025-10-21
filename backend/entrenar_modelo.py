import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Datos de ejemplo (ficticios)
X = pd.DataFrame([
    [25, 3000, 12, 2],
    [40, 7000, 24, 1],
    [35, 5000, 36, 3],
    [50, 8000, 48, 1],
    [30, 2000, 6, 2],
], columns=["edad", "ingresos", "antiguedad_meses", "num_productos"])

# Etiquetas (0 = Permanece, 1 = Abandona)
y = [0, 1, 0, 1, 1]

# Entrenar modelo simple
modelo = RandomForestClassifier(n_estimators=50, random_state=42)
modelo.fit(X, y)

# Guardar modelo en la carpeta correcta
joblib.dump(modelo, "models/modelo_churn.joblib")

print("✅ Modelo entrenado y guardado correctamente en 'models/modelo_churn.joblib'")
