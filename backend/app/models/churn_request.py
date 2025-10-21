# app/schemas/churn_request.py
from pydantic import BaseModel

class ChurnRequest(BaseModel):
    customer_id: str  # Solo necesitas este campo
