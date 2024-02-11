from functools import lru_cache
from typing import Any, Dict

from pydantic_settings import BaseSettings

from .components.logging import logging_settings


class Settings(BaseSettings):
    logging: Dict[str, Any] = logging_settings


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()
