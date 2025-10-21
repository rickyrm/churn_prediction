# app/api/routes_predictions_log.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.prediction_record import PredictionRecord
from app.database.database import get_session

router = APIRouter(prefix="/predicciones", tags=["Historial de predicciones"])

@router.get("/")
def listar_predicciones(session: Session = Depends(get_session)):
    registros = session.exec(select(PredictionRecord).order_by(PredictionRecord.timestamp.desc())).all()
    return registros
