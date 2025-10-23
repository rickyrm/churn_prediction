# app/api/routes_auth.py
from fastapi import APIRouter, HTTPException, Form
from app.core.auth import crear_token_acceso

router = APIRouter()

# Usuario de ejemplo
USERS = {
    "admin": "e99a18c428cb38d5f260853678922e03"
}

@router.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    if USERS.get(username) != password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = crear_token_acceso({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


