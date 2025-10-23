# app/core/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "774bed2568a0999e7a11b26902c64f321ab43a1e51f0f5e794c669a04483f980"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# HTTP Bearer scheme para Swagger y dependencias
bearer_scheme = HTTPBearer()

# Crear token JWT
def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificar token JWT
def verificar_token(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        token_str = token.credentials  # <-- token real
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        if user is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


