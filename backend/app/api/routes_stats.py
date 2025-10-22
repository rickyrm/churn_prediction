# app/api/routes_stats.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.database.database import get_session
from app.models.prediction_model import PredictionRecord
from app.core.auth import verificar_token

router = APIRouter()

@router.get("/stats", dependencies=[Depends(verificar_token)])
def obtener_estadisticas(session: Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(PredictionRecord)).one()

    # Obtener totales por tipo de predicción
    abandona = session.exec(
        select(func.count()).where(PredictionRecord.prediction == "Abandona")
    ).one()
    permanece = session.exec(
        select(func.count()).where(PredictionRecord.prediction == "Permanece")
    ).one()

    porcentaje_abandono = (abandona / total * 100) if total > 0 else 0
    porcentaje_permanencia = (permanece / total * 100) if total > 0 else 0

    return {
        "total_predicciones": total,
        "abandona": abandona,
        "permanece": permanece,
        "porcentaje_abandono": round(porcentaje_abandono, 2),
        "porcentaje_permanencia": round(porcentaje_permanencia, 2)
    }
