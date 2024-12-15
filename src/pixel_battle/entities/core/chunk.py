from dataclasses import dataclass
from typing import ClassVar

from pixel_battle.entities.quantities.rectangle import Rectangle, rectangle_with
from pixel_battle.entities.quantities.size import Size
from pixel_battle.entities.quantities.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class ChunkNumber:
    x: int
    y: int


@dataclass(kw_only=True, frozen=True, slots=True)
class Chunk:
    size: ClassVar = Size(width=250, height=250)

    number: ChunkNumber

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


def chunk_where(position: Vector) -> Chunk:
    chunk_number = ChunkNumber(
        x=position.x // Chunk.size.width,
        y=position.y // Chunk.size.height,
    )

    return Chunk(number=chunk_number)
