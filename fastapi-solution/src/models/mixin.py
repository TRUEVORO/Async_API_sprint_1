from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    """Миксин модель uuid."""

    uuid: UUID = Field(default_factory=uuid4)


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonMixin(BaseModel):
    """Модель для быстрой работы с json."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
