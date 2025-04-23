from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    services: Dict[str, bool]
    openai: Dict[str, str | int]
    redis: Dict[str, str | int]
    qdrant: Dict[str, str | int]
    postgres: Dict[str, str | int]

    class Config:
        env_file = ".env"