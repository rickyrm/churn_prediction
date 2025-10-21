import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1️⃣ Simulación de dataset
data = {
    "edad": [25, 45, 32, 50, 40, 29, 60, 35, 48, 23],
    "ingresos": [25000, 54000, 42000, 61000, 58000, 32000, 72000, 40000, 55000, 23000],
    "antiguedad_meses": [12, 48, 30, 60, 55, 15, 70, 28, 50, 8],
    "num_productos": [1, 3, 2, 4, 3, 1, 5, 2, 4, 1],
    "abandono": [0, 1, 0, 1, 0, 0, 1, 0, 1, 1]
}

df = pd.DataFrame(data)

# 2️⃣ División de datos
X = df.drop("abandono", axis=1)
y = df["abandono"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3️⃣ Entrenamiento del modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 4️⃣ Evaluación
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print(f"Exactitud del modelo: {acc:.2f}")

# 5️⃣ Guardar el modelo
joblib.dump(model, "modelo_churn.joblib")
print("Modelo guardado como modelo_churn.joblib")
