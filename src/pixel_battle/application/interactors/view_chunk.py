from dataclasses import dataclass
from typing import Sequence

from pixel_battle.application.ports.broker import Broker
from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    DefaultChunkViewOf,
)
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.offsets import Offsets
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[ChunkViewT: ChunkView]:
    chunk_view: ChunkViewT
    pixels: Sequence[Pixel[RGBColor]]


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunk[ChunkViewT: ChunkView, OffsetT]:
    broker: Broker[OffsetT]
    offsets_of_latest_compressed_events: Offsets[OffsetT]
    chunk_views: ChunkViews[ChunkViewT]
    default_chunk_view_of: DefaultChunkViewOf[ChunkViewT]

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> Output[ChunkViewT]:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        chunk_view = await self.chunk_views.chunk_view_of(chunk)
        offset = await self.offsets_of_latest_compressed_events.offset_for(
            chunk
        )

        if offset is not None:
            events = await self.broker.events_after(offset, chunk=chunk)
        else:
            events = await self.broker.events_of(chunk)

        if chunk_view is None:
            chunk_view = await self.default_chunk_view_of(chunk)

        pixels = tuple(event.pixel for event in events)
        return Output(pixels=pixels, chunk_view=chunk_view)
