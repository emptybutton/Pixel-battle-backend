from dataclasses import dataclass
from typing import Any, Sequence

from pixel_battle.application.ports.broker import Broker
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    new_pixels: Sequence[Pixel[RGBColor]]


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunkStream:
    broker: Broker[Any]

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> Output:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        async with self.broker.pulled_events_when(chunk=chunk) as events:
            new_pixels = tuple(event.pixel for event in events)
            return Output(new_pixels=new_pixels)
