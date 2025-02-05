from asyncio import Lock as AsyncIOLock
from collections import defaultdict
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from redis.asyncio import RedisCluster
from redis.asyncio.lock import Lock as RedisClusterLock

from pixel_battle.application.ports.chunk_optimistic_lock import (
    ActiveChunkOptimisticLock,
    ChunkOptimisticLockWhen,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.redis.keys import chunk_key_when


@dataclass(init=False, slots=True)
class AsyncIOChunkOptimisticLockWhen(ChunkOptimisticLockWhen):
    __lock_by_chunk: defaultdict[Chunk, AsyncIOLock]

    def __init__(self) -> None:
        self.__lock_by_chunk = defaultdict(AsyncIOLock)

    @asynccontextmanager
    async def __call__(
        self, *, chunk: Chunk
    ) -> AsyncIterator[ActiveChunkOptimisticLock]:
        lock = self.__lock_by_chunk[chunk]

        if lock.locked():
            yield ActiveChunkOptimisticLock(is_owned=False)
            return

        await lock.acquire()

        try:
            yield ActiveChunkOptimisticLock(is_owned=True)
        except Exception as error:
            lock.release()
            raise error from error
        else:
            lock.release()


@dataclass(kw_only=True, frozen=True, unsafe_hash=False, slots=True)
class RedisClusterChunkOptimisticLockWhen(ChunkOptimisticLockWhen):
    redis_cluster: RedisCluster
    lock_max_age_seconds: int | float | None
    _lock_by_chunk: dict[Chunk, RedisClusterLock] = field(
        init=False, default_factory=dict
    )

    def __new_lock_of(self, chunk: Chunk) -> RedisClusterLock:
        return RedisClusterLock(
            redis=self.redis_cluster,
            name=chunk_key_when(chunk=chunk) + b"_optimistic_lock",
            blocking=False,
            timeout=self.lock_max_age_seconds,
        )

    def __lock_of(self, chunk: Chunk) -> RedisClusterLock:
        lock = self._lock_by_chunk.get(chunk)

        if lock is not None:
            return lock

        lock = self.__new_lock_of(chunk)
        self._lock_by_chunk[chunk] = lock

        return lock

    @asynccontextmanager
    async def __call__(
        self, *, chunk: Chunk
    ) -> AsyncIterator[ActiveChunkOptimisticLock]:
        lock = self.__lock_of(chunk)

        is_active_lock_owned = await lock.acquire()
        active_lock = ActiveChunkOptimisticLock(is_owned=is_active_lock_owned)

        if not is_active_lock_owned:
            yield active_lock
            return

        try:
            yield active_lock
        except Exception as error:
            await lock.release()
            raise error from error
        else:
            await lock.release()
