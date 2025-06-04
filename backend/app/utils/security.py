from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def verify_pwd(plain_text:str, hashed_pwd:str) -> bool:
    return pwd_context.verify(plain_text, hashed_pwd)

def hash_pwd(plain_text:str) -> str:
    return pwd_context.hash(plain_text)
