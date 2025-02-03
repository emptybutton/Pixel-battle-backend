from collections.abc import Sequence
from dataclasses import dataclass

from pixel_battle.application.ports.pixel_queue import PixelQueue
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    new_pixels: Sequence[Pixel[RGBColor]]


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunkStream:
    pixel_queue: PixelQueue

    async def __call__(
        self, chunk_number_x: int, chunk_number_y: int
    ) -> Output:
        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        committable_pixels = self.pixel_queue.committable_pulled_pixels_when(
            chunk=chunk, process=None, only_new=True
        )
        async with committable_pixels as pixels:
            return Output(new_pixels=pixels)
