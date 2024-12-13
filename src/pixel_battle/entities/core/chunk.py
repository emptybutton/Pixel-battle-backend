from dataclasses import dataclass

from pixel_battle.entities.quantities.position import Position


@dataclass(kw_only=True, frozen=True, slots=True)
class ChunkNumber:
    x: int
    y: int


@dataclass(kw_only=True, frozen=True, slots=True)
class Chunk:
    number: ChunkNumber


def chunk_where(position: Position) -> Chunk:
    chunk_number = ChunkNumber(x=position.x // 250, y=position.y // 250)

    return Chunk(number=chunk_number)
