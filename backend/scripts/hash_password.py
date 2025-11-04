# scripts/hash_password.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_hash(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    import getpass
    pw = getpass.getpass("Introduce la contraseña para generar su hash: ")
    print(crear_hash(pw))
