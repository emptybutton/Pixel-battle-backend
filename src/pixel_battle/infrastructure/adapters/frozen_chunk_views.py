from dataclasses import dataclass
from typing import Any, ClassVar

from redis.asyncio import RedisCluster

from pixel_battle.application.ports.frozen_chunk_views import FrozenChunkViews
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.adapters.frozen_chunk_view import (
    FrozenPNGImageChunkView,
)
from pixel_battle.infrastructure.redis.keys import chunk_key_when


@dataclass(kw_only=True, frozen=True, slots=True, unsafe_hash=False)
class InMemoryFrozenChunkViews[FrozenChunkViewT = Any](
    FrozenChunkViews[FrozenChunkViewT]
):
    frozen_chunk_view_by_chunk: dict[Chunk, FrozenChunkViewT]

    async def frozen_chunk_view_when(
        self, *, chunk: Chunk
    ) -> FrozenChunkViewT | None:
        return self.frozen_chunk_view_by_chunk.get(chunk)

    async def put(self, view: FrozenChunkViewT, *, chunk: Chunk) -> None:
        self.frozen_chunk_view_by_chunk[chunk] = view


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterFrozenPNGImageChunkViews(
    FrozenChunkViews[FrozenPNGImageChunkView]
):
    redis_cluster: RedisCluster
    _field: ClassVar = b"png_image_formatted_data"

    async def frozen_chunk_view_when(
        self, *, chunk: Chunk
    ) -> FrozenPNGImageChunkView | None:
        key = chunk_key_when(chunk=chunk)

        view: FrozenPNGImageChunkView
        view = await self.redis_cluster.hget(key, self._field)  # type: ignore[arg-type, misc]
        return view

    async def put(self, view: FrozenPNGImageChunkView, *, chunk: Chunk) -> None:
        key = chunk_key_when(chunk=chunk)
        await self.redis_cluster.hset(key, self._field, view)  # type: ignore[arg-type, misc]
