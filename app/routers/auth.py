from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register():
    pass


@router.post("/login")
async def login():
    pass


@router.get("/logout")
async def logout():
    pass
