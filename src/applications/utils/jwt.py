
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from src.config import global_settings

class JWTUtils:
    @staticmethod
    def generate_access_token(user_id:str, email:str, role:str) -> str:
        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes= 60),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, global_settings.SECRET_KEY, algorithm="HS256")
    @staticmethod
    def generate_refresh_token(user_id:str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, global_settings.SECRET_KEY, algorithm="HS256")
    @staticmethod
    def verify_token(token:str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, global_settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None
