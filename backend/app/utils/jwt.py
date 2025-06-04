import jwt
from datetime import timedelta, datetime, timezone
class JWTService():
    def __init__(self, secret:str, algorithm:str):
        self._secret = secret
        self._algorithm = algorithm
        
    def create_token(self, payload:dict) -> str:
        return jwt.encode(
            payload,
            self._secret,
            algorithm = self._algorithm,
            headers={"exp": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()} #7 days
        )
    
    def parse_token(self, token:str) -> dict:
        return jwt.decode(token, key=self._secret, algorithms=[self._algorithm])

import os
from dotenv import load_dotenv

load_dotenv()
algorithm = os.getenv("JWT_ALGORITHM")
secret = os.getenv("JWT_SECRET")

jwt_service = JWTService(secret=secret,algorithm=algorithm)