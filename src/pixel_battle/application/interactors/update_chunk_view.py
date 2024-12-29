from dataclasses import dataclass

from pixel_battle.application.ports.broker import Broker
from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    DefaultChunkViewWhen,
)
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.lock import Lock
from pixel_battle.application.ports.offsets import Offsets
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateChunkView[ChunkViewT: ChunkView, OffsetT]:
    broker: Broker[OffsetT]
    offsets_of_latest_compressed_events: Offsets[OffsetT]
    lock: Lock
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_when: DefaultChunkViewWhen[ChunkViewT]

    async def __call__(self, chunk_number_x: int, chunk_number_y: int) -> None:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        async with self.lock(chunk):
            last_compressed_event_offset = (
                await self
                .offsets_of_latest_compressed_events
                .offset_when(chunk=chunk)
            )

            if last_compressed_event_offset is not None:
                not_compressed_events = await self.broker.events_after(
                    last_compressed_event_offset, chunk=chunk
                )
            else:
                not_compressed_events = await self.broker.events_when(
                    chunk=chunk
                )

            if len(not_compressed_events) == 0:
                return

            chunk_view = await self.chunk_views.chunk_view_when(chunk=chunk)

            if chunk_view is None:
                chunk_view = await self.default_chunk_view_when(chunk=chunk)

            pixels = (event.pixel for event in not_compressed_events)
            await chunk_view.redraw_by_pixels(pixels)

            await self.chunk_views.put(chunk_view, chunk=chunk)

            last_compressed_event = not_compressed_events[-1]

            await self.offsets_of_latest_compressed_events.put(
                last_compressed_event.offset, chunk=chunk
            )
