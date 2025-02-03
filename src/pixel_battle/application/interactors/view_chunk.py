from collections.abc import Sequence
from dataclasses import dataclass

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    DefaultChunkViewWhen,
)
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.pixel_queue import (
    PixelQueue,
    PullingProcess,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[ChunkViewT: ChunkView]:
    chunk_view: ChunkViewT
    pixels: Sequence[Pixel[RGBColor]]


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunk[ChunkViewT: ChunkView]:
    pixel_queue: PixelQueue
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_when: DefaultChunkViewWhen[ChunkViewT]

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> Output[ChunkViewT]:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        chunk_view = await self.chunk_views.chunk_view_when(chunk=chunk)

        process = PullingProcess.chunk_view_refresh
        pixels = await self.pixel_queue.uncommittable_pulled_pixels_when(
            chunk=chunk, process=process, only_new=False
        )

        if chunk_view is None:
            chunk_view = await self.default_chunk_view_when(chunk=chunk)

        return Output(pixels=pixels, chunk_view=chunk_view)
