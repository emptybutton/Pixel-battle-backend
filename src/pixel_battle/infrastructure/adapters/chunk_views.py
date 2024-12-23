from dataclasses import dataclass, field
from typing import ClassVar, Iterator

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.infrastructure.redis.keys import chunk_key_of


@dataclass(frozen=True, slots=True)
class InMemoryChunkViews[ChunkViewT: ChunkView](ChunkViews[ChunkViewT]):
    _view_by_chunk: dict[Chunk, ChunkViewT] = field(default_factory=dict)

    def __bool__(self) -> bool:
        return bool(self._view_by_chunk)

    def __iter__(self) -> Iterator[tuple[Chunk, ChunkViewT]]:
        return iter(self._view_by_chunk.items())

    async def chunk_view_of(self, chunk: Chunk) -> ChunkViewT | None:
        return self._view_by_chunk.get(chunk)

    async def put(self, view: ChunkViewT, *, chunk: Chunk) -> None:
        self._view_by_chunk[chunk] = view


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterPNGImageChunkViews(ChunkViews[PNGImageChunkView]):
    redis_cluster: RedisCluster
    close_when_putting: bool
    _field: ClassVar = b"view"

    async def chunk_view_of(self, chunk: Chunk) -> PNGImageChunkView | None:
        key = chunk_key_of(chunk)
        raw_view = await self.redis_cluster.hget(key, self._field)  # type: ignore[arg-type, misc]

        if raw_view is None:
            return None

        return PNGImageChunkView.from_bytes(raw_view)

    async def put(self, view: PNGImageChunkView, *, chunk: Chunk) -> None:
        with view.to_stream() as stream:
            if self.close_when_putting:
                view.close()

            buffer = stream.getbuffer()
            key = chunk_key_of(chunk)
            await self.redis_cluster.hset(key, self._field, buffer)  # type: ignore[arg-type, misc]
            buffer.release()
