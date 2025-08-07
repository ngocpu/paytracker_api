from passlib.context import CryptContext
from src.core import logger

class PasswordHandler:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        if not password or len(password) < 8:
            logger.error("Password must be at least 8 characters")
            raise ValueError("Password must be at least 8 characters")
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        if not plain_password or not hashed_password:
            return False
        return self.pwd_context.verify(plain_password, hashed_password)