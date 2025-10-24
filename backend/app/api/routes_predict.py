from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlmodel import Session, select, desc
import json

from app.models.prediction_model import PredictionRecord
from app.database.database import get_session
from app.services.churn_service import predecir_churn
from app.core.auth import verificar_token

router = APIRouter()


@router.post("/predecir/", dependencies=[Depends(verificar_token)])
def crear_prediccion(record: PredictionRecord, session: Session = Depends(get_session)):
    # Validar si ya existe cliente
    existe = session.exec(
        select(PredictionRecord).where(PredictionRecord.customer_id == record.customer_id)
    ).first()

    if existe:
        raise HTTPException(status_code=409, detail="Este cliente ya tiene una predicción registrada.")

    input_dict = (
        json.loads(record.input_data) if isinstance(record.input_data, str) else record.input_data
    )

    pred, prob = predecir_churn(input_dict)

    nuevo = PredictionRecord(
        customer_id=record.customer_id,
        input_data=json.dumps(input_dict),
        prediction=pred,
        probability=prob,
    )

    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    return nuevo


@router.get("/predicciones", dependencies=[Depends(verificar_token)])
def obtener_predicciones(session: Session = Depends(get_session)):
    return session.exec(select(PredictionRecord)).all()


@router.put("/predicciones/{id}", dependencies=[Depends(verificar_token)])
def actualizar_prediccion(id: int, data: dict, session: Session = Depends(get_session)):
    record = session.get(PredictionRecord, id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    input_data = data.get("input_data")
    if input_data:
        pred, prob = predecir_churn(input_data)
        record.input_data = json.dumps(input_data)
        record.prediction = pred
        record.probability = prob

    session.add(record)
    session.commit()
    session.refresh(record)

    return record


@router.delete("/predicciones/{id}", dependencies=[Depends(verificar_token)])
def eliminar_prediccion(id: int, session: Session = Depends(get_session)):
    record = session.get(PredictionRecord, id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    session.delete(record)
    session.commit()

    return {"message": "Registro eliminado correctamente"}

