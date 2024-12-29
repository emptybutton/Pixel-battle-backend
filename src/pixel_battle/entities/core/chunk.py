from dataclasses import dataclass
from math import ceil
from typing import ClassVar

from pixel_battle.entities.core.canvas import canvas
from pixel_battle.entities.geometry.rectangle import Rectangle, rectangle_with
from pixel_battle.entities.geometry.size import Size
from pixel_battle.entities.geometry.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class Chunk:
    size: ClassVar = Size(width=100, height=100)

    number: "ChunkNumber"

    @property
    def area(self) -> Rectangle:
        min_x_min_y_position = Vector(
            x=self.number.x * self.size.width,
            y=self.number.y * self.size.height,
        )

        return rectangle_with(
            min_x_min_y_position=min_x_min_y_position,
            size=self.size,
        )


class ChunkNumberError(Exception): ...


class ExtremeChunkNumberValuesError(ChunkNumberError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class ChunkNumber:
    max_x: ClassVar = ceil(canvas.area.size.width / Chunk.size.width) - 1
    max_y: ClassVar = ceil(canvas.area.size.height / Chunk.size.height) - 1

    x: int
    y: int

    def __post_init__(self) -> None:
        is_x_valid = 0 <= self.x <= ChunkNumber.max_x
        is_y_valid = 0 <= self.y <= ChunkNumber.max_y

        if not is_x_valid or not is_y_valid:
            raise ExtremeChunkNumberValuesError


def chunk_where(position: Vector) -> Chunk:
    chunk_number = ChunkNumber(
        x=position.x // Chunk.size.width,
        y=position.y // Chunk.size.height,
    )

    return Chunk(number=chunk_number)
