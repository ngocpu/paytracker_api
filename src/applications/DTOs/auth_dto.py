from pydantic import BaseModel, EmailStr, Field
# from src.domains.entities.users import UserRole
from typing import Optional
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    username: str = Field(..., min_length=3, max_length=50)
    preferred_language: str = Field(default="en", pattern="^(vi|en)$")
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    preferred_language: str
    role: str
    is_active: bool
    avatar_url: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    class Config:
        use_enum_values = True

class RegisterResponse(BaseModel):
    message: str
    user_id: str
    email: EmailStr

class AuthResponse(BaseModel):
    user: UserResponse
    access_tokens: TokenResponse
    refresh_tokens: TokenResponse
    message: str