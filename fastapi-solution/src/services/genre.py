from functools import lru_cache

from db import get_elastic, get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models import Genre
from redis.asyncio import Redis

from .service import Service


class GenreService(Service):
    """Genre class for executing business logic."""

    def __init__(
        self,
        redis: Redis,
        elastic: AsyncElasticsearch,
    ):
        super().__init__(redis, elastic, ('genres', Genre))


@lru_cache
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
