from dataclasses import dataclass
from typing import ClassVar

from pixel_battle.entities.quantities.rectangle import Rectangle
from pixel_battle.entities.quantities.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class ChunkNumber:
    x: int
    y: int


@dataclass(kw_only=True, frozen=True, slots=True)
class Chunk:
    width: ClassVar = 250
    height: ClassVar = 250

    number: ChunkNumber

    @property
    def area(self) -> Rectangle:
        position1 = Vector(
            x=self.number.x * self.width,
            y=self.number.y * self.height,
        )
        position2 = Vector(
            x=(self.number.x + 1) * self.width - 1,
            y=(self.number.y + 1) * self.height - 1,
        )

        return Rectangle(position1=position1, position2=position2)


def chunk_where(position: Vector) -> Chunk:
    chunk_number = ChunkNumber(
        x=position.x // Chunk.width,
        y=position.y // Chunk.height,
    )

    return Chunk(number=chunk_number)
