from dataclasses import dataclass

from pixel_battle.application.ports.broker import Broker
from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    ChunkViews,
    DefaultChunkViewOf,
)
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateChunkView[ChunkViewT: ChunkView]:
    broker: Broker
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_of: DefaultChunkViewOf[ChunkViewT]

    async def __call__(self, chunk_number_x: int, chunk_number_y: int) -> None:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        async with self.lock(chunk):
            offset = await self.chunk_view_offsets.offset_for(chunk)
            new_events = self.broker.events_from(offset, chunk=chunk)

            if len(new_events) == 0:
                return

            chunk_view = await self.chunk_views.chunk_view_of(chunk)

            if chunk_view is None:
                chunk_view = await self.default_chunk_view_of(chunk)

            new_pixels = (event.pixel for event in new_events)
            await chunk_view.redraw_by_pixels(new_pixels)

            await self.chunk_views.put(chunk_view, chunk=chunk)

            last_event = new_events[-1]
            await self.chunk_view_offsets.put(last_event.offset, chunk=chunk)
