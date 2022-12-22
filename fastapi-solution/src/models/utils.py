import orjson
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
