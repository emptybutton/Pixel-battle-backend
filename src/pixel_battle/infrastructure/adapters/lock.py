from asyncio import Lock as _AsyncIOLock
from dataclasses import dataclass

from redis.asyncio.cluster import RedisCluster
from redis.asyncio.lock import Lock as _RedisLock

from pixel_battle.application.ports.lock import Lock
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.redis_cluster.identity import chunk_key_of


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterLock(Lock):
    redis_cluster: RedisCluster

    def __call__(self, chunk: Chunk) -> _RedisLock:
        return _RedisLock(
            name=chunk_key_of(chunk),
            redis=self.redis_cluster,
            timeout=5,
            blocking_timeout=15,
            thread_local=False,
        )


@dataclass(init=False)
class AsyncIOLock(Lock):
    def __init__(self) -> None:
        self.__lock_by_chunk = dict[Chunk, _AsyncIOLock]()

    def __call__(self, chunk: Chunk) -> _AsyncIOLock:
        lock = self.__lock_by_chunk.get(chunk)

        if lock is None:
            lock = _AsyncIOLock()
            self.__lock_by_chunk[chunk] = lock

        return lock
