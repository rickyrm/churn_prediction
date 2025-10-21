from fastapi import FastAPI
from app.api.routes_predict import router as predict_router
from sqlmodel import SQLModel
from app.database.database import engine  # tu engine SQLAlchemy
from app.models.prediction_model import PredictionRecord

app = FastAPI(
    title="Customer Churn API",
    description="API para predicción de churn con almacenamiento de registros.",
    version="1.0.0"
)

# Crear tablas al iniciar la aplicación
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas correctamente en la base de datos")

# Endpoint de salud
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# Rutas del módulo de predicción
app.include_router(predict_router)

# Endpoint raíz
@app.get("/")
def root():
    return {
        "message": "🚀 API de Predicción de Churn está activa",
        "docs": "/docs",
        "health": "/health",
        "api": "/predecir/"
    }





