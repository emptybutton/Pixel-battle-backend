from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    DefaultChunkViewWhen,
)
from pixel_battle.application.ports.frozen_chunk_view import ChunkViewFreezing
from pixel_battle.application.ports.frozen_chunk_views import FrozenChunkViews
from pixel_battle.application.ports.pixel_queue import (
    PixelQueue,
    PullingProcess,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[FrozenChunkViewT]:
    frozen_chunk_view: FrozenChunkViewT
    pixels: Sequence[Pixel[RGBColor]]


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunk[ChunkViewT: ChunkView = ChunkView, FrozenChunkViewT = Any]:
    pixel_queue: PixelQueue
    frozen_chunk_views: FrozenChunkViews[FrozenChunkViewT]
    default_chunk_view_when: DefaultChunkViewWhen[ChunkViewT]
    chunk_view_freezing: ChunkViewFreezing[ChunkViewT, FrozenChunkViewT]

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> Output[FrozenChunkViewT]:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        frozen_chunk_view = (
            await self.frozen_chunk_views.frozen_chunk_view_when(chunk=chunk)
        )

        process = PullingProcess.chunk_view_refresh
        pixels = await self.pixel_queue.uncommittable_pulled_pixels_when(
            chunk=chunk, process=process
        )

        if frozen_chunk_view is None:
            async with await self.default_chunk_view_when(chunk=chunk) as view:
                frozen_chunk_view = await self.chunk_view_freezing.frozen(view)

        return Output(pixels=pixels, frozen_chunk_view=frozen_chunk_view)
