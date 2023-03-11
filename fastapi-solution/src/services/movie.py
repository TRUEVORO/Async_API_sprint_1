from functools import lru_cache

from db import get_elastic, get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models import Movie
from redis.asyncio import Redis

from .service import Service


class MovieService(Service):
    def __init__(
        self,
        redis: Redis,
        elastic: AsyncElasticsearch,
    ):
        super().__init__(redis, elastic, ('movies', Movie))


@lru_cache
def get_movie_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> MovieService:
    return MovieService(redis, elastic)
