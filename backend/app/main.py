from fastapi import FastAPI
from app.core.config import setup_cors
from app.api.routes_predict import router as predict_router
from app.api.routes_health import router as health_router
from app.database.database import init_db
from app.api.routes_predictions_log import router as predictions_router

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API de predicción de abandono de clientes con IA.",
    version="1.0.0",
)
@app.on_event("startup")
def on_startup():
    init_db()

# Configurar CORS
setup_cors(app)

# Incluir rutas
app.include_router(health_router)
app.include_router(predict_router)
app.include_router(predictions_router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}




