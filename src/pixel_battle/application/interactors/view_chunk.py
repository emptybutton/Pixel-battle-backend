from dataclasses import dataclass

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    ChunkViews,
    DefaultChunkViewOf,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunk[ChunkViewT: ChunkView]:
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_of: DefaultChunkViewOf[ChunkViewT]

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> ChunkViewT:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))
        chunk_view = await self.chunk_views.chunk_view_of(chunk)

        if chunk_view is None:
            chunk_view = await self.default_chunk_view_of(chunk)

        return chunk_view
