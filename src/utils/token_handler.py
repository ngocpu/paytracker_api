# src/services/token_handler.py
import jwt
from jwt import JWTError
from datetime import datetime, timedelta
from typing import Optional, Dict
from src.core import global_settings

class TokenHandler:
    def __init__(self):
        self.settings = global_settings

    def create_access_token(self, data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.settings.jwt_expiration))
        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "token_type": "access"})
        return jwt.encode(to_encode, self.settings.jwt_secret, algorithm=self.settings.jwt_algorithm)

    def create_refresh_token(self, data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(days=self.settings.refresh_token_expire_days))
        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "token_type": "refresh"})
        return jwt.encode(to_encode, self.settings.jwt_secret, algorithm=self.settings.jwt_algorithm)

    def decode_token(self, token: str) -> Dict:
        try:
            payload = jwt.decode(token, self.settings.jwt_secret, algorithms=[self.settings.jwt_algorithm])
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = self.decode_token(refresh_token)
            if payload.get("token_type") != "refresh":
                raise ValueError("Invalid refresh token")
            email: str = payload.get("sub")
            if not email:
                raise ValueError("Invalid token payload")
            # Create a new access token with the original subject
            return self.create_access_token(data={"sub": email})
        except ValueError as e:
            raise ValueError(f"Refresh failed: {str(e)}")