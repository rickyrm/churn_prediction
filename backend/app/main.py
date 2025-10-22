from fastapi import FastAPI
from sqlmodel import SQLModel
from app.api.routes_predict import router as predict_router
from app.database.database import engine

app = FastAPI(
    title="Customer Churn API",
    description="API para predicción de churn con almacenamiento de registros.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas correctamente en la base de datos")

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

app.include_router(predict_router)

@app.get("/")
def root():
    return {
        "message": "🚀 API de Predicción de Churn está activa",
        "docs": "/docs",
        "health": "/health",
        "api": "/predecir/"
    }






