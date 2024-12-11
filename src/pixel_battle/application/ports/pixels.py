from abc import ABC, abstractmethod

from pixel_battle.entities.chunk import Chunk
from pixel_battle.entities.color import Color, RGBColor
from pixel_battle.entities.pixel import Pixel


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
