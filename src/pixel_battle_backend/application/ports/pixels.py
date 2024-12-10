from abc import ABC, abstractmethod

from pixel_battle_backend.entities.pixel import Pixel
from pixel_battle_backend.entities.position import Position


class Pixels[PixelSetViewT](ABC):
    @abstractmethod
    async def add(self, pixel: Pixel) -> None: ...

    @abstractmethod
    async def remove(self, pixel: Pixel) -> None: ...

    @abstractmethod
    async def update(self, pixel: Pixel) -> None: ...

    @abstractmethod
    async def pixel_at(self, position: Position) -> Pixel: ...

    @abstractmethod
    async def view_of_pixels_inside_rectangle(
        self,
        position1: Position,
        position2: Position,
    ) -> PixelSetViewT: ...
