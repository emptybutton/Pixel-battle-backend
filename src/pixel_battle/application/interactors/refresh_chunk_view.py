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


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshChunkView[ChunkViewT: ChunkView]:
    pixel_queue: PixelQueue
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_when: DefaultChunkViewWhen[ChunkViewT]

    async def __call__(self, chunk_number_x: int, chunk_number_y: int) -> None:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        process = PullingProcess.chunk_view_refresh
        committable_pixels = self.pixel_queue.committable_pulled_pixels_when(
            chunk=chunk, process=process, only_new=False
        )
        async with committable_pixels as pixels:
            chunk_view = await self.chunk_views.chunk_view_when(chunk=chunk)

            if chunk_view is None:
                chunk_view = await self.default_chunk_view_when(chunk=chunk)

            await chunk_view.redraw_by_pixels(pixels)

            await self.chunk_views.put(chunk_view, chunk=chunk)
