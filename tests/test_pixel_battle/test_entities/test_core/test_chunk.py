from pytest import mark

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber, chunk_where
from pixel_battle.entities.geometry.rectangle import Rectangle
from pixel_battle.entities.geometry.vector import Vector


@mark.parametrize(
    "position, chunk_number",
    [
        [Vector(x=0, y=0), ChunkNumber(x=0, y=0)],
        [Vector(x=1, y=0), ChunkNumber(x=0, y=0)],
        [Vector(x=100, y=50), ChunkNumber(x=1, y=0)],
        [Vector(x=199, y=200), ChunkNumber(x=1, y=2)],
    ]
)
def test_chunk_where(
    position: Vector, chunk_number: ChunkNumber
) -> None:
    assert chunk_where(position) == Chunk(number=chunk_number)


@mark.parametrize(
    "chunk_number, area",
    [
        [
            ChunkNumber(x=0, y=0),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=99, y=99),
            ),
        ],
        [
            ChunkNumber(x=1, y=0),
            Rectangle(
                position1=Vector(x=100, y=0),
                position2=Vector(x=199, y=99),
            ),
        ],
        [
            ChunkNumber(x=3, y=2),
            Rectangle(
                position1=Vector(x=300, y=200),
                position2=Vector(x=399, y=299),
            ),
        ],
    ]
)
def test_area(
    chunk_number: ChunkNumber, area: Rectangle
) -> None:
    chunk = Chunk(number=chunk_number)

    assert chunk.area == area
