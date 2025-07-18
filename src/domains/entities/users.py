from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class PreferredLanguage(Enum):
    VI = "vi"
    EN = "en"

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

@dataclass
class User:
    user_id: str
    username: str
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    avatar: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    preferred_language: PreferredLanguage = PreferredLanguage.VI
    role: UserRole = UserRole.USER
    is_active: bool = False
    is_deleted: bool = False
    
    def is_oauth_user(self) -> bool:
        return self.provider is not None
    
    def can_login(self) -> bool:
        return self.is_active and not self.is_deleted
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
