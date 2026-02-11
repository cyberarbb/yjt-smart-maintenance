"""사용자 스키마"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    company: str = ""
    country: str = ""
    phone: str = ""
    preferred_language: str = "en"


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    company: str
    country: str
    phone: str
    preferred_language: str
    is_active: bool
    is_admin: bool

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
