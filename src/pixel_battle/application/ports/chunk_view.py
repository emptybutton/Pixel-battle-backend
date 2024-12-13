from abc import ABC, abstractmethod

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


class ChunkView(ABC):
    @abstractmethod
    async def redraw(self, pixel: Pixel[RGBColor]) -> None: ...


class ChunkViews[ChunkViewT: ChunkView](ABC):
    @abstractmethod
    async def chunk_view_of(self, chunk: Chunk) -> ChunkViewT | None: ...

    @abstractmethod
    async def put(self, view: ChunkViewT, *, chunk: Chunk) -> None: ...


class DefaultChunkViewOf[ChunkViewT: ChunkView](ABC):
    @abstractmethod
    async def __call__(self, chunk: Chunk) -> ChunkViewT: ...
