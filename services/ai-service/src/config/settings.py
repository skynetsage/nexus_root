from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional

from utils.config_util import load_env_file

class Settings(BaseSettings):
    GROQ_API_KEY: str
    HF_KEY: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None

    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=str(load_env_file(".env.ai")),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
        case_sensitive=False
    )

settings = Settings()