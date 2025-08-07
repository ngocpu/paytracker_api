from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class PreferredLanguage(str, Enum):
    vi = "vi"
    en = "en"
class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserRegisterDTO(BaseModel):
    email: EmailStr
    username: str
    password: str
    
class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str
    
class UserDTO(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    preferred_language: Optional[PreferredLanguage] = "en"
    role: Optional[UserRole] = "user"
    is_active: Optional[bool] = True
    is_deleted: Optional[bool] = False
    avatar: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True
    
class UserResponseDTO(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    user_data: UserDTO