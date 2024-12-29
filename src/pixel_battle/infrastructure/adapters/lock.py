from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from redis.asyncio.cluster import RedisCluster
from redis.asyncio.lock import Lock as _RedisLock

from pixel_battle.application.ports.lock import Lock
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.redis.keys import chunk_key_when


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterLock(Lock):
    redis_cluster: RedisCluster

    def __call__(self, chunk: Chunk) -> _RedisLock:
        return _RedisLock(
            name=chunk_key_when(chunk=chunk) + b"lock",
            redis=self.redis_cluster,
            timeout=5,
            blocking_timeout=15,
            thread_local=False,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class FakeLock(Lock):
    @asynccontextmanager
    async def __call__(self, _: Chunk) -> AsyncIterator[None]:
        yield
