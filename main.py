from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.utils import validation_exception_handler

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
