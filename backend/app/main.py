from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.api.routes_auth import router as auth_router
from app.api.routes_stats import router as stats_router
from app.api.routes_predict import router as predict_router
from app.database.database import engine

app = FastAPI(
    title="Customer Churn API",
    description="API para predicción de churn con almacenamiento de registros.",
    version="1.0.0"
)

# --- CORS ---
origins = [
    "http://127.0.0.1:5173",  # puerto de tu frontend
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # o ["*"] en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup ---
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas correctamente en la base de datos")

# --- Health check ---
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# --- Routers ---
app.include_router(auth_router, tags=["Auth"])
app.include_router(stats_router, tags=["Stats"])
app.include_router(predict_router, tags=["Predict"])

@app.get("/")
def root():
    return {
        "message": "🚀 API de Predicción de Churn está activa",
        "docs": "/docs",
        "health": "/health",
        "api": "/predecir/"
    }




