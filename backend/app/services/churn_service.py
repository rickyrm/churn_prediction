from app.models.prediction_record import PredictionRecord
from app.database.database import get_session
from sqlmodel import Session
import json

def predecir_churn(data):
    # Lógica del modelo ML (ya existente)
    pred = modelo.predict([list(data.dict().values())])[0]
    prob = modelo.predict_proba([list(data.dict().values())])[0][1]

    # Guardar en base de datos
    registro = PredictionRecord(
        customer_id=str(data.CustomerID),
        input_data=json.dumps(data.dict()),
        prediction=str(pred),
        probability=float(prob)
    )

    with Session(engine) as session:
        session.add(registro)
        session.commit()

    return {"prediction": pred, "probability": prob}



