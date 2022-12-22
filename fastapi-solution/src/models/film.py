from pydantic import Field

from genre import Genre
from person import Person
from utils import OrjsonMixin, UUIDMixin


class FilmMixin(UUIDMixin):
    title: str
    imdb_rating: float
    description: str = Field(default_factory=str)
    genre: list[Genre] = Field(default_factory=list)
    actors: list[Person] = Field(default_factory=list)
    writers: list[Person] = Field(default_factory=list)
    directors: list[Person] = Field(default_factory=list)


class Film(FilmMixin, OrjsonMixin):
    pass
