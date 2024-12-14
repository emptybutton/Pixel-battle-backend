from pytest import mark

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber, chunk_where
from pixel_battle.entities.quantities.position import Position


@mark.parametrize(
    "position, chunk_number",
    [
        [Position(x=0, y=0), ChunkNumber(x=0, y=0)],
        [Position(x=1, y=0), ChunkNumber(x=0, y=0)],
        [Position(x=250, y=150), ChunkNumber(x=1, y=0)],
        [Position(x=499, y=500), ChunkNumber(x=1, y=2)],
        [Position(x=-249, y=-250), ChunkNumber(x=-1, y=-1)],
        [Position(x=-249, y=-251), ChunkNumber(x=-1, y=-2)],
    ]
)
def test_chunk_where(
    position: Position, chunk_number: ChunkNumber
) -> None:
    assert chunk_where(position) == Chunk(number=chunk_number)
