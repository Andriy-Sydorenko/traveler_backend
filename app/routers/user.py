from typing import Annotated

import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserUpdate, UserUpdateResponse
from app.services.auth import AuthService as auth_service
from app.services.user import UserService
from app.utils import clean_file_entry

router = APIRouter(prefix="/me", tags=["me"])


@router.patch("/")
async def update_user(
    user_update: UserUpdate,
    user_id: Annotated[str, Depends(auth_service.decode_jwt)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserUpdateResponse:
    user_service = UserService(db)
    user = await user_service.get_user("id", user_id)
    await user_service.update_user(
        user, user_update.model_dump(exclude_none=True), ["email", "username"]
    )
    return UserUpdateResponse.model_validate(user)


@router.patch("/update-avatar/")
async def update_avatar(
    file: Annotated[UploadFile, Depends(clean_file_entry)],
    user_id: Annotated[str, Depends(auth_service.decode_jwt)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserUpdateResponse:
    user_service = UserService(db)
    user = await user_service.get_user("id", user_id)
    result = cloudinary.uploader.upload(file.file)
    image_url = result["secure_url"]
    await user_service.update_user(
        user, {"avatar_url": image_url}, ["email", "username"]
    )
    return UserUpdateResponse.model_validate(user)
