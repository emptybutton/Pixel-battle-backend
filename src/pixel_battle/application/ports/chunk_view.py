from abc import ABC, abstractmethod
from collections.abc import Iterable

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor


class ChunkView(ABC):
    @abstractmethod
    async def redraw_by_pixels(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        ...


class DefaultChunkViewWhen[ChunkViewT: ChunkView](ABC):
    @abstractmethod
    async def __call__(self, *, chunk: Chunk) -> ChunkViewT: ...
