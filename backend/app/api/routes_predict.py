# api/routes_predict.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.prediction_model import PredictionRecord
from app.services.churn_service import predecir_churn
from app.database.database import get_session
from sqlmodel import Session
import json

router = APIRouter()

@router.post("/predecir/")
def predecir_churn_endpoint(
    record: PredictionRecord,
    session: Session = Depends(get_session)  # sesión manejada automáticamente
):
    try:
        # Convertir input_data a dict si es string
        if isinstance(record.input_data, str):
            try:
                input_dict = json.loads(record.input_data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="input_data no es un JSON válido")
        else:
            input_dict = record.input_data

        # Validar columnas esperadas
        columnas_esperadas = ["edad", "ingresos", "antiguedad_meses", "num_productos"]
        for col in columnas_esperadas:
            if col not in input_dict:
                raise HTTPException(
                    status_code=400,
                    detail=f"Falta la columna '{col}' en input_data"
                )
            # Validar tipo numérico
            if not isinstance(input_dict[col], (int, float)):
                raise HTTPException(
                    status_code=400,
                    detail=f"Columna '{col}' debe ser numérica"
                )

        # Realizar predicción
        pred, prob = predecir_churn(input_dict)

        # Guardar en base de datos
        new_record = PredictionRecord(
            customer_id=record.customer_id,
            input_data=json.dumps(input_dict),
            prediction=pred,
            probability=prob
        )
        session.add(new_record)
        session.commit()
        session.refresh(new_record)

        return {
            "prediction": pred,
            "probability": prob
        }

    except HTTPException:
        # Ya es un error controlado (400)
        raise
    except Exception as e:
        # Otros errores inesperados devuelven 500
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


