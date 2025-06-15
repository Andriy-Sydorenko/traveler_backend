from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseValidatedModel


class UserRegister(BaseValidatedModel):
    email: str = EmailStr()
    password: str = Field(..., min_length=8)
    username: Optional[str] = Field(None, min_length=3)


class UserRegisterResponse(BaseModel):
    email: str = EmailStr()
    username: Optional[str] = Field(None, min_length=3)

    class Config:
        from_attributes = True


class UserLogin(BaseValidatedModel):
    email: str = EmailStr()
    password: str = Field(..., min_length=8)


class UserLoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"
