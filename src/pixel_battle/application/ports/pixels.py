from abc import ABC, abstractmethod
from typing import Sequence

from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


class Pixels(ABC):
    @abstractmethod
    async def add(self, pixel: Pixel[RGBColor]) -> None: ...

    @abstractmethod
    async def pixels_of_chunk(self, chunk: Chunk) -> Sequence[Pixel[RGBColor]]:
        ...

    @abstractmethod
    async def lremove_pixels_of_chunk(
        self, chunk: Chunk, *, amount: int
    ) -> None:
        ...
