from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from db import get_elastic, get_redis
from models import Person

from .service import Service


class PersonService(Service):
    def __init__(
        self,
        redis: Redis,
        elastic: AsyncElasticsearch,
    ):
        super().__init__(redis, elastic, ('persons', Person))


@lru_cache
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
