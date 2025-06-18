from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr

from app.schemas.base import BaseValidatedModel


class UserUpdate(BaseValidatedModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None


class UserUpdateResponse(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    avatar_url: Optional[HttpUrl]

    class Config:
        from_attributes = True
