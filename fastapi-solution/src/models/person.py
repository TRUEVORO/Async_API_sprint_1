from pydantic import BaseModel

from .mixin import OrjsonMixin, UUIDMixin


class _Person(UUIDMixin):
    """Person model."""

    full_name: str
    roles: list[str]


class Persons(BaseModel):
    """Person models."""

    persons: _Person


class Person(_Person, OrjsonMixin):
    """Person model for business logic."""

    pass
