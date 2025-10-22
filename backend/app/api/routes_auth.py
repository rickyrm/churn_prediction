# app/api/routes_auth.py
from fastapi import APIRouter, HTTPException
from app.core.auth import crear_token_acceso

router = APIRouter()

USERS = {
    "admin": "d7cc95c9c1f84b1032ebf247e3b6c993e37bb5398f1485cd330f8179a128af3a",  # Usuario de ejemplo
}

@router.post("/token")
def login(username: str, password: str):
    if USERS.get(username) != password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = crear_token_acceso({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
