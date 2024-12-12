from dataclasses import dataclass
from typing import Iterable, Iterator

from pixel_battle.application.ports.pixels import ChunkViewOf, Pixels
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import Color, RGBColor
from pixel_battle.entities.quantities.position import Position
from pixel_battle.infrastructure.view import ChunkIdentityView


@dataclass(init=False)
class InMemoryPixels(Pixels):
    __pixel_by_position: dict[Position, Pixel[RGBColor]]

    def __init__(self, pixels: Iterable[Pixel[RGBColor]] = tuple()) -> None:
        self.__pixel_by_position = {pixel.position: pixel for pixel in pixels}

    def __iter__(self) -> Iterator[Pixel[RGBColor]]:
        return iter(self.__pixel_by_position.values())

    def __len__(self) -> int:
        return len(self.__pixel_by_position)

    def __bool__(self) -> bool:
        return bool(self.__pixel_by_position)

    async def put(self, pixel: Pixel[RGBColor]) -> None:
        self.__pixel_by_position[pixel.position] = pixel

    async def remove[ColorT: Color](self, pixel: Pixel[ColorT]) -> None:
        if pixel.position in self.__pixel_by_position:
            del self.__pixel_by_position[pixel.position]


class ChunkIdentityViewOfInMemoryPixels(
    ChunkViewOf[InMemoryPixels, ChunkIdentityView]
):
    async def __call__(
        self, pixels: InMemoryPixels, *, chunk: Chunk
    ) -> ChunkIdentityView:
        return frozenset({pixel for pixel in pixels if pixel.chunk == chunk})
