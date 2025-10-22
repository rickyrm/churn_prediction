from sqlmodel import SQLModel, Field
from datetime import datetime
import json

class PredictionRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: str
    input_data: str  # Guardamos el JSON como string
    prediction: str
    probability: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Métodos auxiliares (opcionales)
    def set_input_data(self, data: dict):
        self.input_data = json.dumps(data)

    def get_input_data(self) -> dict:
        try:
            return json.loads(self.input_data)
        except Exception:
            return {}


