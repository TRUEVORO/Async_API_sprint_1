from pydantic import BaseModel, Field

from .mixin import OrjsonMixin, UUIDMixin


class _Movies(UUIDMixin):
    """Movie model with persona roles."""

    roles: list[str] = Field(default_factory=list)


class _Person(UUIDMixin):
    """Person model."""

    full_name: str
    movies: list[_Movies] = Field(default_factory=list)


class Persons(BaseModel):
    """Person models."""

    persons: list[_Person] = Field(default_factory=list)


class Person(_Person, OrjsonMixin):
    """Person model for business logic."""

    pass
