from dataclasses import dataclass

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    ChunkViews,
    DefaultChunkViewOf,
)
from pixel_battle.application.ports.pixels import Pixels
from pixel_battle.application.ports.users import Users
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber


@dataclass(kw_only=True, frozen=True, slots=True)
class ReducePixelBatch[ChunkViewT: ChunkView]:
    users: Users
    pixel_batch: Pixels
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_of: DefaultChunkViewOf[ChunkViewT]

    async def __call__(self, chunk_number_x: int, chunk_number_y: int) -> None:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))
        chunk_view = await self.chunk_views.chunk_view_of(chunk)

        if chunk_view is None:
            chunk_view = await self.default_chunk_view_of(chunk)

        pixels = await self.pixel_batch.pixels_of_chunk(chunk)
        await chunk_view.redraw_by_pixels(pixels)

        await self.chunk_views.put(chunk_view, chunk=chunk)
        await self.pixel_batch.lremove_pixels_of_chunk(
            chunk, amount=len(pixels)
        )