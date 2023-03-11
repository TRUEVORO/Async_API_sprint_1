from pydantic import BaseModel, Field

from .genre import Genre
from .mixin import OrjsonMixin, UUIDMixin
from .person import Person


class _Movie(UUIDMixin):
    """Movie model with short description."""

    title: str
    imdb_rating: float


class Movies(BaseModel):
    """Movie models with short description."""

    movies: list[_Movie]


class MovieFull(_Movie):
    """Movie model with full description."""

    description: str = Field(default_factory=str)
    genre: list[Genre] = Field(default_factory=list)
    actors: list[Person] = Field(default_factory=list)
    writers: list[Person] = Field(default_factory=list)
    directors: list[Person] = Field(default_factory=list)


class Movie(MovieFull, OrjsonMixin):
    """Movie model for business logic."""

    pass
