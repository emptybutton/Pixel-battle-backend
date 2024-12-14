from pytest import fixture

from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import black
from pixel_battle.entities.quantities.position import Position
from pixel_battle.infrastructure.adapters.chunk_view import (
    CollectionChunkView,
    InMemoryChunkViews,
)


@fixture
def chunk1() -> Chunk:
    return Chunk(number=ChunkNumber(x=0, y=0))


@fixture
def chunk2() -> Chunk:
    return Chunk(number=ChunkNumber(x=1, y=1))


@fixture
def chunk1_view() -> CollectionChunkView:
    return CollectionChunkView([
        Pixel(position=Position(x=0, y=0), color=black),
        Pixel(position=Position(x=50, y=50), color=black),
        Pixel(position=Position(x=75, y=75), color=black)
    ])


@fixture
def chunk2_view() -> CollectionChunkView:
    return CollectionChunkView([
        Pixel(position=Position(x=100, y=100), color=black),
        Pixel(position=Position(x=150, y=150), color=black),
        Pixel(position=Position(x=175, y=175), color=black)
    ])


async def test_chunk_view_of_without_stored_chunk(
    chunk1: Chunk, chunk1_view: CollectionChunkView, chunk2: Chunk
) -> None:
    views = InMemoryChunkViews({chunk1: chunk1_view})

    assert await views.chunk_view_of(chunk2) is None


async def test_chunk_view_of_with_stored_chunk(
    chunk1: Chunk,
    chunk1_view: CollectionChunkView,
    chunk2: Chunk,
    chunk2_view: CollectionChunkView,
) -> None:
    views = InMemoryChunkViews({chunk1: chunk1_view, chunk2: chunk2_view})

    assert await views.chunk_view_of(chunk2) is chunk2_view


async def test_put_with_stored_chunk(
    chunk1: Chunk,
    chunk1_view: CollectionChunkView,
    chunk2_view: CollectionChunkView,
) -> None:
    views = InMemoryChunkViews({chunk1: chunk1_view})

    await views.put(chunk2_view, chunk=chunk1)

    assert views.to_dict() == {chunk1: chunk2_view}


async def test_put_without_stored_chunk(
    chunk1: Chunk,
    chunk1_view: CollectionChunkView,
    chunk2: Chunk,
    chunk2_view: CollectionChunkView,
) -> None:
    views = InMemoryChunkViews({chunk1: chunk1_view})

    await views.put(chunk2_view, chunk=chunk2)

    assert views.to_dict() == {chunk1: chunk1_view, chunk2: chunk2_view}
