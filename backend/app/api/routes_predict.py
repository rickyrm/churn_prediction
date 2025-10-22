from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.models.prediction_model import PredictionRecord
from app.services.churn_service import predecir_churn
from app.database.database import get_session
from app.core.auth import verificar_token
from typing import Optional
from sqlmodel import Session, select, desc
from jose import jwt, JWTError
import json

oauth2__scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "TU_CLAVE_SECRETA_SUPER_SEGURA"
ALGORITHM = "HS256"

def verificar_token(token: str = Depends(oauth2__scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
router = APIRouter()

@router.post("/predecir/", dependencies=[Depends(verificar_token)])
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


@router.get("/predicciones/", response_model=list[PredictionRecord], dependencies=[Depends(verificar_token)])
def obtener_predicciones(session: Session = Depends(get_session)):
    try:
        statement = select(PredictionRecord).order_by(desc(PredictionRecord.timestamp))
        predicciones = session.exec(statement).all()
        if not predicciones:
            raise HTTPException(status_code=404, detail="No hay predicciones registradas")
        return predicciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener predicciones: {str(e)}")

@router.get("/predicciones", response_model=list[PredictionRecord], dependencies=[Depends(verificar_token)])
def obtener_predicciones(
    customer_id: Optional[str] = Query(None, description="Filtrar por ID de cliente"),
    from_date: Optional[datetime] = Query(None, description="Fecha mínima (YYYY-MM-DD)"),
    to_date: Optional[datetime] = Query(None, description="Fecha máxima (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Número de página (por defecto 1)"),
    limit: int = Query(10, ge=1, le=100, description="Resultados por página (por defecto 10)"),
    session: Session = Depends(get_session)
):
    """
    Devuelve predicciones con filtros opcionales por cliente y rango de fechas.
    Incluye paginación profesional para grandes volúmenes de datos.
    """
    try:
        # Base query
        statement = select(PredictionRecord)

        # Filtros opcionales
        if customer_id:
            statement = statement.where(PredictionRecord.customer_id == customer_id)

        if from_date:
            statement = statement.where(PredictionRecord.timestamp >= from_date)

        if to_date:
            statement = statement.where(PredictionRecord.timestamp <= to_date + timedelta(days=1))

        # Orden y paginación
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

@router.get("/stats", dependencies=[Depends(verificar_token)])
def obtener_estadisticas(session: Session = Depends(get_session)):
    """
    Devuelve métricas generales de predicciones almacenadas.
    Incluye totales, proporciones y última fecha registrada.
    """
    try:
        statement = select(PredictionRecord)
        registros = session.exec(statement).all()

        if not registros:
            return {
                "total_predicciones": 0,
                "abandona": 0,
                "permanece": 0,
                "porcentaje_abandono": 0.0,
                "ultima_prediccion": None
            }

        total = len(registros)
        abandona = sum(1 for r in registros if r.prediction.lower() == "abandona")
        permanece = total - abandona
        porcentaje_abandono = round((abandona / total) * 100, 2)

        ultima_pred = max(r.timestamp for r in registros)

        return {
            "total_predicciones": total,
            "abandona": abandona,
            "permanece": permanece,
            "porcentaje_abandono": porcentaje_abandono,
            "ultima_prediccion": ultima_pred
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")
