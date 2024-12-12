from pytest import mark

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber, chunk_where
from pixel_battle.entities.quantities.position import Position


@mark.parametrize(
    "position, chunk_number",
    [
        [Position(x=0, y=0), ChunkNumber(x=0, y=0)],
        [Position(x=1, y=0), ChunkNumber(x=0, y=0)],
        [Position(x=50, y=50), ChunkNumber(x=0, y=0)],
        [Position(x=150, y=50), ChunkNumber(x=1, y=0)],
        [Position(x=250, y=150), ChunkNumber(x=2, y=1)],
        [Position(x=599, y=600), ChunkNumber(x=5, y=6)],
        [Position(x=-99, y=-100), ChunkNumber(x=-1, y=-1)],
        [Position(x=-99, y=-101), ChunkNumber(x=-1, y=-2)],
    ]
)
def test_chunk_where_with_zero_position(
    position: Position, chunk_number: ChunkNumber
) -> None:
    assert chunk_where(position) == Chunk(number=chunk_number)
