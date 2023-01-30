from pydantic import BaseModel

from .mixin import OrjsonMixin, UUIDMixin


class _Genre(UUIDMixin):
    """Genre model."""

    name: str


class Genres(BaseModel):
    """Genre models."""

    genres: _Genre


class Genre(UUIDMixin, OrjsonMixin):
    """Genre model for business logic."""

    pass
