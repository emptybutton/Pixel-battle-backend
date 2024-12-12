from dataclasses import dataclass

from pixel_battle.application.ports.pixels import ChunkViewOf, Pixels
from pixel_battle.entities.core.chunk import Chunk


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewChunk[PixelsT: Pixels, ChunkViewT]:
    chunk: Chunk
    pixels: PixelsT
    chunk_view_of: ChunkViewOf[PixelsT, ChunkViewT]

    async def __call__(self) -> ChunkViewT:
        return await self.chunk_view_of(self.pixels, chunk=self.chunk)
