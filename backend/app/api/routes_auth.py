import os
from fastapi import APIRouter, HTTPException, Form, status
from passlib.context import CryptContext
from app.core.auth import crear_token_acceso

router = APIRouter()

# Configuración de hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cargar variables de entorno (ya cargadas en main.py con load_dotenv)
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña ingresada coincide con el hash almacenado.
    """
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    """
    Endpoint para autenticación. 
    Verifica usuario y contraseña, y devuelve el token JWT si son válidos.
    """
    if not ADMIN_USER or not ADMIN_PASSWORD_HASH:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Configuración de autenticación incompleta en el servidor."
        )

    # Verificar credenciales
    if username != ADMIN_USER or not verificar_password(password, ADMIN_PASSWORD_HASH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Generar token JWT
    access_token = crear_token_acceso({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}



