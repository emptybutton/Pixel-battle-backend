from dataclasses import dataclass, field
from typing import ClassVar

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.offsets import Offsets
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.redis_cluster.keys import chunk_key_of


@dataclass(frozen=True, slots=True)
class InMemoryOffsets(Offsets):
    _offsets_by_chunk: dict[Chunk, int] = field(defaul_factory=dict)

    def __bool__(self) -> bool:
        return bool(self._offsets_by_chunk)

    async def put(self, offset: int, *, chunk: Chunk) -> None:
        self._offsets_by_chunk[chunk] = offset

    async def offset_for(self, chunk: Chunk) -> int | None:
        return self._offsets_by_chunk.get(chunk)


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterOffsets(Offsets):
    _field: ClassVar = "offset"
    redis_cluster: RedisCluster

    async def put(self, offset: int, *, chunk: Chunk) -> None:
        key = chunk_key_of(chunk).decode()
        await self.redis_cluster.hset(key, self._field, offset)

    async def offset_for(self, chunk: Chunk) -> int | None:
        key = chunk_key_of(chunk).decode()
        raw_offset = await self.redis_cluster.hget(key, self._field)

        try:
            return int(raw_offset)
        except ValueError:
            return None
