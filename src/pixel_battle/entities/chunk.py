from dataclasses import dataclass

from pixel_battle.entities.position import Position


@dataclass(kw_only=True, frozen=True, slots=True)
class Chunk:
    position: Position


def chunk_where(position: Position) -> Chunk:
    chunk_position = Position(x=position.x // 100, y=position.y // 100)

    return Chunk(position=chunk_position)
