from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Customer registration request"""
    email: EmailStr
    password: str
    contact_person: str
    phone: str
    company_name: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr
