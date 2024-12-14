from pytest import mark

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber, chunk_where
from pixel_battle.entities.quantities.vector import Vector


@mark.parametrize(
    "position, chunk_number",
    [
        [Vector(x=0, y=0), ChunkNumber(x=0, y=0)],
        [Vector(x=1, y=0), ChunkNumber(x=0, y=0)],
        [Vector(x=250, y=150), ChunkNumber(x=1, y=0)],
        [Vector(x=499, y=500), ChunkNumber(x=1, y=2)],
        [Vector(x=-249, y=-250), ChunkNumber(x=-1, y=-1)],
        [Vector(x=-249, y=-251), ChunkNumber(x=-1, y=-2)],
    ]
)
def test_chunk_where(
    position: Vector, chunk_number: ChunkNumber
) -> None:
    assert chunk_where(position) == Chunk(number=chunk_number)
