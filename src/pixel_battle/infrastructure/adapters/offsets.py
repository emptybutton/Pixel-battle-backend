from dataclasses import dataclass, field
from typing import ClassVar, Iterator

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.offsets import Offsets
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.redis.keys import chunk_key_of
from pixel_battle.infrastructure.redis.types import RedisStreamOffset


@dataclass(frozen=True, slots=True)
class InMemoryOffsets[OffsetT](Offsets[OffsetT]):
    _offsets_by_chunk: dict[Chunk, OffsetT] = field(default_factory=dict)

    def __iter__(self) -> Iterator[tuple[Chunk, OffsetT]]:
        return iter(self._offsets_by_chunk.items())

    def __bool__(self) -> bool:
        return bool(self._offsets_by_chunk)

    async def put(self, offset: OffsetT, *, chunk: Chunk) -> None:
        self._offsets_by_chunk[chunk] = offset

    async def offset_where(self, *, chunk: Chunk) -> OffsetT | None:
        return self._offsets_by_chunk.get(chunk)


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterRedisStreamOffsets(Offsets[RedisStreamOffset]):
    _field: ClassVar = b"offset"
    redis_cluster: RedisCluster

    async def put(self, offset: RedisStreamOffset, *, chunk: Chunk) -> None:
        key = chunk_key_of(chunk)
        await self.redis_cluster.hset(key, self._field, offset)  # type: ignore[misc, arg-type]

    async def offset_where(self, *, chunk: Chunk) -> RedisStreamOffset | None:
        key = chunk_key_of(chunk)
        offset: bytes | None = await self.redis_cluster.hget(key, self._field)  # type: ignore[misc, arg-type]

        return offset
