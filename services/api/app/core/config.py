from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    app_name: str = Field(default="Attendance API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    debug: bool = Field(default=True, alias="DEBUG")
    database_url: str = Field(default="sqlite:///./attendance.db", alias="DATABASE_URL")

    jwt_secret_key: str = Field(default="change-this-in-production", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    qr_secret_key: str = Field(default="change-this-too", alias="QR_SECRET_KEY")
    qr_algorithm: str = Field(default="HS256", alias="QR_ALGORITHM")
    qr_token_expire_minutes: int = Field(default=15, alias="QR_TOKEN_EXPIRE_MINUTES")


@lru_cache
def get_settings() -> Settings:
    return Settings()
