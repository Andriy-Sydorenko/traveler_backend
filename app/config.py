import os

import cloudinary
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Demo App of Linear Clone"
    app_version: str = "0.1.0"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "password"

    jwt_secret: str = os.urandom(32).hex()
    jwt_encrypt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24 * 7

    cloudinary_cloud_name: str = "CLOUDINARY_CLOUD_NAME"
    cloudinary_api_key: str = "CLOUDINARY_API_KEY"
    cloudinary_api_secret: str = "CLOUDINARY_API_SECRET"

    allowed_hosts: list[str] = ["*"]

    @property
    def db_creds(self) -> str:
        return str(
            f"{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def async_db_url(self) -> str:
        return str(PostgresDsn(f"postgresql+asyncpg://{self.db_creds}"))

    @property
    def sync_db_url(self) -> str:
        return str(PostgresDsn(f"postgresql://{self.db_creds}"))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)
