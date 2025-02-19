from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from pixel_battle.application.ports.chunk_optimistic_lock import (
    ChunkOptimisticLockWhen,
)
from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    DefaultChunkViewWhen,
)
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.frozen_chunk_view import ChunkViewFreezing
from pixel_battle.application.ports.frozen_chunk_views import FrozenChunkViews
from pixel_battle.application.ports.pixel_queue import (
    PixelQueue,
    PullingProcess,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber


class Error(Enum):
    concurrent_refresh = auto()


type Ok = None
ok: Ok = None

type Output = Ok | Error


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshChunk[ChunkViewT: ChunkView = ChunkView, FrozenChunkViewT = Any]:
    pixel_queue: PixelQueue
    chunk_views: ChunkViews[ChunkViewT]
    frozen_chunk_views: FrozenChunkViews[FrozenChunkViewT]
    chunk_view_freezing: ChunkViewFreezing[ChunkViewT, FrozenChunkViewT]
    default_chunk_view_when: DefaultChunkViewWhen[ChunkViewT]
    chunk_optimistic_lock_when: ChunkOptimisticLockWhen

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> Output:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        lock = self.chunk_optimistic_lock_when(chunk=chunk)
        committable_pixels = self.pixel_queue.committable_pulled_pixels_when(
            process=PullingProcess.chunk_view_refresh,
            chunk=chunk,
            only_new=False
        )
        async with lock as active_lock:
            if not active_lock.is_owned:
                return Error.concurrent_refresh

            async with committable_pixels as pixels:
                chunk_view = await self.chunk_views.chunk_view_when(chunk=chunk)

                if chunk_view is None:
                    chunk_view = await self.default_chunk_view_when(chunk=chunk)

                async with chunk_view:
                    await chunk_view.redraw_by_pixels(pixels)
                    frozen_chunk_view = await self.chunk_view_freezing.frozen(
                        chunk_view
                    )
                    await self.chunk_views.put(chunk_view, chunk=chunk)

                await self.frozen_chunk_views.put(
                    frozen_chunk_view, chunk=chunk
                )
                return ok
