import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

_SETTINGS_FILE_PATH = Path(__file__).resolve()
_PROJECT_ROOT = _SETTINGS_FILE_PATH.parents[3]
_ENV_FILE_PATH = _PROJECT_ROOT / "config" / ".env.core"


class Settings(BaseSettings):
    ENV: str = "dev"
    PORT: int = 8000

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int 
    POSTGRES_DB: str

    @property
    def get_pg_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE_PATH), env_file_encoding="utf-8", extra="allow"
    )

settings = Settings()