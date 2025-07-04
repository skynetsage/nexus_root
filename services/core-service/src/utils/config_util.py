from pathlib import Path
from typing import  Dict, Any
import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[4]
CONFIG_DIR = PROJECT_ROOT / "config"


def load_yaml_config(filename: str) -> dict[str, Any]:
    path = CONFIG_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"YAML config file not found: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_env_file(filename: str) -> None:

    path = CONFIG_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f".env file not found: {path}")
    load_dotenv(dotenv_path=path)


