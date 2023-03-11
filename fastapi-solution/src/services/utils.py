from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from models import Genre, Movie, Person


@dataclass
class Mapper:
    """Model for describing each service."""

    index: Literal['genres', 'movies', 'persons']
    model: type(Movie) | type(Genre) | type(Person)


def is_valid_uuid(query: str) -> UUID | bool:
    """
    Check whether a query is a valid UUID.
    :param query: query to be checked
    :return: uuid if true, False if not
    """
    try:
        uuid = UUID(query)
        return uuid
    except ValueError:
        return False
