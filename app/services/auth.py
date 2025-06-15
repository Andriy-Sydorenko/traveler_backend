import datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:

    @staticmethod
    def generate_jwt_token(user_uuid: str) -> str:
        payload = {
            "user_uuid": user_uuid,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=settings.jwt_access_token_expire_minutes),
        }
        token = jwt.encode(
            payload, settings.jwt_secret, algorithm=settings.jwt_encrypt_algorithm
        )
        return token

    @staticmethod
    def decode_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_encrypt_algorithm]
            )
            user_uuid: str = payload["user_uuid"]
            return user_uuid
        except (KeyError, ValueError):
            raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )
