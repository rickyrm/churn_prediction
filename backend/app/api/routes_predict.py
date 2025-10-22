from fastapi import APIRouter, HTTPException, Depends
from app.models.prediction_model import PredictionRecord
from app.services.churn_service import predecir_churn
from app.database.database import get_session
from sqlmodel import Session, select, desc
import json

router = APIRouter()

@router.post("/predecir/")
def predecir_churn_endpoint(
    record: PredictionRecord,
    session: Session = Depends(get_session)
):
    try:
        if isinstance(record.input_data, str):
            try:
                input_dict = json.loads(record.input_data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="input_data no es un JSON válido")
        else:
            input_dict = record.input_data

        columnas_esperadas = ["edad", "ingresos", "antiguedad_meses", "num_productos"]
        for col in columnas_esperadas:
            if col not in input_dict:
                raise HTTPException(status_code=400, detail=f"Falta la columna '{col}' en input_data")
            if not isinstance(input_dict[col], (int, float)):
                raise HTTPException(status_code=400, detail=f"Columna '{col}' debe ser numérica")

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


@router.get("/predicciones/", response_model=list[PredictionRecord])
def obtener_predicciones(session: Session = Depends(get_session)):
    try:
        statement = select(PredictionRecord).order_by(desc(PredictionRecord.timestamp))
        predicciones = session.exec(statement).all()
        if not predicciones:
            raise HTTPException(status_code=404, detail="No hay predicciones registradas")
        return predicciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener predicciones: {str(e)}")



