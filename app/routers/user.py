from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])


@router.patch("/")
async def update_user():
    pass
