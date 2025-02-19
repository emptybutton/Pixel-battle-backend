from collections.abc import Iterator
from copy import deepcopy
from dataclasses import dataclass, field
from typing import ClassVar

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.adapters.chunk_view import PNGImageChunkView
from pixel_battle.infrastructure.redis.keys import chunk_key_when


@dataclass(frozen=True, slots=True)
class InMemoryChunkViews[ChunkViewT: ChunkView](ChunkViews[ChunkViewT]):
    _view_by_chunk: dict[Chunk, ChunkViewT] = field(default_factory=dict)

    def __bool__(self) -> bool:
        return bool(self._view_by_chunk)

    def __iter__(self) -> Iterator[tuple[Chunk, ChunkViewT]]:
        return iter(self._view_by_chunk.items())

    async def chunk_view_when(self, *, chunk: Chunk) -> ChunkViewT | None:
        return self._view_by_chunk.get(chunk)

    async def put(self, view: ChunkViewT, *, chunk: Chunk) -> None:
        self._view_by_chunk[chunk] = deepcopy(view)


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterPNGImageChunkViews(ChunkViews[PNGImageChunkView]):
    redis_cluster: RedisCluster
    _field: ClassVar = b"png_image_unformatted_data"

    async def chunk_view_when(
        self, *, chunk: Chunk
    ) -> PNGImageChunkView | None:
        key = chunk_key_when(chunk=chunk)
        pixel_data = await self.redis_cluster.hget(key, self._field)  # type: ignore[arg-type, misc]

        if pixel_data is None:
            return None

        return PNGImageChunkView.from_pixel_data(pixel_data)

    async def put(self, view: PNGImageChunkView, *, chunk: Chunk) -> None:
        key = chunk_key_when(chunk=chunk)
        pixel_data = view.to_pixel_data()
        await self.redis_cluster.hset(key, self._field, pixel_data)  # type: ignore[arg-type, misc]
