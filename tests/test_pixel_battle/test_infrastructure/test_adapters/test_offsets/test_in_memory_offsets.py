from pytest import fixture

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.infrastructure.adapters.offsets import InMemoryOffsets


@fixture
def chunk() -> Chunk:
    return Chunk(number=ChunkNumber(x=0, y=0))


@fixture
def offset() -> int:
    return 4


async def test_put(chunk: Chunk, offset: int) -> None:
    offsets = InMemoryOffsets()

    await offsets.put(offset, chunk=chunk)

    assert dict(offsets) == {chunk: offset}


async def test_offset_when_without_offset(chunk: Chunk, offset: int) -> None:
    offsets = InMemoryOffsets()

    offset = await offsets.offset_when(chunk=chunk)

    assert offset is None


async def test_offset_when_with_offset(chunk: Chunk, offset: int) -> None:
    offsets = InMemoryOffsets({chunk: offset})

    offset = await offsets.offset_when(chunk=chunk)

    assert offset == offset
