from pytest import mark

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber, chunk_where
from pixel_battle.entities.quantities.rectangle import Rectangle
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


@mark.parametrize(
    "chunk_number, area",
    [
        [
            ChunkNumber(x=0, y=0),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=249, y=249),
            ),
        ],
        [
            ChunkNumber(x=1, y=0),
            Rectangle(
                position1=Vector(x=250, y=0),
                position2=Vector(x=499, y=249),
            ),
        ],
        [
            ChunkNumber(x=3, y=2),
            Rectangle(
                position1=Vector(x=750, y=500),
                position2=Vector(x=999, y=749),
            ),
        ],
        [
            ChunkNumber(x=-1, y=0),
            Rectangle(
                position1=Vector(x=-250, y=249),
                position2=Vector(x=-1, y=0),
            ),
        ],
        [
            ChunkNumber(x=-2, y=-1),
            Rectangle(
                position1=Vector(x=-500, y=-250),
                position2=Vector(x=-251, y=-1),
            ),
        ],
    ]
)
def test_area(
    chunk_number: ChunkNumber, area: Rectangle
) -> None:
    chunk = Chunk(number=chunk_number)

    assert chunk.area == area
