import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    ENV: str
    PORT: int
    API_V1_STR: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"

settings = Settings()