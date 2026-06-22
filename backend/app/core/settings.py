from pydantic_settings import BaseSettings
from functools import lru_cache
import yaml, os


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    secret_key: str = "dev-secret-change-in-production"
    token_expire_minutes: int = 480

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_config() -> dict:
    config_path = os.path.join(os.path.dirname(__file__), "../../config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
