from pydantic import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    services: Dict[str, bool]
    openai: Dict[str, str]
    redis: Dict[str, str]
    qdrant: Dict[str, str]
    postgres: Dict[str, str]

    class Config:
        env_file = ".env"