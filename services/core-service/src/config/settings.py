from typing import Literal, Optional
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..utils.config_util import load_env_file


Environment = Literal["dev", "test", "prod"]

class Settings(BaseSettings):
    ENV: Environment = "dev"
    PORT: int = 8000
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    VERSION: str


    SECRET_KEY: str = Field(min_length=3, default="unsafe-dev-secret-key-change-me")

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "nexus_db"
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "nexus_history"

    @property
    def get_pg_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # @field_validator("SECRET_KEY", mode="before")
    # def validate_secret_key(cls, v: Optional[str]) -> str:
    #     if not v and cls.model_fields["ENV"].default == "prod":
    #         raise ValueError("SECRET_KEY is required in production")
    #     return v or cls.model_fields["SECRET_KEY"].default

    model_config = SettingsConfigDict(
        env_file=str(load_env_file(".env.core")),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
        case_sensitive=False
    )

settings = Settings()