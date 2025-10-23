# app/api/routes_predict.py
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlmodel import Session, select, desc
from datetime import datetime, timedelta
import json

from app.models.prediction_model import PredictionRecord
from app.database.database import get_session
from app.services.churn_service import predecir_churn
from app.core.auth import verificar_token

router = APIRouter()

# ---------------------------
# Predecir churn
# ---------------------------
@router.post("/predecir/", dependencies=[Depends(verificar_token)])
def predecir_churn_endpoint(record: PredictionRecord, session: Session = Depends(get_session)):
    try:
        input_dict = json.loads(record.input_data) if isinstance(record.input_data, str) else record.input_data

        columnas_esperadas = ["edad", "ingresos", "antiguedad_meses", "num_productos"]
        for col in columnas_esperadas:
            if col not in input_dict or not isinstance(input_dict[col], (int, float)):
                raise HTTPException(status_code=400, detail=f"Columna '{col}' faltante o no numérica")

        pred, prob = predecir_churn(input_dict)

        new_record = PredictionRecord(
            customer_id=record.customer_id,
            input_data=json.dumps(input_dict),
            prediction=pred,
            probability=prob
        )
        session.add(new_record)
        session.commit()
        session.refresh(new_record)

        return {"prediction": pred, "probability": prob}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ---------------------------
# Obtener predicciones (filtros + paginación)
# ---------------------------
@router.get("/predicciones", response_model=list[PredictionRecord], dependencies=[Depends(verificar_token)])
def obtener_predicciones(
    customer_id: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    try:
        statement = select(PredictionRecord)

        if customer_id:
            statement = statement.where(PredictionRecord.customer_id == customer_id)
        if from_date:
            statement = statement.where(PredictionRecord.timestamp >= from_date)
        if to_date:
            statement = statement.where(PredictionRecord.timestamp <= to_date + timedelta(days=1))

        statement = statement.order_by(desc(PredictionRecord.timestamp))
        offset = (page - 1) * limit
        statement = statement.offset(offset).limit(limit)

        results = session.exec(statement).all()

        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron registros con los filtros aplicados.")

        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener predicciones: {str(e)}")
