import os
import yaml
from functools import lru_cache
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogSettings(BaseSettings):
    level: str
    dir: str
    rotation_enabled: bool
    rotation: str
    retention: str
    compression: str
    format_console: str
    format_file: str


class Settings(BaseSettings):
    # Environment
    ENV: Literal["dev", "prod"] = "dev"
    PORT: int = 8000

    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str

    # Database settings - PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # Database settings - MongoDB
    MONGO_URI: str
    MONGO_DB: str

    # Log settings (optional, filled manually later)
    log: Optional[LogSettings] = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    @property
    def postgres_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def mongodb_uri(self) -> str:
        return self.MONGO_URI


class DevSettings(Settings):
    ENV: Literal["dev"] = "dev"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class ProdSettings(Settings):
    ENV: Literal["prod"] = "prod"
    model_config = SettingsConfigDict(env_file=".env.prod", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    env = os.getenv("ENV", "dev")

    if env == "prod":
        settings = ProdSettings()
    else:
        settings = DevSettings()

    yaml_path = "./settings.yml"
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as file:
            config = yaml.safe_load(file)
        log_config = config["log"]
        settings.log = LogSettings(**log_config)

    return settings

settings = get_settings()
