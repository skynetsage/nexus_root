import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

_SETTINGS_FILE_PATH = Path(__file__).resolve()
_PROJECT_ROOT = _SETTINGS_FILE_PATH.parents[4]
_ENV_FILE_PATH = _PROJECT_ROOT / "config" / "core_config" / ".env.core"


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

    # @property
    # def get_pg_url(self) -> str:
    #     return (
    #         f"postgresql+asyncpg://{self.POSTGRES_USER}:"
    #         f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
    #         f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    #     )
    @property
    def get_pg_url(self) -> str:
        # Debug prints to see the actual values of attributes from 'self'
        print(f"--- DEBUG: settings.get_pg_url ---")
        pg_user = getattr(self, 'POSTGRES_USER', 'NOT_SET_ON_INSTANCE')
        pg_password_present = bool(getattr(self, 'POSTGRES_PASSWORD', None))
        pg_host = getattr(self, 'POSTGRES_HOST', 'NOT_SET_ON_INSTANCE')
        pg_port = getattr(self, 'POSTGRES_PORT', 'NOT_SET_ON_INSTANCE')
        pg_db = getattr(self, 'POSTGRES_DB', 'NOT_SET_ON_INSTANCE')

        print(f"Retrieved POSTGRES_USER: {pg_user}")
        print(f"Retrieved POSTGRES_PASSWORD is set: {pg_password_present}")
        print(f"Retrieved POSTGRES_HOST: {pg_host}")
        print(f"Retrieved POSTGRES_PORT: {pg_port}")
        print(f"Retrieved POSTGRES_DB: {pg_db}")
        print(f"--- END DEBUG: settings.get_pg_url ---")

        # Explicitly check if any of the required components are None or empty strings
        # Pydantic should catch missing values during instantiation if they are not Optional
        # and have no defaults, but this adds an extra layer for runtime issues.
        if not all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_PORT, self.POSTGRES_DB]):
            missing_details = {
                "user": self.POSTGRES_USER,
                "password_is_set": bool(self.POSTGRES_PASSWORD),
                "host": self.POSTGRES_HOST,
                "port": self.POSTGRES_PORT,
                "db_name": self.POSTGRES_DB,
            }
            raise ValueError(
                "One or more database connection parameters are missing, None, or empty. "
                f"Current values: {missing_details}"
            )

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE_PATH), env_file_encoding="utf-8", extra="allow"
    )

settings = Settings()