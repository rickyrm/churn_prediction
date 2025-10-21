# app/models/prediction_record.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class PredictionRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: str
    input_data: str
    prediction: str
    probability: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
