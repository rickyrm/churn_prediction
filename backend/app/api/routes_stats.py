# app/api/routes_stats.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.prediction_model import PredictionRecord
from app.core.auth import verificar_token

router = APIRouter(
    prefix="/stats",
    tags=["Estadísticas"],
    dependencies=[Depends(verificar_token)]  # Protege toda la ruta con JWT
)

@router.get("/")
def obtener_estadisticas(session: Session = Depends(get_session)):
    """Devuelve métricas generales de predicciones almacenadas. Incluye totales, proporciones y última fecha registrada."""
    try:
        registros = session.exec(select(PredictionRecord)).all()

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




