from uuid import UUID

from core.backoff import backoff
from elasticsearch import AsyncElasticsearch, NotFoundError
from models import Genre, Movie, Person
from redis.asyncio import Redis

from .utils import Mapper, is_valid_uuid


class Service:
    """Base class for executing business logic."""

    def __init__(
        self, redis: Redis, elastic: AsyncElasticsearch, mapper: Mapper | tuple[str, type[Movie | Genre | Person]]
    ):
        self.redis = redis
        self.elastic = elastic
        self.mapper = mapper if isinstance(mapper, Mapper) else Mapper(*mapper)

    async def _get_from_elastic(self, uuid: UUID) -> Movie | Genre | Person | None:
        """
        Get movie/genre/person by id from Elastic.
        :param uuid: id of the movie/genre/person
        :return: movie/genre/person data
        """
        try:
            doc = await self.elastic.get(index=self.mapper.index, id=str(uuid))
        except NotFoundError:
            return None
        return self.mapper.model(**doc['_source'])

    async def _search_in_elastic(self, query: str) -> list[Movie | Genre | Person] | None:
        """
        Search movies/genres/persons in Elastic.
        :param query: user's query
        :return: list of movies/genres/persons data
        """
        try:
            docs = await self.elastic.search(
                index='movies',
                body={
                    'query': {
                        'multi_match': {
                            'query': query,
                            'fields': [
                                'title^3',
                                'description',
                                'genre',
                            ],
                        },
                    },
                    'sort': [
                        {'imdb_rating': {'order': 'asc'}},
                        {'title': {'order': 'asc'}},
                    ],
                },
            )
        except NotFoundError:
            return None
        return [self.mapper.model(**doc) for doc in docs['hits']['hits']]

    @backoff()
    async def get_by_id(self, uuid: UUID) -> Movie | Genre | Person | None:
        """
        Get movie/genre/person by id from movies database.
        :param uuid: id of the movie/genre/person
        :return: movie/genre/person data
        """
        if data := await self._get_from_elastic(uuid):
            return data
        # TODO: add similar movies/genres/persons
        return None

    @backoff()
    async def search(self, query: str = '') -> list[Movie | Genre | Person] | None:
        """
        Full-text search movie/genre/person from movies database.
        :param query: user's query
        :return: list of movies/genres/persons data
        """
        if uuid := is_valid_uuid(query):
            data = await self.get_by_id(uuid)
            return data
        if data := await self._search_in_elastic(query):
            return data
        return None
