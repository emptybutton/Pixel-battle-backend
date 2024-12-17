from dataclasses import dataclass
from typing import Sequence

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    ChunkViews,
    DefaultChunkViewOf,
)
from pixel_battle.application.ports.pixels import Pixels
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[ChunkViewT: ChunkView]:
    chunk_view: ChunkViewT
    pixels: Sequence[Pixel[RGBColor]]


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunk[ChunkViewT: ChunkView]:
    pixel_batch: Pixels
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_of: DefaultChunkViewOf[ChunkViewT]

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> Output[ChunkViewT]:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        chunk_view = await self.chunk_views.chunk_view_of(chunk)
        pixels = await self.pixel_batch.pixels_of_chunk(chunk)

        if chunk_view is None:
            chunk_view = await self.default_chunk_view_of(chunk)

        return Output(pixels=pixels, chunk_view=chunk_view)
