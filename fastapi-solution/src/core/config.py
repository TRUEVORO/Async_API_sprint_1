import os
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Settings class to read environment variables."""

    class Config:
        env_file = BASE_DIR / '.env'
        env_file_encoding = 'utf-8'


class RedisConfig(Settings):
    """Configuration class for redis."""

    redis_host: str
    redis_port: int


class ElasticConfig(Settings):
    """Configuration class for elastic."""

    elastic_host: str
    elastic_port: int
