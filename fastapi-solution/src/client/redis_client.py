from redis.asyncio import ConnectionError
from redis.typing import EncodableT, KeyT

from core import backoff

from .base_client import AsyncBaseClient


class AsyncRedisClient(AsyncBaseClient):
    """Redis client."""

    @backoff(ConnectionError)
    async def set(self, name: KeyT, value: EncodableT, *args, **kwargs) -> None:
        """Redis client execute set."""

        await self.connection.set(name, value, *args, **kwargs)

    @backoff(ConnectionError)
    async def get(self, name: KeyT) -> bytes | None:
        """Redis client execute get."""

        return await self.connection.get(name)
