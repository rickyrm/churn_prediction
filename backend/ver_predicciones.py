# ver_predicciones.py
from sqlmodel import Session, select
from app.database.database import engine
from app.models.prediction_model import PredictionRecord

def mostrar_predicciones():
    with Session(engine) as session:
        results = session.exec(select(PredictionRecord)).all()
        if not results:
            print("No hay predicciones guardadas todavía.")
            return
        print(f"{'ID':<5} {'Customer':<15} {'Prediction':<12} {'Probability':<10} {'Input Data'}")
        print("-"*80)
        for r in results:
            prediction = getattr(r, 'prediction', 'N/A')
            probability = getattr(r, 'probability', 0.0)
            print(f"{r.id:<5} {r.customer_id:<15} {prediction:<12} {probability:<10.2f} {r.input_data}")

if __name__ == "__main__":
    mostrar_predicciones()

