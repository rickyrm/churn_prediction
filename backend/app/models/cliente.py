from pydantic import BaseModel, Field

class Cliente(BaseModel):
    edad: int = Field(..., ge=18, le=100)
    ingresos: float = Field(..., gt=0)
    antiguedad_meses: int = Field(..., ge=0)
    num_productos: int = Field(..., ge=1, le=10)
