from fastapi import APIRouter
from app.models.cliente import Cliente
from app.services.churn_service import predecir_churn
from app.core.logger import logger

router = APIRouter(prefix="/predecir", tags=["Predicción"])

@router.post("/")
def predecir(cliente: Cliente):
    logger.info(f"Petición recibida: {cliente.dict()}")
    resultado = predecir_churn(cliente.dict())
    logger.info(f"Resultado: {resultado}")
    return {"resultado": resultado}
