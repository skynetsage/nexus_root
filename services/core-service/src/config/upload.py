from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from ..utils.config_util import load_yaml_config, PROJECT_ROOT

class UploadConfig(BaseSettings):
    upload_folder: Path
    max_file_size: int
    allowed_file_types: List[str]

def load_config() -> UploadConfig:
    config = load_yaml_config("settings-core.yml")
    return UploadConfig(**config["uploads"])

upload_config = load_config()

