from dataclasses import dataclass
from enum import Enum, auto

from pixel_battle.application.ports.chunk_optimistic_lock import (
    ChunkOptimisticLockWhen,
)
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


class Error(Enum):
    concurrent_refresh = auto()


type Ok = None
ok: Ok = None

type Output = Ok | Error


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshChunkView[ChunkViewT: ChunkView]:
    pixel_queue: PixelQueue
    chunk_views: ChunkViews[ChunkViewT]
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

                await chunk_view.redraw_by_pixels(pixels)

                await self.chunk_views.put(chunk_view, chunk=chunk)
                return ok
