from abc import ABC, abstractmethod

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import Color, RGBColor


class Pixels(ABC):
    @abstractmethod
    async def put(self, pixel: Pixel[RGBColor]) -> None: ...

    @abstractmethod
    async def remove[ColorT: Color](self, pixel: Pixel[ColorT]) -> None:
        ...


class ChunkViewFrom[ChunkViewT](ABC):
    @abstractmethod
    async def __call__(self, pixels: Pixels, *, chunk: Chunk) -> ChunkViewT:
        ...
