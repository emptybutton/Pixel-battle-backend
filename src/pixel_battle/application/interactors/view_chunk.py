from dataclasses import dataclass

from pixel_battle.application.ports.pixels import ChunkViewFrom, Pixels
from pixel_battle.entities.core.chunk import Chunk


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunk[PixelSetViewT]:
    chunk: Chunk
    pixels: Pixels
    chunk_view_of: ChunkViewFrom[PixelSetViewT]

    async def __call__(self) -> PixelSetViewT:
        return await self.chunk_view_of(self.pixels, chunk=self.chunk)
